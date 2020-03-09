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
]
# + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
