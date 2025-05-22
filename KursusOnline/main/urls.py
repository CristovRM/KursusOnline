from . import views
from django.urls import path

urlpatterns = [
    path("", views.home, name="home"),
    path("login", views.login, name="login"),
    path("course", views.course, name="course"),
    path("about", views.about, name="about"),
    path("contact", views.contact, name="contact"),
    path("my-courses", views.mycourse, name="mycourse"),
    path("my-courses1", views.mycourse1, name="mycourse1"),
    
    # Admin
    path('login-admin', views.login_admin, name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-logout/', views.logout_admin, name='logout_admin'),
]