from django import forms
from basemodule.models import *
from django.utils.translation import ugettext_lazy as _
from Problems.models import *
from RightArmCms.models import *
from django.forms import ModelForm


class LOGIN_FORM(forms.Form):
    username = forms.CharField(label=u'Username ')
    password = forms.CharField(label=u'Password ',
                               widget=forms.PasswordInput(render_value=False))

class SalutationForm(forms.ModelForm):
    class Meta:
        model = Salutation
        exclude = ('is_active','url4SEO')

class CommTypeForm(forms.ModelForm):
    class Meta:
        model = CommType
        exclude = ('is_active','url4SEO')

class SkillsForm(forms.ModelForm):
    class Meta:
        model = Skills
        exclude = ('is_active','url4SEO')

class TagsForm(forms.ModelForm):
    class Meta:
        model = Tags
        exclude = ('is_active','url4SEO')

class ProjectCategoryForm(forms.ModelForm):
    description = forms.CharField(widget = forms.Textarea)
    class Meta:
        model = Project_Category
        exclude = ('is_active','url4SEO')


class ProblemCategoryForm(forms.ModelForm):
    class Meta:
        model = Problem_Category
        exclude = ('is_active','url4SEO')

class BoundaryCountryForm(forms.ModelForm):
    name = forms.CharField(label=_(u'Country Name*'))
    class Meta:
        model = Boundary
        exclude = ('parent','active','level')


class BoundaryStateForm(forms.ModelForm):
    country = forms.ModelChoiceField(label=_(u'Country*'),queryset = Boundary.objects.filter(level=0,active=2))
    name = forms.CharField(label=_(u'State Name*'))
    class Meta:
        model = Boundary
        exclude = ('parent','active','level','url4SEO')
        fields = ['country','name']

class BoundaryDistrictForm(forms.ModelForm):
    country = forms.ModelChoiceField(label=_(u'Country*'),queryset = Boundary.objects.filter(level=0,active=2))
    state = forms.ModelChoiceField(label=_(u'State*'),queryset = Boundary.objects.filter(level=1,active=2))
    name = forms.CharField(label=_(u'District Name*'))
    class Meta:
        model = Boundary
        exclude = ('parent','active','level','url4SEO')
        fields = ['country','state','name']


class Challenge_Form(forms.ModelForm):
    class Meta:
        model = Challenge
        exclude = ('created_on','is_active','description','URL','keywords','updated_by','created_by','is_published','video','beneficiary','url4SEO')


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ('slug','block','team','staff','summary','listingOrder','status')

from django.core.files.images import get_image_dimensions
class ImageForm(ModelForm):
    class Meta:
        model=Image
        exclude=('content_type', 'object_id', 'title', 'listingOrder', 'status')
        def clean_picture(self):
            picture = self.cleaned_data.get("image")
            if not picture:
                raise forms.ValidationError("No image!")
            else:
                w, h = get_image_dimensions(picture)
                if w != 930:
                    raise forms.ValidationError("The image is %i pixel wide. It's supposed to be 930px" % w)
                if h != 300:
                    raise forms.ValidationError("The image is %i pixel high. It's supposed to be 300px" % h)
            return picture

class LinkForm(ModelForm):
    class Meta:
        model = Link
        exclude=('content_type', 'object_id', 'title', 'listingOrder', 'status')

class AttachmentForm(ModelForm):
    class Meta:
        model = Attachment
        exclude=('content_type', 'object_id', 'title', 'listingOrder', 'status')

class CodeForm(ModelForm):
    class Meta:
        model = CodeScript
        exclude=('content_type', 'object_id', 'status')



