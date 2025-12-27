
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('userauth.urls')),
    path('api/product/', include('Products.urls')),
    path('api/job/', include('post_a_job.urls'))
]
