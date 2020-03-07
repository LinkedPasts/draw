from django.contrib import auth, messages
from django.contrib.gis.geos import GEOSGeometry
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
    mapid = int(request.POST['mapid'])
    print('mapid',mapid,type(mapid))
    if mapid > 0:
        feature = json.loads(request.POST['jsonb'])
        placetype = feature['properties']['type']
        ftype = feature['geometry']['type']
        #gfield = 'geom_'+('point' if ftype=='Point' else 'line' if ftype=='LineString' else 'poly')
        # GEOSGeometry('MULTIPOLYGON((( 1 1, 1 2, 2 2, 1 1)))'))
        mapobj = get_object_or_404(Map, pk=int(mapid))
        newfeat = Feature(
            user = request.user,
            name = feature['properties']['name'],
            type = placetype,
            jsonb = feature,
            map = mapobj,
            geom_point = GEOSGeometry(json.dumps(feature['geometry'])) if ftype == 'Point' else None,
            geom_line = GEOSGeometry(json.dumps(feature['geometry'])) if ftype == 'LineString' else None,
            geom_poly = GEOSGeometry(json.dumps(feature['geometry'])) if ftype == 'Polygon' else None,
        )
        newfeat.save()
        print('feat',newfeat)
        result = {"mapid": mapid, "ftype": ftype, "name": feature['properties']['name'], "errors":[]}
    else:
        # no map selected
        result = {"errors":["no map selected"]}
    return JsonResponse(result,safe=False)
    