from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE, SET_DEFAULT
from django.db.models.enums import Choices
from django.db.models.fields import CharField, DecimalField
from django.db.models.fields.related import ForeignKey, ManyToManyField
from datetime import datetime

from django.db.models.fields.reverse_related import ManyToOneRel
from django.forms.models import ModelMultipleChoiceField
from django.forms.widgets import NumberInput



class User(AbstractUser):
    pass
    
class Bid(models.Model): 
    value = models.DecimalField(max_digits=6,decimal_places=2,default=0)
    user = models.ForeignKey(User,blank=True, on_delete=CASCADE,null=True)
    auction = models.IntegerField(blank=False,default=-1)
    def __str__(self):
        return f"{self.user} bid is: {self.value}"

class Comments(models.Model):
    author = models.ForeignKey(User,on_delete=CASCADE,null=True,blank=True)
    content = models.CharField(max_length=999)

class Category(models.Model): 
    name = models.CharField(max_length=64)
    def __str__(self): 
        return f"{self.name}"

class AuctionListing(models.Model): 
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=999)
    bid = models.ForeignKey(Bid,on_delete=models.SET_NULL,blank=True,null=True,related_name='listings')
    comments = models.ManyToManyField(Comments,blank=True,null=True)
    product_photo = models.ImageField(upload_to='images',null=True,blank=True)
    created_at = models.DateTimeField(default=datetime.now,blank=True)
    category = models.ManyToManyField(Category,null=True,blank=True,related_name='auctions')
    creator = models.ForeignKey(User,on_delete=CASCADE,blank=True,null=True)
    open = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.title}, bid: {self.bid}"

class Watchlist(models.Model):
    user = ForeignKey(User,blank=True,null=True,on_delete=CASCADE)
    auctions = ManyToManyField(AuctionListing,blank=True,null=True,related_name='watchlists')

