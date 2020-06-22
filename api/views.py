# api.views
from django.contrib.auth.models import User, Group
#from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import View
from rest_framework import generics
from rest_framework import permissions
from rest_framework import viewsets

from api.serializers import FeatureSerializer
#from accounts.permissions import IsOwnerOrReadOnly, IsOwner
from main.models import Feature, Map, Name
import re

class MapNamesView(View):
    """ Returns name,type tuples for given map when available """
    @staticmethod
    def get(request):
        """
        args in request.GET:
            [string] mapid
        """    
        #print('MapNamesView GET:',request.GET)
        namelist=[]
        mapid = request.GET.get('mapid')
        mapnum = re.search('_(.*)$',get_object_or_404(Map,pk=mapid).label).group(1)
        print('mapnum from label',mapnum)
        #qs=Name.objects.filter(maps__contains=[mapnum],type__in=['settlement'],flag=False).values_list('name','id','type')
        qs=Name.objects.filter(maps__contains=[mapnum],flag=True).values_list('name','id','type')
        for n in qs:
            namelist.append({"name":n[0],"id":n[1]})
        return JsonResponse(namelist, safe=False, json_dumps_params={'ensure_ascii':False})
    
# feature for map
class FeatureViewSet(viewsets.ModelViewSet):
    queryset = Feature.objects.all()
    #serializer_class = GeomSerializer
    serializer_class = FeatureSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    
    def get_queryset(self):
        projid = self.request.GET.get('projid')
        mapid = self.request.GET.get('mapid')
        user = self.request.GET.get('user')
        mapIds = Map.objects.values('id').filter(project = projid)
        # places polygons below other features
        qs = Feature.objects.filter(map__in=mapIds).order_by('geom_poly')
        #print('qs count',qs.count())
        return qs
    

# Linked Places record
# not operational
class LPViewSet(viewsets.ModelViewSet):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    
    def get_queryset(self):
        projid = self.request.GET.get('projid')
        #mapid = self.request.GET.get('mapid')
        mapIds = Map.objects.values('id').filter(project = projid)
        qs = Feature.objects.filter(map__in=mapIds)
        #print('qs count',qs.count())
        return qs
