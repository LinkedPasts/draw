from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.gis.geos import GEOSGeometry
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import (CreateView, DeleteView, ListView, UpdateView)

import json, sys
from .utils import myprojects
from main.models import Project, Map, Feature
from main.forms import ProjectCreateModelForm, MapCreateModelForm

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
            return Project.objects.filter( Q(id__in=myprojects(me)) | Q(owner=me) | Q(id__lt=3)).order_by('-id')

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
        maps = Map.objects.all().filter(project=proj).order_by('-create_date')
        
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
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    model = Project
    #form_class = ProjectDetailModelForm
    template_name = 'main/map_update.html'
    fields = ['id', 'project', 'title', 'label', 'owner', 'cite_text', 'cite_uri']

    def get_success_url(self):
        id_ = self.kwargs.get("id")
        print('messages:', messages.get_messages(self.kwargs))
        #return '/projects/'+str(id_)+'/detail'

    # Dataset has been edited, form submitted
    def form_valid(self, form):
        print('foo')

@login_required
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

@login_required    
def deleteFeature(request,*args,**kwargs):
    print('deleteFeature() request', request)
    print('in deleteFeature() kwargs', kwargs)
    if request.method == 'POST':
        _id = request.POST.get('fid')
        #result = {"msg":"id in kwargs: "+str(_id)}
        try:
            get_object_or_404(Feature, pk=_id).delete()
            result = {"msg":"deleted "+str(_id)}
        except:
            result = {"msg":"delete of "+str(id)+' failed: '+sys.exc_info()}
            print('delete failed',_id, sys.exc_info())
    return JsonResponse(result,safe=False)
    
@login_required    
def updateFeature(request):
    newfeat = json.loads(request.POST['jsonb'])
    _id = newfeat['fid']
    name = newfeat['properties']['name']; print(name)
    placetype = newfeat['properties']['placetype']; print(placetype)
    print('newfeat in updateFeature(), type', newfeat,type(newfeat))
    # get existing 
    #fobj = get_object_or_404(Feature, pk=_id)
    fobj = Feature.objects.filter(pk=_id)
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
        result = {"msg":"updated"+json.dumps(newfeat)}    
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
        placetype = feature['properties']['placetype']
        ftype = feature['geometry']['type']
        #gfield = 'geom_'+('point' if ftype=='Point' else 'line' if ftype=='LineString' else 'poly')
        # GEOSGeometry('MULTIPOLYGON((( 1 1, 1 2, 2 2, 1 1)))'))
        mapobj = get_object_or_404(Map, pk=int(mapid))
        newfeat = Feature(
            user = request.user,
            name = feature['properties']['name'],
            placetype = placetype,
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
    