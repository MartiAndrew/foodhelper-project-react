from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

DEFAULT_VERSION = 'v1'


schema_view = get_schema_view(
    openapi.Info(
        title='Foodhelper',
        default_version=DEFAULT_VERSION,
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path(f'api/{DEFAULT_VERSION}/', include('api.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(
            r'^swagger/$',
            schema_view.with_ui('swagger', cache_timeout=0),
            name='schema-swagger-ui',
        ),
        path('redoc/',
             TemplateView.as_view(template_name='redoc.html'),
             name='redoc'),
    ]
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)
