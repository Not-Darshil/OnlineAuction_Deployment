#created this file manually
from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #Home Components
    path('',views.home,name=''),
    path('homepage',views.homepage,name='homepage'),
    path('pricing',views.pricing,name='pricing'),
    path('about',views.about,name='about'),
    path('listings',views.listings,name='listings'),
    #User Components
    path('register',views.register,name='register'),
    path('checkmail',views.checkmail,name='checkmail'),
    path('my_login',views.my_login,name='my_login'),
    path('logout',views.logout,name='logout'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    #Main Components
    path('dashboard',views.dashboard,name='dashboard'),
    path('create',views.create,name='create'),
    # path('profile/<username>', views.profile, name='profile'),
     
        #FOR sub-main components
    path("listing/<int:id>", views.listingpage, name="listingpage"),
    path("listing/<int:id>/addwatch",views.addwatch,name="addwatch"),
    path("listing/<int:id>/removewatch",views.removewatch,name="removewatch"),
    path("listing/<int:listingid>/bid",views.bid,name="bid"),
    path("listing/<int:listingid>/closebid",views.closebid,name="closebid"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("listing/<int:listingid>/closed", views.closed, name='closed'),
    #FOR extra features
    path("comment/<int:listingid>", views.comment, name="comment"),
    # path("category", views.category, name="category"),
    # path("category/<str:cats>", views.categorylistings, name="categorylistings"),   
    path("listing/closed", views.allclosed, name="allclosed"),






]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)