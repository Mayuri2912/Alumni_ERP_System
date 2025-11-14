# alumni_portal/urls.py
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Send all "accounts/" URLs to the accounts app
    path('accounts/', include('accounts.urls')),
    
    # Send all "portal/" URLs to the portal app
    path('portal/', include('portal.urls')),

    # Make the root URL redirect to the login/signup page
    path('', lambda r: redirect('login_signup'), name='root'),
]