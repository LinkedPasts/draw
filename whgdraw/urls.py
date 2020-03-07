from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView

from main import views

urlpatterns = [
    path(r'', TemplateView.as_view(template_name="main/index.html"), name="index"),
    path('home/', include('main.urls')),
    #path(r'home/', TemplateView.as_view(
        #template_name="main/home.html"),name="home"),
    
    
    #path('home/fetch_projects/', views.fetchProjects, name='fetch-projects'),
    #path('home/feature_create/', views.createFeature, name='feature-create'),
    path('accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls)
]
# + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
