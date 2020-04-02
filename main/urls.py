from django.conf import settings
#from django.conf.urls.static import static
#from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path#, include
from django.views.generic.base import TemplateView

from . import views

app_name='main'
urlpatterns = [
    path(r'', login_required(TemplateView.as_view(
        template_name="main/home.html")),name="home"),

    path('fetch_projects/', views.fetchProjects, name='fetch-projects'),
    
    path('feature_create/', views.createFeature, name='feature-create'),
    path('feature_delete/', views.deleteFeature, name='feature-delete'),
    path('feature_update/', views.updateFeature, name='feature-update'),

    path('project_create/', views.ProjectCreateView.as_view(), name='project-create'),
    path('project_delete/<int:id>', views.ProjectDeleteView.as_view(), name='project-delete'),
    path('project_update/<int:pk>', views.ProjectUpdateView.as_view(), name='project-update'),

    path('map_create/<int:pid>', views.MapCreateView.as_view(), name='map-create'),
    path('map_delete/<int:id>', views.MapDeleteView.as_view(), name='map-delete'),
    path('map_update/<int:id>', views.MapUpdateView.as_view(), name='map-update'),
    
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
]
# + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
