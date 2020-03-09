from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView

from main import views

urlpatterns = [
    path(r'', TemplateView.as_view(template_name="main/index.html"), name="index"),
    path('home/', include('main.urls')),

    path('create_project/', views.ProjectCreateView.as_view(), name='project-create'),
    path('create_map/', views.MapCreateView.as_view(), name='map-create'),

    path('delete_project/', views.ProjectDeleteView.as_view(), name='project-delete'),
    path('delete_map/', views.MapDeleteView.as_view(), name='map-delete'),
    
    #path('home/fetch_projects/', views.fetchProjects, name='fetch-projects'),
    #path('home/feature_create/', views.createFeature, name='feature-create'),
    path('api/', include('api.urls')),
    path('accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls)
]
# + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
