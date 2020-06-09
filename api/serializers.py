# api.serializers.py

from django.contrib.auth.models import User, Group
from rest_framework import serializers
from main.models import Feature, Map, Project

class FeatureSerializer(serializers.ModelSerializer):
    # return geojson feature as held in drawnFeatures (incl leaflet_id)
    fid = serializers.ReadOnlyField(source='id')
    type = serializers.ReadOnlyField(source='jsonb.type')
    properties = serializers.ReadOnlyField(source='jsonb.properties')
    geometry = serializers.ReadOnlyField(source='jsonb.geometry')
    when = serializers.ReadOnlyField(source='jsonb.when')
    
    class Meta:
        model = Feature
        fields = ('fid','type','geometry','properties','when')

