from django.contrib import admin
from django.urls import path,include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls')),
]


urlpatterns += staticfiles_urlpatterns()


# postgres://hrms_3qph_user:JpCG64DnRfhtOiJXSACBv6tR7e7WOsJd@dpg-coe0ar8l6cac73brndp0-a.oregon-postgres.render.com/hrms_3qph