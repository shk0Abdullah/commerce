from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.makelist, name="create"),
    path("display", views.display, name ="display"),
    path("listed/<int:id>", views.listed,name="listed"),
    path("removeitem/<int:id>", views.removeitem, name="removeitem"),
    path("additem/<int:id>", views.additem, name="additem"),
    path("watchlist", views.displayWatchlist , name="watchlist"),
    path("addComment/<int:id>", views.addComment , name="addComment"),
    path("addBid/<int:id>", views.addBid, name="addBid"),
    path("closeAuction/<int:id>", views.closeAuction, name="closeAuction")
]
