from django.contrib import admin
from django.urls import path, include
from .views import *

app_name = 'blog'

urlpatterns = [
    path('aboutus/', about, name='about'),
    path('', index, name='index'),
    path('tag/<tag_slug>', index, name='index-tag'),
    path('search/', post_search, name='search'),
    path('<slug:slug>/', post_detail, name='post_detail'),
    # path('<int:post_id>/share/', post_share, name='share'),

]
