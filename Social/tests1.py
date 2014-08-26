"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from basemodule.models import *
from django.test import TestCase
from django.contrib.auth.models import User
from Social.models import *

class SimpleTest(TestCase):

    def test_add_salutations(self):
        salutation_obj = Salutation.objects.create(name='Mr')
        sal_list = Salutation.objects.all()
        self.assertEqual(sal_list.count(), 1)

    def test_edit_salutations(self):
        salutation_obj = Salutation.objects.create(name='Mr')
        sal_obj = Salutation.objects.get(id=1)
        sal_obj.name = 'Mrs'
        sal_obj.save()
        sal_obj = Salutation.objects.get(name='Mrs')
        sal_list = Salutation.objects.all()
        self.assertEqual(sal_list.count(), 1)

    def test_delete_salutations(self):
        salutation_obj = Salutation.objects.create(name='Mr')
        sal_obj = Salutation.objects.get(id=1)
        sal_obj.delete()
        sal_list = Salutation.objects.all()
        self.assertEqual(sal_list.count(), 0)

class test_skills(TestCase):

    def test_add_member1(self):
        salutation_obj = Salutation.objects.create(name='Mr')