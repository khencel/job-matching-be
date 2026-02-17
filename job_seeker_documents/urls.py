from django.urls import path
from . import views

urlpatterns = [
    path('', views.CreateDocuments.as_view())
]