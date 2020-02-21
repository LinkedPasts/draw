from django.conf import settings
from django.contrib.gis.db import models as geo
from django.contrib.postgres.fields import JSONField, ArrayField
from django.db import models

class Project(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
        related_name='projects', on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    label = models.CharField(max_length=20)

class Map(models.Model):
    project = models.ForeignKey('main.Project', db_column='project',
        related_name='maps', on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    label = models.CharField(max_length=20)
    cite_uri = models.URLField(null=True)
    cite_text = models.CharField(max_length=2044, null=False)


class Feature(models.Model):
    # TODO: map and type are reserved - problem?
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
        related_name='features', on_delete=models.CASCADE)
    map = models.ForeignKey('main.Map', db_column='map',
        related_name='features', on_delete=models.CASCADE)

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=20, blank=False, null=False)
    jsonb = JSONField(blank=True, null=True)
    
    geom_point = geo.PointField(blank=True, null=True)
    geom_line = geo.MultiLineStringField(blank=True, null=True)
    geom_poly = geo.MultiPolygonField(blank=True, null=True)
