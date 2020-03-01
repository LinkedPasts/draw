from django.contrib import auth, messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
import json

from main.models import Project, Map, Feature

def fetchProjects(request):
    print('in fetchProject()', request.GET)
    result = {"projects":[], "maps":[]}
    projects = Project.objects.all()
    maps = Map.objects.all()
    for p in projects:
        result['projects'].append(
            {'id':p.id, 'owner':p.owner_id, 'label':p.label, 'title':p.title}
        )
    for m in maps:
        result['maps'].append(
            {'id':m.id, 'project':m.project_id, 'label':m.label, 
             'title':m.title, 'cite_uri':m.cite_uri, 'cite_text':m.cite_text}
        )
    
    return JsonResponse(result,safe=False)
    
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
    