from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
class Category(models.Model):
    category_name = models.CharField(max_length=30)
    def __str__(self):
        return self.category_name    
class Bid(models.Model):
    bid = models.FloatField(default=0)
    user = models.ForeignKey(User,on_delete=models.CASCADE, blank=True, null=True, related_name="userbid")

    

class listing(models.Model):
    title = models.CharField(max_length=35)
    description = models.CharField(max_length=350)
    img = models.CharField(max_length=2000)
    price = models.ForeignKey("Bid", on_delete=models.CASCADE, null=True, blank=True,related_name="bidprice")
    isActive = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='user')
    category = models.ForeignKey(Category,on_delete=models.CASCADE,blank=True,null=True,related_name='category')
    watchlist = models.ManyToManyField(User, blank=True, null=True,related_name="watchlist")
    def __str__(self):
        return self.title
class Comment(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE, blank=True, null=True, related_name="usercomment")
    listing = models.ForeignKey(listing,on_delete=models.CASCADE, blank=True, null=True, related_name="listingcomment")
    message = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.author} comments on {self.listing}"


    