# api.serializers.py

from django.contrib.auth.models import User, Group
from rest_framework import serializers
from main.models import Feature, Map, Project

class FeatureSerializer(serializers.ModelSerializer):
    # return geojson feature as held in drawnFeatures (incl leaflet_id)
    #name = serializers.ReadOnlyField()
    fid = serializers.ReadOnlyField(source='id')
    #type = "Feature"
    #ftype = serializers.ReadOnlyField(source='jsonb.geometry.type')
    #coordinates = serializers.ReadOnlyField(source='jsonb.geometry.coordinates')
    type = serializers.ReadOnlyField(source='jsonb.type')
    properties = serializers.ReadOnlyField(source='jsonb.properties')
    geometry = serializers.ReadOnlyField(source='jsonb.geometry')
    
    class Meta:
        model = Feature
        fields = ('fid','type','geometry','properties')

#class FeatureSerializer(serializers.ModelSerializer):
    ## id, map, user, name, type, jsonb, geom_point, geom_line, geom_poly
    ## jsonb: type:Feature, geometry{type,coordinates}, properties{name,type,leaflet_id}
    ##geowkt = serializers.ReadOnlyField(
        ##source=('geom_point' if 'jsonb.geometry.type'=='Point' else 'geom_line' \
                ##if 'jsonb.geometry.type'=='LineString' else 'geom_poly')
    ##)
    ##citation = serializers.ReadOnlyField(source='jsonb.citation')
    ##when = serializers.ReadOnlyField(source='jsonb.when')
    #placetype = serializers.ReadOnlyField(source='type')
    #coordinates = serializers.ReadOnlyField(source='jsonb.geometry.coordinates')

    #class Meta:
        #model = Feature
        #fields = ('id', 'map','user','name','type','coordinates','jsonb','placetype',
                  #'geom_point','geom_line','geom_poly')
