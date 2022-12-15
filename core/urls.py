from unicodedata import name
from django.contrib import admin
from django.urls import path, include  # add this


urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),          # Django admin route
    path("", include("apps.authentication.urls")),          # Auth routes - login / register
    path("", include("apps.inneye.urls")),
]
