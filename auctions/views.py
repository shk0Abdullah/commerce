from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, listing, Comment, Bid

def index(request):
    categories = Category.objects.all() 
    active = listing.objects.filter(isActive=True)
    return render(request, "auctions/index.html",{
        "listings" : active,
        "categories":categories
    })

def makelist(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        return render(request, "auctions\create.html",{
            'categories' : categories,
        })
    else:
        # Take the data
        title = request.POST['title']
        description = request.POST['description']
        img = request.POST['img']
        price = request.POST['price']
        category = request.POST['category']
        # User
        user = request.user
        # creating a bid
        bid = Bid(bid= (price), user=user)
        bid.save()
        categoryData = Category.objects.get(category_name=category)
        # Create an obj
        new = listing(
            title = title,
            description = description,
            img=img,
            price=bid,
            owner=user,
            category=categoryData
        )
        # Inserting to DB
        new.save()
        return HttpResponseRedirect(reverse(index))\

def display(request):
    if request.method == "POST":
        categories = Category.objects.all() 
        cat = request.POST['category']
        category = Category.objects.get(category_name=cat)
        active = listing.objects.filter(isActive=True, category=category)
        return render(request, "auctions\display.html",{
            "cats":category,
            "categories": categories,
            "listings" : active
        })
def closeAuction(request, id):
    lsdata = listing.objects.get(pk=id)
    lsdata.isActive = False
    lsdata.save()
    Comments = Comment.objects.filter(listing=lsdata)
    isWatchlist = request.user in lsdata.watchlist.all()
    isOwner = request.user.username == lsdata.owner.username
    return render(request, "auctions\listed.html", {
        "updated": True,
        "list_item":lsdata,
        "comments":Comments,
        "message":"Auction closes Successfully!",
        "isWatchlist":isWatchlist,
        "isOwner":isOwner,
    })

def listed(request, id):

    lsdata = listing.objects.get(pk=id)
    comments = Comment.objects.filter(listing=lsdata)
    isOwner = request.user.username == lsdata.owner.username
    isWatchlist = request.user in lsdata.watchlist.all()
        
       
    message = ""
    updated = False
        
    if request.method == "POST":
           
        if "addBid" in request.POST:
            newBid = request.POST['newBid']
              
            if int(newBid) > lsdata.price.bid:
                message = "Bid was Successful"
                updated = True
            else:
                message = "Bid was Failed"
        
    return render(request, "auctions/listed.html", {
            "list_item": lsdata,
            "comments": comments,
            "isWatchlist": isWatchlist,
            "message": message,
            "updated": updated,
            "isOwner":isOwner,
        })

    
def removeitem(request, id):
    lsdata = listing.objects.get(pk=id)
    user = request.user
    lsdata.watchlist.remove(user)
    return HttpResponseRedirect(reverse(listed, args=[id] ))
def additem(request,id):
    lsdata = listing.objects.get(pk=id)
    user = request.user
    lsdata.watchlist.add(user)
    return HttpResponseRedirect(reverse(listed, args=[id] ))
def addBid(request, id):
    newBid = request.POST['newBid']
    listingData = listing.objects.get(pk=id)
    isOwner = request.user.username == listingData.owner.username
    Comments = Comment.objects.filter(listing=listingData)
    isWatchlist = request.user in listingData.watchlist.all()
    if int(newBid)>listingData.price.bid:
        update = Bid(user=request.user, bid=int(newBid))
        update.save()
        listingData.price = update
        listingData.save()
        return render(request, "auctions\listed.html", {
            "isOwner":isOwner,
            'updated': True,
            "message": "Bid was Successful",
            'list_item': listingData,
            "comments":Comments,
            "isWatchlist":isWatchlist
        })
    else:
        return render(request, "auctions\listed.html", {
            "isOwner":isOwner,
            'updated': False,
            "message": "Bid was Failed",
            'list_item': listingData ,
            "comments":Comments,
            "isWatchlist":isWatchlist
        })
        
def addComment(request, id):
    user = request.user
    listeditem = listing.objects.get(pk = id)
    message = request.POST['newComment']
    new = Comment(
        author=user,
        listing=listeditem,
        message=message
    )
    new.save()
    return HttpResponseRedirect(reverse(listed, args=[id] ))


def displayWatchlist(request):
    user = request.user
    watchlists = user.watchlist.all()
    return render(request, 'auctions\watchlist.html',{
        "watchlists":watchlists
    })
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
