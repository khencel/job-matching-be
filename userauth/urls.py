from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    # path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login', views.EmailTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify', TokenVerifyView.as_view(), name='token_verify'),
    path('test', views.ProtectedView.as_view(), name='test_view'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('get-data', views.GetData.as_view(), name='getData'),
    
    path('get-all-user/', views.ListCreate.as_view(), name='index'),
    path('store', views.ListCreate.as_view(), name='store'),
    path('user/<int:pk>', views.UserRetrieveUpdateDestroyView.as_view(), name='update'),
    
    path('add-super-admin', views.AddSuperAdmin.as_view(), name='add_super_admin'),
    path("verify-email/<uuid:token>/", views.VerifyEmail.as_view()),
    
    path('test-translate', views.TestTranslate.as_view(), name='test_translate'),
]