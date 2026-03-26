from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
    
    # This line gives you 'login' and 'logout' automatically
    path('accounts/', include('django.contrib.auth.urls')), 
]