from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('contact/', TemplateView.as_view(template_name='contact.html'), name='contact'),
    
    # App URLs
    path('customer/', include('apps.customer.urls')),
    path('agent/', include('apps.collection_agent.urls')),
    path('municipality/', include('apps.municipality.urls')),
    path('recycler/', include('apps.recycler.urls')),
    path('admin-panel/', include('apps.admin_panel.urls')),
    
    # API endpoints
    path('api/', include('apps.core.api_urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = "SMARTRASH Admin"
admin.site.site_title = "SMARTRASH Admin Portal"
admin.site.index_title = "Welcome to SMARTRASH Administration"
