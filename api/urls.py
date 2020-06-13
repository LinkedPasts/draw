# api.urls

from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers
from . import views

# TODO: too much of a black box
router = routers.DefaultRouter()

router.register(r'geoms', views.FeatureViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('',include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('features/',views.LPViewSet.as_view({'get': 'list'}))

    #url(r'^', include(router.urls)),
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
