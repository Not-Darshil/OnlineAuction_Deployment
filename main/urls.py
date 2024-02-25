from django.contrib import admin
from django.urls import path, include
##ADDED MANUALLY
from django.conf import settings
from django.conf.urls.static import static
from myapp import views
admin.site.site_header='Auction Admin Panel'
# admin.site.site_title='Auction Admin Portal Server' ## do not know what the fuck this line is doing
admin.site.index_title='Welcome to Auction Admin Panel'
# admin.site.index_template='Auction Admin Panel3'


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('',views.home), ##yeh bhadia h
    path('',include('myapp.urls'))
 
    
] 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
urlpatterns +=  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 
