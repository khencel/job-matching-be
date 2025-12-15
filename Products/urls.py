from django.urls import path
from . import views

urlpatterns = [
    path('create', views.ProductListCreate.as_view(), name='create'),
    path('index', views.ProductListCreate.as_view(), name='index'),
]