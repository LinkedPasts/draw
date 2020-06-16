from django.contrib import admin
from .models import *

# appear in admin
class FeatureAdmin(admin.ModelAdmin):
    
    list_display = ('name','map','placetype', 'jsonb')
    search_fields = ['name']
    list_filter = ('map__project','placetype')
    exclude = ('geom_point', 'geom_line','geom_poly')
    sort_fields = ['feature']
    
admin.site.register(Feature,FeatureAdmin)

