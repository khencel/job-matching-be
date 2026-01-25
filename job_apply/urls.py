from django.urls import path
from . import views

urlpatterns = [
    path('', views.JobApplyView.as_view(), name='apply_job'),
    path('status', views.ApplyChangeStatus.as_view(), name='apply_change_status'),
    path('applicant', views.ApplyJobSeekerApplicant.as_view(), name='apply_job_seeker_applicant')
]