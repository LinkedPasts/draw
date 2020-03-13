# api.views
from django.contrib.auth.models import User, Group
#from django.db.models import Count
#from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import permissions
from rest_framework import viewsets

from api.serializers import GeomSerializer, FeatureSerializer

#from accounts.permissions import IsOwnerOrReadOnly, IsOwner
from main.models import Feature, Map, Project

# geometry for map
class GeomViewSet(viewsets.ModelViewSet):
    queryset = Feature.objects.all()
    serializer_class = GeomSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    
    def get_queryset(self):
        projid = self.request.GET.get('projid')
        mapid = self.request.GET.get('mapid')
        user = self.request.GET.get('user')
        mapIds = Map.objects.values('id').filter(project = projid)
        qs = Feature.objects.filter(map__in=mapIds)
        #print('qs count',qs.count())
        return qs
    
    #def get_context_data(self, *args, **kwargs):
        #context = super(GeomViewSet, self).get_context_data(*args, **kwargs)
        #context['foo'] = 'bar'
        #return context    

# Linked Places record
# not operational
class LPViewSet(viewsets.ModelViewSet):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    
    def get_queryset(self):
        projid = self.request.GET.get('proj')
        mapid = self.request.GET.get('mapid')
        mapIds = Map.objects.values('id').filter(project = projid)
        qs = Feature.objects.filter(id__in=mapIds)
        #print('qs count',qs.count())
        return qs