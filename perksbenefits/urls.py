from django.urls import path
from . import views

urlpatterns = [
   path('', views.PerksBenefitsListCreate.as_view()),
   path('<int:pk>/', views.PerksBenefitsRetrieveUpdateDestroy.as_view())
]