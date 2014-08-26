from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from thumbs import ImageWithThumbsField
from ckeditor.fields import RichTextField
from Member.models import Member, Skills
from django.contrib.auth.models import User
from basemodule.models import *
import datetime

# Create your models here.

STATUS_CHOICES = ((0, u'Inception/New'), (1, u'In Progress'), (2, u'Completed'
                  ))

POST_TYPE_CHOICES = (
    (0, u'Text'),
    (1, u'Image'),
    (2, u'Video'),
    (3, u'Link'),
    (4, u'Audio'),
    (5, u'Doc/Pdf'),
    )

PROJECT_RELATION_TYPE_CHOICES = ((0, u'Owner'), (1, u'Moderator'), (2,
                                 u'Giver'), (3, u'Member'))

TASK_PRIORITY_CHOICES = ((0, u'High'), (1, u'Medium'), (2, u'Low'))

TASK_STATUS_CHOICES = (
    (0, u'Complete'),
    (1, u'Incomplete'),
    (2, u'Inprogress'),
    (3, u'Not Yet Started'),
    (4, u'Onhold'),
    (5, u'Pending'),
    )

OFFERED_TYPES = ((0, u'Physical'), (1, u'Virtual'))




class Beneficiary(Base):
    """ Class describes beneficiaries for particular project """


    name = models.CharField(max_length=100, blank=True, null=True)
    description = RichTextField(blank=True, null = True)

    def __unicode__(self):
        return '%s' % self.name


class Goals(Base):
    """ Class describes goals of the project """

    name = models.CharField(max_length=100)
    description = RichTextField(blank=True, null = True)

    def __unicode__(self):
        return '%s' % self.name


class Transact(Base):
    """ Class describes project requirement types """

    name = models.CharField(max_length=100)
    description = RichTextField(blank=True, null = True)

    def __unicode__(self):
        return '%s' % self.name



class Project(Base):
    """ This class Stores information about Project """

    project_category = models.ForeignKey(Project_Category)
    name = models.CharField(max_length=100)
    image = ImageWithThumbsField(upload_to='static/%Y/%m/%d', sizes=((90,
                                 120), (120, 120), (180, 240), (360, 480)),
                                 blank=True, null=True)
    summary = models.CharField('Project Objective', blank=True, null=True,
                               max_length=150)
    description = RichTextField(blank=True, null = True)
    requirement = RichTextField(blank=True, null = True)
    target_amount = models.PositiveIntegerField('Target Amt', blank=True,
            null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    created_by = models.ForeignKey(Member, related_name='Project_CreatedBy')
    beneficiaries = models.ManyToManyField(Beneficiary, blank=True, null=True)
    transactions = models.ManyToManyField(Transact, blank=True, null=True)
    goals = models.ManyToManyField(Goals, blank=True, null=True)
    start_date = models.DateField(max_length=20, blank=True, null=True)
    end_date = models.DateField(max_length=20, blank=True, null=True)
    peoples = models.ManyToManyField(Member, through = 'Project_Member_Relationship', blank = True, null = True)
    
    def __unicode__(self):
        return '%s' % self.name

   

class Project_Member_Relationship(models.Model):
    """ Class describes project member relationship """

    relation_type = \
        models.IntegerField(choices=PROJECT_RELATION_TYPE_CHOICES, default=0)
    project = models.ForeignKey(Project)
    member = models.ForeignKey(Member)

    def __unicode__(self):
        return '%s' % self.project.name


class Offer_Time(Base):
    """ Class describes members who offered time for the projects """

    offered_by = models.ForeignKey(Member)
    project = models.ForeignKey(Project)
    offered_type = models.IntegerField(choices=OFFERED_TYPES, default=0)
    start_date = models.DateField(max_length=20, blank=True, null=True)
    end_date = models.DateField(max_length=20, blank=True, null=True)
    description = RichTextField(blank=True, null = True)

    def __unicode__(self):
        return self.offered_by



class Goods_Required_For_Project(Base):
    """ Class describes goods required for the projects """

    name = models.CharField(max_length=100)
    description = RichTextField(blank=True, null = True)
    url = models.URLField(blank=True)
    qty = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.ForeignKey(Member, related_name='GoodsCreatedBy')
    project = models.ForeignKey(Project)

    def __unicode__(self):
        return self.name


class Goods_Given_From_Member_To_Project(Base):
    """ Class describes goods given from members to givers in the projects """

    goods = models.ForeignKey(Goods_Required_For_Project)
    given_by = models.ForeignKey(Member)
    description = RichTextField(blank=True, null = True)
    url = models.URLField(blank=True)
    qty = models.CharField(max_length=100, blank=True, null=True)

    def __unicode__(self):
        return self.given_by



class Member_Skills(Base):
    """ Class describes member skills to be used in the projects """

    created_by = models.ForeignKey(Member, related_name='SkillsCreatedBy')
    project = models.ForeignKey(Project)
    skills = models.ManyToManyField(Skills, blank = True, null = True)

    def __unicode__(self):
        return self.project.name


class Influence(Base):
    """ Class describes members who influence who for what purpose for \
    the project """

    influenced_by = models.ForeignKey(Member, related_name='InfluencedBy')
    project = models.ForeignKey(Project)
    description = RichTextField(blank=True, null = True)

    def __unicode__(self):
        return self.volunteer


class Post(Base):
    """ Class describes posts of the projects """

    post_type = models.IntegerField(choices=POST_TYPE_CHOICES, default=0)
    project = models.ForeignKey(Project)
    image = ImageWithThumbsField(upload_to='static/%Y/%m/%d', sizes=((90,
                                 120), (180, 240), (360, 480)), blank=True,
                                 null=True)
    URL = models.CharField('Link url', max_length=200, blank=True)
    description = RichTextField(blank=True, null = True)
    video_file = models.FileField(upload_to='static/%Y/%m/%d', blank=True,
                                  null=True)
    audio_file = models.FileField(upload_to='static/%Y/%m/%d', blank=True,
                                  null=True)
    doc = models.FileField(upload_to='static/%Y/%m/%d', blank=True, null=True)
    tags = models.ManyToManyField(Member, blank=True, null=True)
    featured = models.BooleanField(default=False)

    def __unicode__(self):
        return self.post_type


class Task(Base):
    """ Class describes project tasks """

    name = models.CharField(max_length=100)
    description = RichTextField(blank=True, null = True)
    associated_goal = models.ForeignKey(Goals, blank=True, null=True)
    assign_to = models.ManyToManyField(Member, blank=True, null=True)
    priority = models.IntegerField(choices=TASK_PRIORITY_CHOICES, default=1)
    status = models.IntegerField(choices=TASK_STATUS_CHOICES, default=3)
    content_type = models.ForeignKey(ContentType,
                                     verbose_name=_('content type'),
                                     related_name='TaskCPTM')
    object_id = models.TextField(_('object ID'))
    from_date = models.DateField(max_length=20, blank=True, null=True)
    to_date = models.DateField(max_length=20)
    parent = models.ForeignKey('self', blank=True, null=True)

    def __unicode__(self):
        return self.name
