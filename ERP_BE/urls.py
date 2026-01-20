
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('userauth.urls')),
    path('api/product/', include('Products.urls')),
    path('api/job/', include('post_a_job.urls')),
    path('api/perks/', include('perksbenefits.urls')),
    path('api/apply/', include('job_apply.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)