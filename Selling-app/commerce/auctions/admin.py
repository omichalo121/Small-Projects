from django.contrib import admin
from .models import Listing, Bid, Comment
# Register your models here.

class ListingAdmin(admin.ModelAdmin):
    list_display = ("title", "id", "seller", "active", "category", "price", "added")

class BidAdmin(admin.ModelAdmin):
    list_display = ("title", "item_id", "bidder", "amount", "timestamp")

    def title(self, obj):
        return obj.item.title
    def item_id(self, obj):
        return obj.item.id

class CommentAdmin(admin.ModelAdmin):
    list_display = ("title", "item_id", "comment", "opinion", "author", "upvotes", "downvotes")

    def title(self, obj):
        return obj.listing.title
    def item_id(self, obj):
        return obj.listing.id

admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)