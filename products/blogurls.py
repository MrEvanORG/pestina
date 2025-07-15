from django.urls import path
from . import blogviews

urlpatterns = [
    path('',blogviews.blog_index,name='blog'), #show main page of weblog and categories
    path('<str:category_slug>/',blogviews.blog_category,name='blog_category'), #show posts of a category 
    path('<str:category_slug>/<str:post_slug>/',blogviews.blog_post_detail,name='blog_post_detail'), # show a post
]