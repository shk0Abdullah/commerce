from django.contrib import admin
from .models import User, Category, listing, Comment, Bid
# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(listing)
admin.site.register(Comment)
admin.site.register(Bid)

