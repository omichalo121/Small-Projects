from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField('Listing', related_name="watchers", blank=True)

class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    price = models.FloatField()
    active = models.CharField(max_length=1, default='Y')
    img = models.CharField(max_length=255)
    added = models.DateTimeField(auto_now_add=True)
    expires = models.DateTimeField()
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listed_items")
    description = models.TextField()
    winner = models.CharField(max_length=50, default='null')
    CATEGORY_CHOICES = [
         ('N', 'None'),
         ('AN', 'Animal'),
         ('HS', 'House'),
         ('S', 'Sport'),
         ('HB', 'Hobby'),
         ('E', 'Electronics'),
         ('F', 'Food'),
         ('A', 'Art'),
         ('AM', 'Automobile'),
    ]
    category = models.CharField(max_length=13, choices=CATEGORY_CHOICES, default='N')

class Bid(models.Model):
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    amount = models.FloatField()
    lost = models.CharField(max_length=1, default='N')
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids_placed")
    timestamp = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=500)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    OPINION_CHOICES = [
        ('P', 'POSITIVE'),
        ('N', 'NEGATIVE'),
        ('NE', 'NEUTRAL'),
    ]
    opinion = models.CharField(max_length=2, choices=OPINION_CHOICES, default='NE')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments", default=None, null=True)