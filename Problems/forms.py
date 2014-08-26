from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from Problems.models import *
from basemodule.models import *
from django.utils.translation import ugettext_lazy as _

class Problem_form(forms.Form):
    class Meta:
        model = Problem

class Person_form(ModelForm):
    class Meta:
        model = Person
        exclude = ('visible',)

class ChallengeForm(forms.ModelForm):
    #keywords = forms.CharField(widget=forms.Textarea(attrs={'cols':30,'rows':5}))
    description = forms.CharField(widget=forms.Textarea(attrs={'cols':30,'rows':5}))
    class Meta:
        model = Challenge
        exclude = ['is_active','created_on','modified_on','slug','url4SEO','keywords','beneficiary','is_published','updated_by','created_by']

class ChallengeKeywordsForm(forms.ModelForm):
    #short_desc = forms.CharField(widget=forms.Textarea(attrs={'cols':30,'rows':5}))
    class Meta:
        model = ChallengeKeywords
        exclude = ['is_active','created_on','modified_on','slug','url4SEO','short_desc']


class OtherContactsForm(forms.ModelForm):
    class Meta:
        model = OtherContacts
        exclude = ['is_active','created_on','modified_on','content_type','object_id','url4SEO']

class AddressForm(forms.ModelForm):
    country = forms.ModelChoiceField(queryset = Boundary.objects.filter(level=0,active=2), required = False)
    class Meta:
        model = Address
        exclude = ['is_active','created_on','modified_on','content_type','object_id','url4SEO','subcounty','county','secondary_contact_no']
        fields = ['country', 'postal_code','primary_contact_no','email']

class DonationCategoryForm(forms.ModelForm):
    #parent = forms.ModelChoiceField(label=_(u'Donation'), queryset = GiverMaster.objects.filter(parent=None))
    class Meta:
        model = GiverMaster
        exclude = ['created_on','modified_on','is_active','url4SEO','active','parent']

class DonationTypeForm(forms.ModelForm):
    parent = forms.ModelChoiceField(label=_(u'Donation'), queryset = GiverMaster.objects.filter(parent=None))
    class Meta:
        model = GiverMaster
        exclude = ['created_on','modified_on','is_active','url4SEO','active']
