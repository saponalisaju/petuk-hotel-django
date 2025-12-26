
from django.contrib import admin
from django.urls import path, include

from django.conf.urls.i18n import i18n_patterns


from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('core.urls', 'core'), namespace='core')),
    path('blog/', include(('blog.urls', 'blog'), namespace='blog')),
    path('user/', include(('userauths.urls', 'userauths'), namespace='userauths')),
    path("ckeditor5/", include("django_ckeditor_5.urls")),
    path('i18n/', include('django.conf.urls.i18n')),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


### TEST ###

# handler404 = 'core.views.error_404'
# handler500 = 'core.views.error_500'