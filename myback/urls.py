from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404, handler500
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView


handler404 = "posts.views.page_not_found"
handler500 = "posts.views.server_error"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("users.urls")),
    path("api/v1/", include("api.urls")),
    path('redoc/', TemplateView.as_view(template_name='redoc.html'), name='redoc'),
    path("", include("posts.urls")),
    path("auth/", include("django.contrib.auth.urls")),
    path("about/", include("about.urls")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
