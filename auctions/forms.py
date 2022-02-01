
from msilib.schema import File
from tkinter import Widget
from django.contrib.auth import models
from django.forms import ModelForm, Textarea, TextInput, SelectMultiple, FileInput

from .models import AuctionListing, Bid, Comments, Category
from django import forms 

class BidForm(ModelForm):
    class Meta: 
        model = Bid 
        fields = ['value']

class AuctionListingForm(ModelForm,forms.Form):
    class Meta: 
        model = AuctionListing
        fields = '__all__'
        field_classes = { 
            'categories' : forms.ModelMultipleChoiceField(queryset = Category.objects.all())
        }
        widgets = {
            'title': TextInput(attrs={
                'size': 60,
                'class':'specialInput', 
                'placeholder':'Auction title'
                }),

            'description': Textarea(attrs={
                'cols': 80, 
                'rows': 20, 
                'class': 'specialText',
                'placeholder': 'Describe your product here',
                }),
            'category': SelectMultiple(attrs={
                'class':'specialMultiple',
                
                }),
            'product_photo': FileInput(attrs={
                'class': 'specialFile',
            })
        }

class CommentsForm(ModelForm):
    class Meta: 
        model = Comments
        fields = ['content']
        labels  = {
            'content': 'Your Comment',
        }
        widgets= { 
            'content': Textarea(attrs={
                'size': 50,
                'class' : 'inputComment',
                'placeholder':' Type your comment',
                }),
        }