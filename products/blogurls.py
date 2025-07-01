from django.urls import path , include
from . import views
from django.contrib import admin

urlpatterns = [
    path('',views.blog,name='blog'),
]