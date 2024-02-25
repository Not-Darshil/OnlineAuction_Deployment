from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseBadRequest
from django.urls import reverse
from django.db import IntegrityError

#authentication models and functions
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages

from .decorators import user_not_authenticated

#for authenticating through email
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage,EmailMultiAlternatives
from .tokens import account_activation_token

#for main components
from datetime import datetime
from django.utils.timezone import now   
from . forms import UserRegistrationForm, LoginForm, CreateListingForm,BiddingForm, CommentForm
from .models import User, Product,Bidding,Watchlist,Closebid,Comment #, Category



# Create your views here.

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('/my_login')
    else:
        messages.error(request, 'Activation link is invalid!')
    
    return redirect('/my_login')


def activateEmail(request, user, to_email,login_url):
    mail_subject = 'Activate your user account.'
    html_message=render_to_string('mails/template_activate_account.html',
                                  {
                                    'user': user.username,
                                    'domain': get_current_site(request).domain,
                                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                    'token': account_activation_token.make_token(user),
                                    'protocol': 'https' if request.is_secure() else 'http',
                                    'login_url': login_url
                                  })
    plain_message=strip_tags(html_message)
    message = EmailMultiAlternatives(
        subject=mail_subject,
        from_email=None,
        to=[to_email],
        body=plain_message,
    )

    message.attach_alternative(html_message,"text/html")
    message.send()
    sendEmailWelcome(request,to_email)

def sendEmailtoWinner(request, user, to_email,details):
    mail_subject='Congratulations! Your Bid Has Been Successful'
    html_message=render_to_string('mails/template_winner.html',
                                {
                                    'user': user.username,
                                    'pimage': details[0],
                                    'pname': details[1],
                                    'pdesc': details[2],
                                    'pbrand': details[3],
                                    'pprice': details[4]
                                })
    plain_message=strip_tags(html_message)
    message = EmailMultiAlternatives(
        subject=mail_subject,
        from_email=None,
        to=[to_email],
        body=plain_message,
    )

    message.attach_alternative(html_message,"text/html")
    message.send()
    
def sendEmailWelcome(request, to_email):
    mail_subject='Welcome to AuctionWave - Where Bids Come True!'
    html_message=render_to_string('mails/template_welcome.html')
    plain_message=strip_tags(html_message)
    message = EmailMultiAlternatives(
        subject=mail_subject,
        from_email=None,
        to=[to_email],
        body=plain_message,
    )
    message.attach_alternative(html_message,"text/html")
    message.send()

    





def home(request):
    return render(request,'myapp/home.html')

def pricing(request):
    return render(request,'myapp/homeComponents/pricing.html')

def about(request):
    return render(request,'myapp/homeComponents/about.html')

def contact(request):
    return render(request,'myapp/homeComponents/contact.html')

def listings(request):
    products = Product.objects.all() 
    return render(request,'myapp/homeComponents/listings.html', {
        'object': products},)

def homepage(request):
    # return HttpResponse("request")
    return render(request,'myapp/homepage.html')



@user_not_authenticated 
# def register(request):
#     if request.method == "POST":
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = False
#             user.save()
#             activateEmail(request, user, form.cleaned_data.get('email'))

#             return redirect('my_login')

#         else:
#             for error in list(form.errors.values()):
#                 messages.error(request, error)

#     else:
#         form = UserRegistrationForm()

#     return render(
#         request=request,
#         template_name="myapp/register.html",
#         # template_name="users/register.html",
#         context={"UserRegistrationForm": form}
#         )



def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # Use the reverse function to get the URL for 'my_login'
            my_login_url = reverse('my_login')
            activateEmail(request, user, form.cleaned_data.get('email'),my_login_url)

            messages.success(request, 'Account created successfully. Please check your email for activation instructions.')

            return redirect('/checkmail')

        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    else:
        form = UserRegistrationForm()

    return render(
        request=request,
        template_name="myapp/register.html",  # Update with your correct template path
        context={"UserRegistrationForm": form}
    )

def checkmail(request):
    return render(request,'myapp/checkmail.html')

def my_login(request):
    form=LoginForm()
    if request.method == 'POST':
        form = LoginForm(request,data=request.POST)
        if form.is_valid():
            username=request.POST.get('username')
            password=request.POST.get('password')

            user=authenticate(request,username=username,password=password)

            if user is not None:
                auth.login(request,user)
                return redirect ("dashboard")
    context={'loginform':form}

    return render(request,'myapp/my_login.html',context=context)


def logout(request):
    if request.method == 'POST':
        auth.logout(request)    
        return redirect ("/my_login")
    return render(request,'myapp/logout.html')
    # return redirect("")


@login_required(login_url="my_login") # for protecting the view of dashboard called as csrf protection
def dashboard(request):
    products = Product.objects.all() 
    return render(request,'myapp/dashboard.html', {
        'object': products},)


@login_required(login_url="my_login")
def create(request):
    creator = Product.objects.all()
    form = CreateListingForm(request.POST, request.FILES)
    try:
        watch = Watchlist.objects.filter(watcher=request.user.username)
        watchcount = len(watch)
    except:
        watchcount = None
    if request.method == "POST":
        if form.is_valid():
            now = datetime.now()
            new_product = form.save(commit=False)
            new_product.lister = request.user
            new_product.date = now
            new_product.save()
            messages.success(request, 'Product created successfully.')
            # return redirect("/dashboard")
        return HttpResponseRedirect(reverse('dashboard'))
    else:
            return render(request, 'myapp/mainComponents/create.html', {
                'form': form,
                'creator': creator,
                'watchcount': watchcount
            })





@login_required(login_url="my_login")
def listingpage(request,id):
    listing = Product.objects.get(id=id)
    comment = Comment.objects.filter(listingid=id)
    try:
        cform = CommentForm(request.POST or None)
        bidform = BiddingForm(request.POST or None)
    except:
        return redirect('dashboard')
    if request.user.username:

        try:
            if Watchlist.objects.get(watcher=request.user.username, listingid=id):#will give eroror
                added=True
        except:
            added = False

        try:
            watch = Watchlist.objects.filter(watcher=request.user.username)
            watchcount=len(watch)
        except:
            watchcount=None

        try:
            ccount = Comment.objects.filter(listingid=id)
            ccount = len(ccount)
        except:
            ccount = len(ccount)

        try:

            if listing.lister == request.user.username :
                lister = True
            else:
                lister = False
        except:
            return redirect('/dashboard')
    else: 
        ccount = Comment.objects.filter(listingid=id)
        ccount = len(ccount)
        added = False
        lister = False
        watchcount = None
    try:
        bid = Bidding.objects.filter(listingid=id)
        bidcount = len(bid)
        listing = Product.objects.get(listingid=id)
    except:
        bidcount = None
    print("image",listing.image)
    return render(request, "myapp/mainComponents/listing.html", {
        'object': listing,
        'added': added,
        'bidform': bidform,
        "watchcount": watchcount,
        "error":request.COOKIES.get('error'),
        "success":request.COOKIES.get('success'),
        "bidcount": bidcount,
        "lister": lister,
        'cform': cform,
        "comment": comment,
        "ccount": ccount
    })

@login_required(login_url="my_login")
def addwatch(request, id):
    if request.user.username:
        Product = Product.objects.get(id=id)
        watchers = Watchlist(watcher = request.user.username, listingid = id)
        watchers.lister = Product.lister
        watchers.finalbid = Product.startingbids
        watchers.name = Product.name
        watchers.image = Product.image
        watchers.save()
        return redirect('listingpage', id=id)
    else:
        return redirect('/dashboard')


@login_required(login_url="my_login")
def removewatch(request,id):
    if request.user.username:
        try:
            Watchlist.objects.filter(listingid=id).delete()
            return redirect('listingpage', id=id)
        except:
            return redirect('listingpage', id=id)
    else:
        return redirect('/dashboard')


@login_required(login_url="my_login")
def watchlist(request):
    try:
        watchlist = Watchlist.objects.filter(watcher=request.user.username)
        closebid = Closebid.objects.filter(bidder=request.user.username)
        watchcount = len(watchlist)                                                 #count how many rows in table Watchlist using len()                                    
    except:
        watchcount = None


    try:
        bidwincount = Closebid.objects.filter(bidder = request.user.username)
        bidwincount = len(bidwincount)
    except:
        bidwincount = None


    try:
        if Watchlist.objects.get(listingid=id): #will throw error here
            closed = True
        else:
            closed = False
    except:
        closed = False

        
    return render(request, "'myapp/mainComponents/watchlist.html'", {
        'object': watchlist,
        "watchcount": watchcount,
        "closedbid": closebid,
        "closed" : closed,
        "bidwincount": bidwincount
    })



@login_required(login_url="my_login")
def bid(request, listingid):
    current = Product.objects.get(id=listingid)
    current = current.start_bid
    bidform = BiddingForm(request.POST or None)
    if request.user.username:
        bid = float(request.POST.get("bidprice"))
        if bid > current:
            listing = Product.objects.get(id=listingid)
            listing.start_bid = bid
            listing.save()
            try:
                if  Bidding.objects.filter(id=listingid):
                    bidrow = Bidding.objects.filter(id=listingid)
                    bidrow.delete()
                fs = bidform.save(commit=False) 
                fs.bidder = request.user.username
                fs.bidemail = request.user.email
                fs.listingid = listingid
                fs.save()                                                      
            except:
                fs = bidform.save(commit=False)
                fs.bidder = request.user
                fs.bidemail = request.user.email
                fs.listingid = listingid
                fs.save()   
            response = redirect('listingpage', id=listingid)
            response.set_cookie('success','Successful Bid! Your bid is currently the highest bid.', max_age=1)
            return response
        else:
            response = redirect('listingpage', id=listingid)
            response.set_cookie('error','Your bid must be higher than the current price!', max_age=1)
            return response
    else:
        return redirect('/dashboard')
        


@login_required(login_url="my_login")
def closebid(request, listingid):
    if request.user.username:
        try:
            listing = Product.objects.get(id=listingid)
        except:
            return redirect('/dashboard')
        closebid = Closebid()
        name = listing.name
        closebid.lister = listing.lister
        closebid.listingid = listingid
        closebid.productnames = listing.name
        closebid.images = listing.image
        brand=listing.brand
        description=listing.description

        # closebid.category = listing.category
        try:
            bid = Bidding.objects.get(listingid=listingid,bidprice=listing.start_bid)
            closebid.bidemail=bid.bidemail
            closebid.bidder = bid.bidder
            closebid.finalbid = bid.bidprice
            closebid.save()
            bid.delete()
        except:
            closebid.bidder = listing.lister
            closebid.finalbid = listing.start_bid
            closebid.save()
        try:
            if Watchlist.objects.filter(listingid=listingid):
                watch = Watchlist.objects.filter(listingid=listingid)
                watch.delete()
            else:
                pass
        except:
            pass
        try:
            comment = Comment.objects.filter(listingid=listingid)
            comment.delete()
        except:
            pass
        try:
            bid = bid.objects.filter(listingid=listingid)
            bid.delete()
        except:
            pass
        try:
            closebidlist = Closebid.objects.get(listingid=listingid)
        except:
            closebid.lister = listing.lister
            closebid.bidder = listing.lister
            closebid.listingid = listingid
            description=listing.description
            brand=listing.brand
            closebid.finalbid = listing.start_bid
            closebid.productnames = listing.name
            closebid.images = listing.image
            # closebid.category = listing.category
            closebid.save()
            closebidlist = Closebid.objects.get(listingid=listingid)
        listing.delete()
        try:
            watch = Watchlist.objects.filter(watcher=request.user.username)
            watchcount=len(watch)
        except:
            watchcount = None
        detailslist=[closebid.images,closebid.productnames,description,brand,float(closebid.finalbid)]
        print(detailslist)
        sendEmailtoWinner(request,request.user,closebid.bidemail,detailslist)
        return render(request,"myapp/mainComponents/winner.html",{
            "closebidlist": closebidlist,
            "name": name,
            "watchcount":watchcount
        })   
    else:
        return redirect('/dashboard')

@login_required(login_url="my_login")
def closed(request, listingid):
    closed = Closebid.objects.get(listingid=listingid)
    try:
        watch = Watchlist.objects.filter(watcher=request.user.username)
        watchcount = len(watch)
    except:
        watchcount = None
    return render(request, "myapp/mainComponents/closed.html", {
        "object": closed,
        "watchcount": watchcount
    })








@login_required(login_url="my_login")
def comment(request, listingid):
    if request.method == "POST":
        comment = Comment.objects.all()
        cform = CommentForm(request.POST or None)
        if cform.is_valid():
            now = datetime.now()                                               
            fs = cform.save(commit=False)   
            fs.listingid = listingid
            fs.user = request.user.username                               
            fs.time = now
            fs.save()
        return redirect('listingpage', id=listingid)
    else:
        return redirect('/dashboard') 

# def category(request):
#     category = Category.objects.all()
#     closedbid = Closebid.objects.all()
#     try:
#         if Watchlist.objects.get(listingid=id):#may give error may use Watchlist.listingid or any third vraiable
#             closed = True
#         else:
#             closed = False
#     except:
#         closed = False
#     try:
#         watch = Watchlist.objects.filter(watcher=request.user.username)
#         watchcount = len(watch)
#     except:
#         watchcount = None
#     return render(request, "myapp/mainComponents/categories.html", {
#         "object": category,
#         "watchcount": watchcount,
#         "closed": closed,
#         "closedbid": closedbid
#     })

# def categorylistings(request, cats):
#     category_posts = Product.objects.filter(category=cats)
#     try:
#         watch = Watchlist.objects.filter(watcher=request.user.username)
#         watchcount = len(watch)
#     except:
#         watchcount = None
#     return render(request, "myapp/mainComponents/categorylistings.html", {
#         'cats': cats,
#         'category_posts': category_posts,
#         'watchcount': watchcount
#     })


def allclosed(request):
    closedlist = Closebid.objects.all()
    try:
        watch = Watchlist.objects.filter(watcher=request.user.username)
        watchcount = len(watch)
    except:
        watchcount = None
    return render(request, "myapp/mainComponents/allclosed.html", {
        'closedlist': closedlist,
        'watchcount': watchcount
    })





