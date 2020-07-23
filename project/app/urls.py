from django.contrib import admin
from django.urls import path,include
from app import views

urlpatterns = [
    path('',views.index,name='index'),
    path('about',views.about,name='about'),
    path('contact',views.contact,name='contact'),
    path('handleBlog',views.handleBlog,name='handleBlog'),
    path('handleFriendsBlog',views.friends,name='friends'),
    path('signup',views.handleSignup,name='handleSignup'),
    path('login',views.handleLogin,name='handleLogin'),
    path('handleLogout',views.handleLogout,name='handleLogout'),
    path('search',views.search,name="search"),
]

