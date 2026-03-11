from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # allauth URLs
    path('accounts/', include('allauth.urls')),

    # app URLs
    path('', include('registration.urls')),
]