from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from ckeditor.fields import RichTextField
import datetime
from thumbs import ImageWithThumbsField
from basemodule.models import *

# Create your models here.

DEVICE_CHOICES = ((0, u'PC'), (1, u'Laptop'), (2, u'Mobile'))

FORM_STATUS_CHOICES = ((u'Success', u'Success'), (u'Failure', u'Failure'))

USER_TYPE_CHOICES = ((u'Member', u'Member'), (u'Giver', u'Giver'), (u'Reciver', u'Reciver'))


class SocialNetworkngSites(Base):

    """ social n/w links of Alumni """

    commtype = models.ForeignKey(CommType)
    detail = models.CharField('Link', max_length=100, blank=True, null=True)
    content_type = models.ForeignKey(ContentType,
                                     verbose_name=_('content type'),
                                     related_name='Content Type')
    object_id = models.TextField(_('object ID'))

    def __unicode__(self):
        return u'%s' % self.commtype

class Member(Base):
    """ Class describes Users """
    user_type = models.CharField(max_length=200, choices = USER_TYPE_CHOICES, blank = True)
    salutation = models.ForeignKey(Salutation, verbose_name='Salutation',
                                   blank=True, null=True)
    user = models.ForeignKey(User, related_name='USER')
    photo = ImageWithThumbsField(upload_to='static/%Y/%m/%d', sizes=((90,
                                 120), (120, 120), (180, 240), (360, 480)),
                                 blank=True, null=True)
    about_me = RichTextField(blank=True, null = True)
    skills = models.ManyToManyField(Skills, blank=True, null = True)
    dob = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return u'%s' % (self.user.username)

    def get_relation(self):
        MemberRelation

    def get_address_obj(self):
        add_obj = ''
        try:
            add_obj = Address.objects.get(content_type__model="member", object_id=self.id)
        except:
            pass
        return add_obj

class Member_Information(Base):

    """ Class describes Users Information i.e the device thru which he logged in and at what time, etc """

    member = models.ForeignKey(Member, blank=True, null=True)
    ip_address = models.CharField('IP Address', max_length=100, blank=True,
                                  null=True)
    location_info = models.TextField(blank=True)
    city = models.CharField(max_length=150, blank=True, null=True)
    type_of_device = models.CharField(max_length=100, choices=DEVICE_CHOICES, default='PC',
            null=True)
    browser = models.CharField('Browser', max_length=250, blank=True,
                               null=True)
    native_language = models.CharField('Native Language', max_length=100,
                                       blank=True, null=True)
    os_info = models.CharField('Operating system Information', max_length=500)
    is_bot = models.BooleanField('Is Robot', default=False)

    def __unicode__(self):
        return '%s' % self.member.user.username

class Member_Skill(Base):
    skill = models.CharField(max_length=255,blank=True,null=True)
    member = models.ForeignKey(Member, blank=True, null=True)
    slug = models.SlugField()

    def __unicode__(self):
        return '%s' % self.skill
