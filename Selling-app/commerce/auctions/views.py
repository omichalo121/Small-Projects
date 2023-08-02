from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import User, Listing, Bid, Comment
from datetime import datetime, timedelta

def index(request):
    listings = Listing.objects.filter(active='Y').all()
    return render(request, "auctions/index.html", {
        "listings": listings
    })

def archive (request):
    listings = Listing.objects.filter(active='N').all()
    return render(request, "auctions/index.html", {
        "listings": listings
    })

def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Listing.CATEGORY_CHOICES
    })

def category(request, search):
    for pair in Listing.CATEGORY_CHOICES:
        if search in pair:
            search = pair[0]
            if not Listing.objects.filter(category=search):
                search = pair[1]

    return render(request, "auctions/categories.html", {
        "listings": Listing.objects.filter(category=search, active='Y'),
        "categories": Listing.CATEGORY_CHOICES
    })

@login_required
def watchlist(request):
    user = request.user
    watchlist = user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "listings": watchlist
    })

@login_required
def auctions(request):
        bids = Bid.objects.filter(bidder=request.user)
        items = Listing.objects.filter(bids__in=bids).distinct()
        show = bids.count()
        pack = zip(bids, items)
        return render(request, "auctions/user_bids.html", {
            "pack": pack,
            "show": show
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

def create_listing(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))

    if request.method == "GET":
        return render(request, "auctions/create.html", {
            "categories": Listing.CATEGORY_CHOICES
        })
    else:
        title = request.POST["title"]
        price = float(request.POST["price"])
        description = request.POST["description"]
        time = int(request.POST["days"])
        img = request.POST.get("img")
        category = request.POST.get("category")
        check = 0
        for pair in Listing.CATEGORY_CHOICES:
            if category == pair[0]:
                check = 1
        if check == 0:
            category = 'N'

        expiration_date = datetime.now() + timedelta(days=time)

        listing = Listing(title=title, price=price, description=description, img=img, category=category, added=datetime.now(), expires=expiration_date, seller=request.user)
        listing.save()
        return HttpResponseRedirect(reverse("index"))

def listing(request, id):
    listing = get_object_or_404(Listing, id=id)
    bids = listing.bids.all().order_by('-timestamp')
    comments = listing.comments.all().order_by('-date')
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "bids": bids,
        "choices": Comment.OPINION_CHOICES,
        "comments": comments
    })

def watch(request):
    if request.method == "POST" and request.user.is_authenticated:
        listing = Listing.objects.get(pk=request.POST["listing_id"])
        user = request.user
        watchlist = user.watchlist.all()
        print(watchlist)
        if listing not in watchlist:
            user.watchlist.add(listing)
        else:
            user.watchlist.remove(listing)
        return redirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(reverse("index"))

def bid(request):
    if request.method == "POST" and request.user.is_authenticated:
        price = request.POST["bid"]
        id = request.POST["listing"]
        listing = get_object_or_404(Listing, pk=id)
        listing.price = float(price)
        listing.save()
        previous_bids = Bid.objects.filter(item=listing, lost='N')
        if previous_bids:
            previous_bids.update(lost='Y')

        bid = Bid.objects.filter(bidder=request.user, item=listing)
        if bid:
            bid.update(timestamp=datetime.now(), amount=price, lost='N')
        else:
            Bid.objects.create(item=listing, amount=price, bidder=request.user, timestamp=datetime.now())
        return redirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(reverse("index"))

def delete(request):
    if request.method == "POST" and request.user.is_authenticated:
        user = request.user
        listing = Listing.objects.get(pk=request.POST["id"])
        if listing.seller == user:
            listing.active = 'N'
            listing.winner = Bid.objects.filter(item=listing).order_by('-amount').first().bidder.username
            listing.save()
            return redirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(reverse("index"))

def comment(request):
    if request.method == "POST" and request.user.is_authenticated:
        user = request.user
        listing = Listing.objects.get(pk=request.POST["id"])
        comment = Comment.objects.create(author=user, comment=request.POST["text"], opinion=request.POST["opinion"], date=datetime.now())
        listing.comments.add(comment)
        return redirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(reverse("index"))