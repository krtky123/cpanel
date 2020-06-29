from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('signin/', views.signin),
    path('logout/', views.logout, name="logout"),
    path('signup/', views.signup, name="signup"),
]
