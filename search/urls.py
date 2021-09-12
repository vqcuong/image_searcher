from re import search
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/pool', views.image_pool),
    path('api/fetch', views.image_pool_detail),
    path('api/search', views.search_image)
]
