# api.serializers.py

from django.contrib.auth.models import User, Group
from rest_framework import serializers
from main.models import Feature, Map, Project

class GeomSerializer(serializers.ModelSerializer):
    fid = serializers.ReadOnlyField(source='id')
    type = serializers.ReadOnlyField(source='jsonb.geometry.type')
    #name = serializers.ReadOnlyField()
    placetype = serializers.ReadOnlyField(source='type')
    coordinates = serializers.ReadOnlyField(source='jsonb.geometry.coordinates')

    class Meta:
        model = Feature
        fields = ('fid','name','placetype','type','coordinates')

class FeatureSerializer(serializers.ModelSerializer):
    # id, map, user, name, type, jsonb, geom_point, geom_line, geom_poly
    # jsonb: type:Feature, geometry{type,coordinates}, properties{name,type,leaflet_id}
    placetype = serializers.ReadOnlyField(source='type')
    geowkt = serializers.ReadOnlyField(
        source=('geom_point' if 'jsonb.geometry.type'=='Point' else 'geom_line' \
                if 'jsonb.geometry.type'=='LineString' else 'geom_poly')
    )
    coordinates = serializers.ReadOnlyField(source='jsonb.geometry.coordinates')
    citation = serializers.ReadOnlyField(source='jsonb.citation')
    when = serializers.ReadOnlyField(source='jsonb.when')

    class Meta:
        model = Feature
        fields = ('id', 'map', 'user', 'name', 'type', 'jsonb', 'geom_point', 'geom_line', 'geom_poly')
