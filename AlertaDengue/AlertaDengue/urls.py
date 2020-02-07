from django.urls import include, path, re_path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

admin.autodiscover()

# see https://docs.djangoproject.com/en/3.0/ref/urls/
urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^accounts/profile/$', RedirectView.as_view(url="/")),
    re_path(r'^accounts/', include('django.contrib.auth.urls')),
    # apps
    path(r'', include('dados.urls')),
    re_path(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    re_path(r'^dbf/', include('dbf.urls')),
    re_path(r'^api/', include('api.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
