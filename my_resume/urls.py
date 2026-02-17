from django.urls import path
from . import views

urlpatterns = [
    path('', views.CreateResumeView.as_view(), name='create_resume'),
]