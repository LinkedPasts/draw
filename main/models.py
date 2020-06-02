from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.gis.db import models as geo
from django.contrib.postgres.fields import JSONField, ArrayField
from django.db import models
from django.conf import settings
from main.choices import TEAMROLES

class Project(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
        related_name='projects', on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    label = models.CharField(max_length=20)
    uri = models.URLField(blank=True, null=True)
    create_date = models.DateTimeField(null=True, auto_now_add=True)

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

    title = models.CharField(max_length=255)
    label = models.CharField(max_length=20)
    year = models.IntegerField(null=True)
    cite_uri = models.URLField(null=True)
    cite_text = models.CharField(max_length=2044, null=False)
    create_date = models.DateTimeField(auto_now_add=True)
    tiles = models.BooleanField(default=False)
    
    # values 
    minzoom = models.CharField(max_length=2,null=True)
    maxzoom = models.CharField(max_length=2,null=True)
    bounds = ArrayField(models.DecimalField(decimal_places=8,max_digits=11),null=True)

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
    jsonb = JSONField(blank=True, null=True)
    
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
            
