from django.urls import path
from . import views


urlpatterns = [
    path('login',views.login),
    path('logout',views.logout),
    path('signin',views.signin),
    path('',views.login),
    path('home',views.home),

]
