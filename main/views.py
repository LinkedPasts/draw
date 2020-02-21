from django.contrib import auth, messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
import json

from main.models import Feature, Map

def createFeature(request):
    print('in createFeature()', request.POST)
    mapid = request.POST['mapid']
    feature = json.loads(request.POST['jsonb'])
    mapobj = get_object_or_404(Map, pk=int(mapid))
    
    feat = Feature.objects.create(
        user = request.user,
        name = feature['properties']['name'],
        type = feature['properties']['type'],
        map = mapobj
    )
    result = {"mapid": mapid, "name": feature['properties']['name']}
    return JsonResponse(result,safe=False)
    