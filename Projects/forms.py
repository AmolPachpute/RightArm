from django import forms
from django.forms import ModelForm
from Projects.models import *
from django.forms.extras.widgets import SelectDateWidget


class Project_Category_Form(ModelForm):

    ''' Project Category Form '''

    class Meta:

        model = Project_Category
        exclude = ('created_on', 'modified_on', 'is_active', 'url4SEO')
        
class Project_Manage_Form(ModelForm):
    ''' Project Manage Form '''
    
    class Meta:
        
        model = Project
        exclude = ('is_active')

    