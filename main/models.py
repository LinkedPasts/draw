from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.gis.db import models as geo
from django.contrib.postgres.fields import JSONField, ArrayField
from django.db import models
from django.conf import settings
from django.shortcuts import get_object_or_404
from main.choices import TEAMROLES

class Project(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
        related_name='projects', on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    label = models.CharField(max_length=20)
    uri = models.URLField(blank=True, null=True)
    create_date = models.DateTimeField(null=True, auto_now_add=True)

    @property
    def collab(self):
        projusers=ProjectUser.objects.filter(project_id = self.id)
        collabs=[]
        for pu in projusers:
            u = get_object_or_404(User, id=pu.user_id)
            #r = pu.role
            collabs.append(u)
        return collabs

    #@property
    #def placetypes(self):
        #ppts=ProjectPlacetype.objects.filter(project_id = self.id)
        #types=[]
        #for pt in ppts:
            #t = get_object_or_404(Placetype, id=pt.id)
            #types.append({'identifier':'aat:'+t.aat_id, 'label':t.term})
        #return types

    def __str__(self):
        return self.label
    
    class Meta:
        managed = True
        db_table = 'projects'    

class Map(models.Model):
    project = models.ForeignKey('main.Project', db_column='project',
        related_name='maps', on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
        related_name='maps', on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)

    label = models.CharField(max_length=20, unique=True) # unique slug
    title = models.CharField(max_length=500) # as published
    year_pub = models.IntegerField(null=True)
    cite_uri = models.URLField(null=True) # permalink
    cite_text = models.CharField(max_length=2044, null=False) # proper citation
    tiles = models.BooleanField(default=False) # tiles in place?
    
    # temporal coverage
    when = JSONField(null=True)
    when_constant = models.BooleanField(default=True) # use map when for all its features?
    
    # tileset metadata
    minzoom = models.CharField(max_length=2,null=True)
    maxzoom = models.CharField(max_length=2,null=True)
    bounds = ArrayField(models.DecimalField(decimal_places=8,max_digits=11),null=True)

    #@property
    #def placetypes(self):
        #mpts=MapPlacetype.objects.filter(map_id = self.id)
        #types=[]
        #for pt in mpts:
            #t = get_object_or_404(Placetype, id=pt.id)
            #types.append({'identifier':'aat:'+t.aat_id, 'label':t.term})
        #return types

    def __str__(self):
        return self.label

    class Meta:
        managed = True
        db_table = 'maps'    

class Feature(models.Model):
    # TODO: map and type are reserved - problem?
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
        related_name='features', on_delete=models.CASCADE)
    map = models.ForeignKey('main.Map', db_column='map',
        related_name='features', on_delete=models.CASCADE)

    name = models.CharField(max_length=255)
    placetype = models.CharField(max_length=20, blank=False, null=False)
    jsonb = JSONField(blank=True, null=True) # includes when
    
    # write one at creation, for heck of it
    geom_point = geo.PointField(blank=True, null=True)
    geom_line = geo.LineStringField(blank=True, null=True)
    geom_poly = geo.PolygonField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'features'    

# name-map for atlas index case
class Name(models.Model):
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=200) # source label(s)
    maps = ArrayField(models.CharField(max_length=10)) # array of map ids
    flag = models.BooleanField(default=False,null=True) # checked if name is digitized
    
    def __str__(self):
        return self.name
    
    class Meta:
        managed = True
        db_table = 'names'    
    
class ProjectUser(models.Model):
    project = models.ForeignKey(Project, related_name='projects',
        default=-1, on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='users',
        default=-1, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, null=False, choices=TEAMROLES)

    class Meta:
        managed = True
        db_table = 'project_user'
    
class Placetype(models.Model):
    aat_id = models.IntegerField(unique=True)
    parent_id = models.IntegerField(null=True,blank=True)
    term = models.CharField(max_length=100)
    term_full = models.CharField(max_length=100)
    note = models.TextField(max_length=3000)
    fclass = models.CharField(max_length=1,null=True,blank=True)
    
    def __str__(self):
        return str(self.aat_id) +':'+self.term
    
    class Meta:
        managed = True
        db_table = 'placetypes'

# placetypes designated per project
class ProjectPlacetype(models.Model):
    project = models.ForeignKey(Project,default=-1, on_delete=models.CASCADE)    
    placetype = models.ForeignKey(Placetype,default=-1, on_delete=models.CASCADE)
 
    class Meta:
        managed = True
        db_table = 'project_placetype'

# placetypes designated per map
class MapPlacetype(models.Model):
    map = models.ForeignKey(Map, default=-1, on_delete=models.CASCADE)    
    placetype = models.ForeignKey(Placetype, default=-1, on_delete=models.CASCADE)
 
    class Meta:
        managed = True
        db_table = 'map_placetype'
