from django.urls import path
from . import views

urlpatterns = [
   path('', views.JobSearchListCreate.as_view()),
   path('send-file-to-email', views.SendFileEmail.as_view()),
]