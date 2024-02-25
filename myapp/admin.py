from django.contrib import admin

# Register your models here.
from .models import Product,Bidding,Watchlist,Closebid,Comment

# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display=['name','brand','start_bid','lister','image','date']



class ProductAdmin(admin.ModelAdmin):
    list_display = ("__str__", "name")

class BiddingAdmin(admin.ModelAdmin):
    list_display = ("__str__", "bidprice")

class WatchlistAdmin(admin.ModelAdmin):
    list_display = ("__str__", "watcher")

class ClosebidAdmin(admin.ModelAdmin):
    list_display = ("__str__", "lister")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("__str__", "user")
    
admin.site.register(Product, ProductAdmin)
admin.site.register(Bidding, BiddingAdmin)
admin.site.register(Watchlist, WatchlistAdmin)
admin.site.register(Closebid, ClosebidAdmin)
admin.site.register(Comment, CommentAdmin)

