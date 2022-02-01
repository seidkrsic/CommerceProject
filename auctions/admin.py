from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from .models import Category, User, Bid, AuctionListing, Comments, Watchlist
# Register your models here.
admin.site.register(User)
admin.site.register(Bid)
admin.site.register(AuctionListing)
admin.site.register(Comments)
admin.site.register(Watchlist)
admin.site.register(Category)