# main.forms

from django import forms
#from django.forms import ClearableFileInput
from .models import Project, Map
#from main.choices import FORMATS, DATATYPES, STATUS

# id, title, label, owner_id, create_date, uri
class ProjectCreateModelForm(forms.ModelForm):
    
    class Meta:
        model = Project
        fields = ('title','label','owner','uri')
        #widgets = {
            #'description': forms.Textarea(attrs={
              #'rows':2,'cols': 35,'class':'textarea','placeholder':'brief description'})
            #,'uri_base': forms.URLInput(attrs={
              #'placeholder':'Leave blank unless record IDs are URIs','size':35})
        #}

    def __init__(self, *args, **kwargs):
        super(ProjectCreateModelForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {'required':'The field {fieldname} is required'.format(
          fieldname=field.label)}    
            
class MapCreateModelForm(forms.ModelForm):
    class Meta:
        model = Map
        fields = ('owner','project','title','label', 'year_pub',
                  'cite_uri','cite_text', 'tiles', 'when', 'when_constant', 'minzoom', 'maxzoom', 'bounds')
        widgets = {
        'when': forms.Textarea(attrs={
          'rows':2,'cols': 35,'class':'textarea','placeholder':'json when object'})
        ,'cite_uri': forms.URLInput(attrs={
          'placeholder':'Permalink?','size':35})
    }


    def __init__(self, *args, **kwargs):
        super(MapCreateModelForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {'required':'The field {fieldname} is required'.format(
          fieldname=field.label)}    