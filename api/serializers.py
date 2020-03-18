# api.serializers.py

from django.contrib.auth.models import User, Group
from rest_framework import serializers
from main.models import Feature, Map, Project

class GeomSerializer(serializers.ModelSerializer):
    # TODO: return same geojson as held in drawnFeatures (incl leaflet_id)
    #name = serializers.ReadOnlyField()
    fid = serializers.ReadOnlyField(source='id')
    type = serializers.ReadOnlyField(source='jsonb.geometry.type')
    placetype = serializers.ReadOnlyField(source='type')
    coordinates = serializers.ReadOnlyField(source='jsonb.geometry.coordinates')
    properties = serializers.ReadOnlyField(source='jsonb.properties')

    class Meta:
        model = Feature
        fields = ('fid','name','placetype','type','coordinates','properties')

class FeatureSerializer(serializers.ModelSerializer):
    # id, map, user, name, type, jsonb, geom_point, geom_line, geom_poly
    # jsonb: type:Feature, geometry{type,coordinates}, properties{name,type,leaflet_id}
    #geowkt = serializers.ReadOnlyField(
        #source=('geom_point' if 'jsonb.geometry.type'=='Point' else 'geom_line' \
                #if 'jsonb.geometry.type'=='LineString' else 'geom_poly')
    #)
    #citation = serializers.ReadOnlyField(source='jsonb.citation')
    #when = serializers.ReadOnlyField(source='jsonb.when')
    placetype = serializers.ReadOnlyField(source='type')
    coordinates = serializers.ReadOnlyField(source='jsonb.geometry.coordinates')

    class Meta:
        model = Feature
        fields = ('id', 'map','user','name','type','coordinates','jsonb','placetype',
                  'geom_point','geom_line','geom_poly')
