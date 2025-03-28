"""
URL configuration for volunteerhub project.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('accounts/', include('accounts.urls')),
    path('events/', include('events.urls')),
    path('feedback/', include('feedback.urls')),
]

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Customize admin titles
admin.site.site_header = 'VolunteerHub Administration'
admin.site.site_title = 'VolunteerHub Admin'
admin.site.index_title = 'Welcome to VolunteerHub Admin Panel'
