from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.JobPostCreateView.as_view(), name='create_jobpost'),
    path('list/<str:user_id>', views.JobPostListView.as_view(), name='list_jobpost'),
    path('delete/<int:pk>', views.DeleteJobPostView.as_view(), name='delete_jobpost'),
    path('list', views.JobPostListAllView.as_view(), name='list_all_jobpost')
]