from django.urls import path
from . import views

urlpatterns = [

    # path('', views.home, name='home'),

    path('register/', views.register, name='register'),
    path('api/hospitals/', views.get_hospitals_by_district),

]