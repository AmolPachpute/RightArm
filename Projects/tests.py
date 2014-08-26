"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from basemodule.models import *
from django.contrib.auth.models import User
from Projects.models import *
from Member.models import *
from django.contrib.auth.models import User
from django.test import Client


class SimpleTest(TestCase):
    
    def test_add_project_category(self):
        user_obj1 = User.objects.create_user(username='mahiti', password="mahiti")
        proj_cat1 = Project_Category.objects.create(name="catname")
        project_obj = Project.objects.create(project_category=proj_cat1, name="sample", status=0, created_by=user_obj1)
        proj_list = Project.objects.all()
        self.assertEqual(proj_list.count() ,1)
    
    def test_edit_project_category(self):
        #import ipdb; ipdb.set_trace()
        user_obj1 = User.objects.create_user(username='mahiti', password="mahiti")
        proj_cat1 = Project_Category.objects.create(name="catname")
        project_obj = Project.objects.create(project_category=proj_cat1, name="sample", status=0, created_by=user_obj1)
        project = Project.objects.get(id=1)
        project.name="test"
        project.status=0
        project.save()
        proj_list = Project.objects.all()
        self.assertEqual(proj_list.count() ,1)
        
    def test_delete_project_category(self):
        #import ipdb; ipdb.set_trace()
        user_obj1 = User.objects.create_user(username='mahiti', password="mahiti")
        proj_cat1 = Project_Category.objects.create(name="catname")
        project_obj = Project.objects.create(project_category=proj_cat1, name="sample", status=0, created_by=user_obj1)
        project = Project.objects.get(id=1)
        project.delete()
        proj_list = Project.objects.all()
        self.assertEqual(proj_list.count() ,0)
        
    