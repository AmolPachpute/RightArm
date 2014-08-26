from django import forms
from Social.models import *

class Send_Message_Form(forms.Form):

    subject = forms.CharField(max_length=200,  required=False)
    attachment = forms.FileField(required=False)
    message = forms.CharField(widget=forms.Textarea)

class Attachments_Form(forms.ModelForm):

    class Meta:
        model = Attachments
        fields = ('image_attachment', 'file_attachment')

class Att_Form(forms.Form):

    image_attachment = forms.ImageField(required=False)
    file_attachment = forms.FileField(required=False)

class EditProfilePhotoForm(forms.Form):

    photo = forms.ImageField(label="Upload Photo*")
    clear_image = forms.BooleanField(required=False)

class Add_Name_Form(forms.Form):

    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100, required=False)
