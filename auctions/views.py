from django import forms
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import auctions
from auctions.forms import AuctionListingForm, BidForm, CommentsForm
from auctions.models import AuctionListing, Category, Comments, User, Bid, Watchlist

def maksimum_bid(bids):
    max_bid = 0
    for value in bids:
        if float(value.value)>max_bid:
            max_bid = float(value.value)
    return max_bid


def index(request):
    auctions = AuctionListing.objects.all()
    categories = Category.objects.all()
    bids = {}
    for auction in auctions: 
        if Bid.objects.filter(auction=auction.id):
            bid = Bid.objects.filter(auction=auction.id)
            bid = maksimum_bid(bid)
            bids[auction]=bid 
        else: 
            bids[auction]=False 

    return render(request, "auctions/index.html",{
        'auctions': bids,
        'categories': categories,
    })

def categories(request): 
    categories = Category.objects.all()
    return render(request,'auctions/categories.html', {
        'categories': categories,
    })

def listCategory(request,name):
    category = Category.objects.get(name=name)
    auctions = category.auctions.all()
    bids = {}
    for auction in auctions: 
        if Bid.objects.filter(auction=auction.id):
            bid = Bid.objects.filter(auction=auction.id)
            bid = maksimum_bid(bid)
            bids[auction]=bid 
        else: 
            bids[auction]=False 

    return render(request,'auctions/category.html', { 
        'auctions' : bids,
        'categoryName':category.name,

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


# How to import picture settings are on this link: https://www.youtube.com/watch?v=aNk2CAkHvlE&ab_channel=DennisIvy
@login_required()
def createListing(request): 
    if request.method == 'POST':
        form = AuctionListingForm(request.POST,request.FILES)
        if form.is_valid():
            auction = AuctionListingForm(request.POST,request.FILES)
            auction = auction.save()
            user = User.objects.get(username=request.user)
            auction.creator = user 
            auction.open = True 
            auction.save()
            return HttpResponseRedirect(reverse('index'))
       
    else: 
        form = AuctionListingForm()
        return render(request,'auctions/createListing.html',{
            'form': form,   
        })



def ListingPage(request,list_id):
    global maksimum_bid
    if request.method == 'POST':
        auction = AuctionListing.objects.get(pk=list_id)
        if Bid.objects.filter(auction=list_id).exists():
            check = True
            bids = Bid.objects.filter(auction=list_id)
            maxBid = maksimum_bid(bids)
        else: 
            check = False 
            maxBid = 0
        if check == False: 
            maxBid = float(request.POST['value'])
            users = User.objects.get(username=request.user)
            bid = Bid(value=float(request.POST['value']),user=users,auction=list_id)
            bid.save()
            data_bid = Bid.objects.get(value=maxBid,auction=list_id)
            print(data_bid)
            auction.bid = data_bid
            auction.save()
        else: 
            if float(request.POST['value']) > maxBid:
                users = User.objects.get(username=request.user)
                bid = Bid(value=float(request.POST['value']),user=users,auction=list_id)
                bid.save()
                data_bid = Bid.objects.get(value=request.POST['value'],auction=list_id)
                auction.bid = data_bid
                auction.save()
        return HttpResponseRedirect(reverse('listingPage', args=(list_id, )))
    else: 
        new_bid = BidForm()
        if Bid.objects.filter(auction=list_id).exists():
            bid  = Bid.objects.filter(auction=list_id)
            max_bid = 0
            for value in bid:
                if value.value>max_bid:
                    max_bid = value.value
                    winner = value.user
        else: 
            max_bid = 0
            winner = None
        if request.user.is_authenticated:
            user = User.objects.get(username=request.user)
        else: 
            item = AuctionListing.objects.get(pk=list_id)
            comments = item.comments.all()
            return render(request,'auctions/ListingPage.html', {
            'item': item,
            'comments': comments,
        })
        item = AuctionListing.objects.get(pk=list_id)
        if item.creator == user: 
            creator =  True 
        else: 
            creator = False 
        bid = max_bid
        # winner to string for better template rendering with capitalised first letter
        winner_str = str(winner)
        winner_str = winner_str[0].upper()+winner_str[1:]
        form_2 = CommentsForm()
        comments = item.comments.all()
        print(comments)
        return render(request,'auctions/ListingPage.html', {
            'item': item,
            'new_bid': new_bid,
            'bid': max_bid,
            'winner': winner_str,
            'creator': creator,
            'open': item.open,
            'contentForm': form_2,
            'comments': comments,
    })

@login_required()
def watchlist(request,auction_id):
    if request.method == 'POST': 
        auction = AuctionListing.objects.get(pk=auction_id)
        user = User.objects.get(username=request.user)
        if Watchlist.objects.filter(user=user.id).exists():
            watchlist = Watchlist.objects.get(user=user.id)
            watchlist.auctions.add(auction)
        else: 
            watchlist = Watchlist(user=user)
            watchlist.save()
            watchlist.auctions.add(auction)
        return HttpResponseRedirect(reverse('listingPage',args=(auction_id,)))
    else:
        user = User.objects.get(username=request.user)
        if Watchlist.objects.filter(user=user.id).exists():
            watchlist = Watchlist.objects.get(user=user.id)
            print(watchlist.auctions)
            auctions = watchlist.auctions.all()
            bids = {}
            for auction in auctions: 
                if Bid.objects.filter(auction=auction.id):
                    bid = Bid.objects.filter(auction=auction.id)
                    bid = maksimum_bid(bid)
                    bids[auction]=bid 
                else: 
                    bids[auction]=False 
            return render(request,'auctions/watchlist.html',{
                'auctions': bids,
                'USER': str(user.username).capitalize(),
                
            }) 
        else: 
            bids = {}
            return render(request,'auctions/watchlist.html',{
                'auctions': bids,
                'USER': str(user.username).capitalize(),
            }) 
@login_required()
def delete(request,id):
    if request.method=='POST':
        auction = AuctionListing.objects.get(pk=id)
        user = User.objects.get(username=request.user)
        watchlist = Watchlist.objects.get(user=user.id)
        watchlist.auctions.remove(auction)
        # watchlist.auctions_set.all
        return HttpResponseRedirect(reverse('watchlist',args=(user.id, )))

@login_required()
def close(request,id):
    if request.method == 'POST': 
        auction = AuctionListing.objects.get(pk=id)
        auction.open = False 
        auction.save()
        return HttpResponseRedirect(reverse('listingPage',args=(id, )))

@login_required()
def comments(request,id):
    if request.method == "POST":
        user = User.objects.get(username=request.user) 
        comment_temp = CommentsForm(request.POST)
        comment = comment_temp.save()
        comment.author = user 
        comment.save()
        comment = Comments.objects.filter(author = request.user).last()
        auction = AuctionListing.objects.get(pk=id)
        auction.comments.add(comment)
        return HttpResponseRedirect(reverse('listingPage', args=(id, )))
