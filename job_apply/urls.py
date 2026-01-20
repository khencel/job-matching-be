from django.urls import path
from . import views

urlpatterns = [
    path('', views.JobApplyView.as_view(), name='apply_job'),
]