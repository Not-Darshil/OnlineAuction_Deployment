from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User



# class Category(models.Model):
#     name = models.CharField(
#         max_length=20,
#         choices=[
#             ('fashion', 'Fashion'),
#             ('toys', 'Toys'),
#             ('electronics', 'Electronics'),
#             ('home', 'Home'),
#             ('sports', 'Sports'),
#             ('pets', 'Pets'),
#             ('baby', 'Baby'),
#             ('grocery', 'Grocery'),
#             ('entertainment', 'Entertainment'),
#             ('other', 'Other'),
#         ],
#         unique=True,null=False  # Ensure each category name is unique
#     )

#     def __str__(self):
#         return self.name




class Product(models.Model):#changed
    name=models.CharField(max_length=256,null=False)#changed
    brand=models.CharField(max_length=256,null=True, default="")
    # category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    description=models.CharField(max_length=512,default="",null=True)
    start_bid=models.DecimalField(max_digits=10, decimal_places=2)
    image=models.ImageField(upload_to='myapp/images',null=False)
    lister=models.ForeignKey(User, on_delete=models.CASCADE,null=False)
    date=models.DateField(default=now, editable=False)

    def __str__(self):
        return self.name



class Bidding(models.Model):
    bidder = models.CharField(max_length=50, blank=True, null=True)
    bidemail= models.EmailField(default="abesit.darshil@gmail.com")
    bidprice = models.DecimalField(max_digits=15, decimal_places=2)
    listingid = models.IntegerField()

    def __str__(self):
        return f"{self.listingid}"
    
class Watchlist(models.Model):
    name = models.CharField(max_length=20)#changed
    image = models.URLField(blank=True, null=True)#changed
    finalbid = models.DecimalField(max_digits=15, decimal_places=2)
    lister = models.CharField(max_length=50, blank=True, null=True)
    watcher = models.CharField(max_length=50, blank=True, null=True)
    listingid = models.IntegerField()

    def __str__(self):
        return f"{self.listingid}"
    
class Closebid(models.Model):
    name = models.CharField(max_length=20)
    brand=models.CharField(max_length=256,null=True, default="")
    description=models.CharField(max_length=512,default="",null=True)
    image = models.URLField(blank=True, null=True)
    lister = models.CharField(max_length=64, blank=True, null=True)
    bidemail= models.EmailField(default="abesit.darshil@gmail.com")
    bidder = models.CharField(max_length=64, blank=True, null=True)
    listingid = models.IntegerField()
    # category = models.CharField(max_length=50, blank=True, null=True)
    finalbid = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.listingid}"
    
class Comment(models.Model):
    user = models.CharField(max_length=64, blank=True, null=True)
    time = models.DateTimeField(default=now, editable=False)
    comment = models.CharField(max_length=30)
    listingid = models.IntegerField()

    def __str__(self):
        return f"{self.listingid}"


