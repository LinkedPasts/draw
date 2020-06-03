from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView

from main import views
from api.views import MapNamesView

urlpatterns = [
    path(r'', TemplateView.as_view(template_name="main/index.html"), name="index"),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('draw/', include('main.urls')),
    
    path('project_create/', views.ProjectCreateView.as_view(), name='project-create'),
    path('project_delete/<int:id>', views.ProjectDeleteView.as_view(), name='project-delete'),
    path('project_update/<int:pk>', views.ProjectUpdateView.as_view(), name='project-update'),

    path('map_create/<int:pid>', views.MapCreateView.as_view(), name='map-create'),
    path('map_delete/<int:id>', views.MapDeleteView.as_view(), name='map-delete'),
    path('map_update/<int:pk>', views.MapUpdateView.as_view(), name='map-update'),    
    
    path('api/', include('api.urls')),
    path('accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls),
    path('names/', MapNamesView.as_view(), name='names-api'),
    
]
# + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


#path('create_project/', views.ProjectCreateView.as_view(), name='project-create'),
#path('create_map/', views.MapCreateView.as_view(), name='map-create'),

#path('delete_project/', views.ProjectDeleteView.as_view(), name='project-delete'),
#path('delete_map/', views.MapDeleteView.as_view(), name='map-delete'),

