from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from thumbs import ImageWithThumbsField
from ckeditor.fields import RichTextField
from Member.models import Member, Base
import datetime
from basemodule.models import *


# Create your models here.

WORK_FLOW_STATUS = ((0, u'Pending'), (1,u'Problem Queue'), (2,
                    u'Problem Project Conversation Queue'), (3, u'Closed'))

PROBLEM_VISIBLE_CHOICES = ((0, u'Only To RightArm'), (1, u'To Public'))



class Person(Base):
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank = True)
    last_name = models.CharField(max_length=100, blank = True)



class Problem(Base):
    """ Class describes Problems """

    problem_category = models.ForeignKey(Problem_Category)
    name = models.CharField(max_length=100)
    summary = models.CharField('Problem Objective', blank=True, null=True,
                               max_length=150)
    description = RichTextField('Problem Statement', blank=True,
            null=True)
    requirement = RichTextField('Description', blank=True,
            null=True)
    image = ImageWithThumbsField(upload_to='static/%Y/%m/%d', sizes=((90,
                                 120), (120, 120), (180, 240), (360, 480)),
                                 blank=True, null=True)
    target_amount = models.PositiveIntegerField('Target Amt', blank=True,
            null=True)

    created_by = models.ForeignKey(Member, related_name='Created_By_Member',
                                   blank=True, null=True)
    visible = models.IntegerField(choices=PROBLEM_VISIBLE_CHOICES, default=0)
    tags = models.ManyToManyField(Member, related_name='Tagged Members')
    start_date = models.DateField(max_length=20, blank=True, null=True)
    end_date = models.DateField(max_length=20, blank=True, null=True)
    person_with_problem =  models.ForeignKey(Person, blank = True, null = True)

    def __unicode__(self):
        return '%s' % self.name


class WorkFlow(Base):

    """ Class describes Work Flow Of Problems """

    initiated_by = models.ForeignKey(Member, related_name='Initiated By',
                                     blank=True, null=True)
    assigned_to = models.ForeignKey(Member, related_name='Assigned To',
                                    blank=True, null=True)
    description = RichTextField(blank=True, null = True)
    content_type = models.ForeignKey(ContentType,
                                     verbose_name=_('content type'),
                                     related_name='Content_Type_Of_Problem')
    object_id = models.TextField(_('object ID'))
    relatedTo = generic.GenericForeignKey(ct_field='content_type',
            fk_field='object_id')
    status = models.IntegerField(choices=WORK_FLOW_STATUS, default=0)

    def __unicode__(self):
        return '%s' % self.status

class ChallengeKeywords(Base):
    name = models.CharField("Name", max_length=200,blank=True, null=True)
    slug = models.SlugField("URL4SEO", blank=True, null=True)
    short_desc = RichTextField("Short Description",blank=True,null=True)

    def __unicode__(self):
        return '%s - %s' % (self.name,self.slug)

class OtherContacts(Base):
    content_type = models.ForeignKey(ContentType,
                                    verbose_name=_('content type'),
                                    related_name='Content_Type_Of_OtherContacts')
    object_id = models.TextField(_('object_id'))
    name = models.CharField('Name', max_length=50,blank=True,null=True)
    mobile = models.CharField('Mobile', max_length=200, blank=True, null=True)
    country = models.CharField('Country', max_length=200, blank=True,null=True)
    city = models.CharField('City',max_length=200, blank=True,null=True)

    def __unicode__(self):
        if self.name:
            return self.name
        else:
            return str(self.id)


class Challenge(Base):
    description = RichTextField(blank = True, null = True,verbose_name="Description of Challange")
    URL = models.URLField("Link url", max_length=200 ,blank=True,null=True)
    video = models.FileField("Upload Vedio/Image",upload_to='static/%Y/%m/%d', blank=True, null=True)
    keywords = models.ManyToManyField(ChallengeKeywords,verbose_name = "Tags/Key Words",blank=True, null=True)
    beneficiary = models.ManyToManyField(OtherContacts,blank=True, null=True)
    updated_by = models.ForeignKey(Member, related_name = 'related_to_update_challenge', blank=True, null=True)
    created_by = models.ForeignKey(Member, related_name = 'related_to_create_challenge', blank=True, null=True)
    is_published = models.BooleanField(default=False)
    challenge_status = models.IntegerField('Status',blank=True,null=True,choices=WORK_FLOW_STATUS,default=0)

    def __unicode__(self):
        return '%s' % self.description[0:25]


"""

class Giver(Base):
    donation_to_cause = models.CharField(max_length="255",blank=True,null=True)
    gifts_in_kind = models.CharField(max_length="255",blank=True,null=True)
    time_and_skill = models.CharField(max_length="255",blank=True,null=True)
    support_good_cause = models.CharField(max_length="255",blank=True,null=True)
    keywords = models.ManyToManyField(ChallengeKeywords,verbose_name = "Tags/Key Words",blank=True, null=True)
    member = models.ForeignKey(Member, related_name = 'related_to_giver', blank=True, null=True)
    challenge = models.ForeignKey(Challenge, related_name = "giving_to_challenge", blank = True, null = True)

    def __unicode__(self):
        return str(self.donation_to_cause)
"""



class GiverMaster(Base):
    parent = models.ForeignKey('self', blank=True, null=True)
    name = models.CharField(max_length=300)
    active = models.IntegerField(blank=True, null=True, default=2)


    def __unicode__(self):
        return self.name

    def get_child(self):
        return GiverMaster.objects.filter(parent = self)

    def get_all_parent(self):
        return GiverMaster.objects.filter(parent = None)



class Giver(models.Model):
    member = models.ForeignKey(Member, related_name='giver_member', blank=True, null=True)
    givermaster = models.ManyToManyField(GiverMaster, blank=True,null=True)
    giver_keywords = models.CharField('Giver_keywords', max_length=200, blank=True, null=True)

