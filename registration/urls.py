from django.urls import path
from . import views

urlpatterns = [

    path('', views.landing, name='landing'),
    path('register/', views.register, name='register'),
    path('api/hospitals/', views.get_hospitals_by_district),
    path('stats/',views.stats,name="stats"),
    path("export/", views.export_all_registrations, name="export_data"),
    path("api/live/", views.live_registrations),
    path("monitor/", views.monitor, name="monitor"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("login/", views.login_page, name="login"),
    path("email-login/", views.email_login, name="email_login"),
]