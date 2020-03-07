# api.views
#from django.contrib.auth.models import User, Group
#from django.db.models import Count
#from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import permissions
from rest_framework import viewsets

from api.serializers import FeatureSerializer

#from accounts.permissions import IsOwnerOrReadOnly, IsOwner
from main.models import Feature, Map, Project

class FeatureViewSet(viewsets.ModelViewSet):
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
