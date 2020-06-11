from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.gis.geos import GEOSGeometry
from django.http import HttpResponse, JsonResponse, FileResponse
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import (View, CreateView, DeleteView, ListView, UpdateView)

import json, sys
from .utils import myprojects
from main.models import Project, Map, Feature, ProjectUser
from main.forms import ProjectCreateModelForm, MapCreateModelForm

def download_project(request, *args, **kwargs):
    proj=get_object_or_404(Project,pk=kwargs['projid'])
    print(proj.title)
    
    #response = FileResponse(open(fn, 'rb'), content_type='text/json')
    #response['Content-Disposition'] = 'attachment; filename="'+os.path.basename(fn)+'"'
    
    #return response

class DrawView(LoginRequiredMixin, View):
    #template_name = 'main/draw.html'
    
    def get(self, request, *args, **kwargs):
        context = {'projid': self.kwargs['projid']}
        return render(request, 'main/draw.html', context)
    
    # kwargs = {'projid':<n>}
    #def get_context_data(self, *args, **kwargs):
        #context = super(DrawView, self).get_context_data(*args, **kwargs)
        
        #context['projid'] = self.kwargs['projid']
        #return context

    
class DashboardView(LoginRequiredMixin, ListView):
    context_object_name = 'project_list'
    template_name = 'main/dashboard.html'

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    def get_queryset(self):
        # TODO: make .team() a method on User
        me = self.request.user
        if me.username in ['admin','karlg']:
            print('in get_queryset() if',me)
            return Project.objects.all().order_by('-id')
        else:
            # returns permitted datasets (rw) + black and dplace (ro)
            return Project.objects.filter( Q(id__in=myprojects(me)) | Q(owner=me) ).order_by('-id')

    def get_context_data(self, *args, **kwargs):
        me = self.request.user
        context = super(DashboardView, self).get_context_data(*args, **kwargs)
        print('in get_context',me)

        #types_ok=['ccodes','copied','drawn']
        # list areas
        #userareas = Area.objects.all().filter(type__in=types_ok).order_by('created')
        #context['area_list'] = userareas if me.username == 'whgadmin' else userareas.filter(owner=self.request.user)

        #context['viewable'] = ['uploaded','inserted','reconciling','review_hits','reviewed','review_whg','indexed']
        # TODO: user place collections
        #print('DashboardView context:', context)
        return context

class ProjectCreateView(LoginRequiredMixin, CreateView):
    form_class = ProjectCreateModelForm
    template_name = 'main/project_create.html'
    success_message = 'project created'
    success_url="/home/dashboard/"

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    success_url="/home/dashboard/"

    #form_class = ProjectDetailModelForm
    template_name = 'main/project_update.html'
    model = Project
    fields = ['id', 'title', 'label', 'owner', 'uri']
    
    def get_context_data(self, *args, **kwargs):
        context = super(ProjectUpdateView, self).get_context_data(*args, **kwargs)
        print('ProjectUpdateView get_context_data() kwargs:',self.kwargs)
        id_ = self.kwargs.get("pk")
        proj = get_object_or_404(Project, id=id_)
        maps = Map.objects.all().filter(project=proj,tiles=True).order_by('-create_date')
        
        context['maps'] = maps
        context['project_id'] = id_
        return context

class ProjectDeleteView(DeleteView):
    template_name = 'main/project_delete.html'

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Project, id=id_)

    def get_success_url(self):
        return reverse('main:dashboard')
    

class MapCreateView(LoginRequiredMixin, CreateView):
    form_class = MapCreateModelForm
    template_name = 'main/map_create.html'
    success_message = 'map created'
    success_url="/home/dashboard/"
    
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    

class MapDeleteView(DeleteView):
    template_name = 'main/map_delete.html'

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Map, id=id_)

    def get_success_url(self):
        return reverse('home')

class MapUpdateView(LoginRequiredMixin, UpdateView):
    form_class = MapCreateModelForm
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    #success_url='/home/project_update/'+str(proj_id)

    model = Map
    template_name = 'main/map_update.html'
    #fields = ['id', 'project', 'title', 'label', 'cite_text', 'cite_uri', 'tiles', 'when',
              #'when_constant','minzoom','maxzoom','bounds']
    
    def get_context_data(self, *args, **kwargs):
        context = super(MapUpdateView, self).get_context_data(*args, **kwargs)
        id_ = self.kwargs.get("pk")
        proj_id = get_object_or_404(Map,pk=id_).project_id
        
        context['map_id'] = id_
        context['project_id'] = proj_id
        return context

    def get_success_url(self, *args, **kwargs):
        proj_id=get_object_or_404(Map,pk=self.kwargs.get("pk")).project_id
        print('get_success_url; proj_id',proj_id)        
        return '/project_update/'+str(proj_id)

@login_required
def fetchProjects(request):
    u=request.user
    result = {"projects":[], "maps":[]}
    if u.is_superuser:
        projects = Project.objects.all()
    else:
        collab_projects = ProjectUser.objects.filter(user=u).values_list('project',flat=True)
        projects = Project.objects.filter( Q(id__in=collab_projects) | Q(owner=u) )
    #maps = Map.objects.filter(tiles=True)
    maps = Map.objects.filter(tiles=True,project__in=projects)
    #feature_count = sum([m.features.count() for m in maps])
    for p in projects:
        count=sum([m.features.count() for m in p.maps.all()])
        result['projects'].append(
            {'id':p.id, 'owner':p.owner_id, 'label':p.label, 'title':p.title
            ,'feature_count':count}
        )
    for m in maps:
        result['maps'].append(
            {'id':m.id, 'proj_id':m.project_id, 'proj_label':m.project.label, 'label':m.label, 
             'title':m.title, 'cite_uri':m.cite_uri, 'cite_text':m.cite_text, 
             'minzoom':m.minzoom, 'maxzoom':m.maxzoom, 'bounds':m.bounds,
             'when':m.when, 'when_constant':m.when_constant,'feature_count':m.features.count()}
        )
    
    return JsonResponse(result,safe=False)

@login_required    
def deleteFeature(request,*args,**kwargs):
    print('deleteFeature() request', request)
    print('in deleteFeature() kwargs', kwargs)
    if request.method == 'POST':
        #_id = request.POST.get('fid')
        _id = int(request.POST.get('fid'))
        #result = {"msg":"id in kwargs: "+str(_id)}
        try:
            #get_object_or_404(Feature, pk=_id).delete()
            get_object_or_404(Feature, jsonb__properties__leaflet_id = _id).delete()
            result = {"msg":"deleted "+str(_id)}
        except:
            result = {"msg":"delete of "+str(id)+' failed: '+str(sys.exc_info())}
            print('delete failed',_id, sys.exc_info())
    return JsonResponse(result,safe=False)

@login_required    
def updateFeature(request):
    newfeat = json.loads(request.POST['jsonb'])
    print('newfeat in updateFeature(), type', newfeat,type(newfeat))
    #_id = newfeat['fid']
    leaflet_id = newfeat['properties']['leaflet_id']
    name = newfeat['properties']['names'][0]['toponym']; print(name)
    placetype = newfeat['properties']['types'][0]['identifier']; print(placetype)
    # get existing 
    #fobj = Feature.objects.filter(pk=_id)
    fobj = Feature.objects.filter(jsonb__properties__leaflet_id = leaflet_id)
    ftype = newfeat['geometry']['type']; print(ftype) # Point, LineString, etc
    geowkt = GEOSGeometry(json.dumps(newfeat['geometry']))
    # replace some values
    try:
        fobj.update(name = name)
        fobj.update(placetype = placetype)
        fobj.update(jsonb = newfeat)
        fobj.update(geom_point = geowkt if ftype == 'Point' else None)
        fobj.update(geom_line = geowkt if ftype == 'LineString' else None)
        fobj.update(geom_poly = geowkt if ftype == 'Polygon' else None)
        result = {"msg":"updated "+json.dumps(newfeat)}    
    except:
        result = {"msg":"updating "+str(_id)+' failed; '+sys.exc_info()}
    return JsonResponse(result,safe=False)
    
@login_required    
def createFeature(request):
    print('in createFeature()', request.POST)
    mapid = int(request.POST['mapid'])
    print('mapid',mapid,type(mapid))
    if mapid > 0:
        feature = json.loads(request.POST['jsonb'])
        names = feature['properties']['names']
        types = feature['properties']['types']
        ftype = feature['geometry']['type']
        mapobj = get_object_or_404(Map, pk=int(mapid))
        newfeat = Feature(
            user = request.user,
            name = names[0]['toponym'],
            placetype = types[0]['label'],
            jsonb = feature,
            map = mapobj,
            geom_point = GEOSGeometry(json.dumps(feature['geometry'])) if ftype == 'Point' else None,
            geom_line = GEOSGeometry(json.dumps(feature['geometry'])) if ftype == 'LineString' else None,
            geom_poly = GEOSGeometry(json.dumps(feature['geometry'])) if ftype == 'Polygon' else None,
        )
        newfeat.save()
        print('feat',newfeat)
        result = {"mapid": mapid, "ftype": ftype, "name": names[0], "errors":[]}
    else:
        # no map selected
        result = {"errors":["no map selected"]}
    return JsonResponse(result,safe=False)
    