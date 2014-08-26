"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from basemodule.models import *
from django.test import TestCase
from django.contrib.auth.models import User
from Social.models import *
from Member.models import *
from django.contrib.auth.models import User
from django.test import Client

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

class Salutations_tests(TestCase):

    def test_add_salutations_invalid(self):
        salutation_obj = Salutation.objects.create(name='Mr')
        sal_list = Salutation.objects.all()
        self.assertEqual(sal_list.count(), 5)

    def test_edit_salutations_invalid(self):
        salutation_obj = Salutation.objects.create(name='Mr')
        sal_obj = Salutation.objects.get(id=1)
        sal_obj.name = 'Mrs'
        sal_obj.save()
        sal_obj = Salutation.objects.get(name='Mrs')
        sal_list = Salutation.objects.all()
        self.assertEqual(sal_list.count(), 2)

    def test_delete_salutations_invalid(self):
        salutation_obj = Salutation.objects.create(name='Mr')
        sal_obj = Salutation.objects.get(id=1)
        sal_obj.delete()
        sal_list = Salutation.objects.all()
        self.assertEqual(sal_list.count(), 3)

class test_skills(TestCase):

    def test_add_skills(self):
        sk_obj = Skills.objects.create(name="eating")
        skills = Skills.objects.all()
        self.assertEqual(skills.count(), 1)

    def test_edit_skills(self):
        sk_obj = Skills.objects.create(name="eating")
        self.assertEqual(sk_obj.name, 'eating')
        sk_obj.name = "sleeping"
        sk_obj.save()
        self.assertEqual(sk_obj.name, 'sleeping')

    def test_delete_skills(self):
        sk_obj = Skills.objects.create(name="eating")
        skills = Skills.objects.all()
        self.assertEqual(skills.count(), 1)
        sk_obj.delete()
        skills = Skills.objects.all()
        self.assertEqual(skills.count(), 0)

class test_skills_invlaid(TestCase):

    def test_add_skills_invalid(self):
        sk_obj = Skills.objects.create(name="eating")
        skills = Skills.objects.all()
        self.assertEqual(skills.count(), 1)

    def test_edit_skills_invalis(self):
        sk_obj = Skills.objects.create(name="eating")
        self.assertEqual(sk_obj.name, 'eating')
        sk_obj.name = "sleepings"
        sk_obj.save()
        self.assertEqual(sk_obj.name, 'sleeping')

    def test_delete_skills_invalid(self):
        sk_obj = Skills.objects.create(name="eating")
        skills = Skills.objects.all()
        self.assertEqual(skills.count(), 2)
        sk_obj.delete()
        skills = Skills.objects.all()
        self.assertEqual(skills.count(), 0)

class test_members(TestCase):

    def test_add_member(self):
        salutation_obj = Salutation.objects.create(name='Mr')
        sk_obj = Skills.objects.create(name="eating")
        user_obj = User.objects.create_user(username='usser', password="dfasfd")
        mem_obj = Member.objects.create(user_type=0, salutation=salutation_obj, user=user_obj )
        members = Member.objects.all()
        self.assertEqual(members.count(), 1)

    def test_edit_member(self):
        salutation_obj = Salutation.objects.create(name='Mr')
        sk_obj = Skills.objects.create(name="eating")
        user_obj = User.objects.create_user(username='usser', password="dfasfd")
        mem_obj = Member.objects.create(user_type=0, salutation=salutation_obj, user=user_obj )
        member = Member.objects.get(id=1)
        member.user_type=1
        member.save()
        self.assertEqual(member.user_type, 1)

    def test_delete_member(self):
        salutation_obj = Salutation.objects.create(name='Mr')
        sk_obj = Skills.objects.create(name="eating")
        user_obj = User.objects.create_user(username='usser', password="dfasfd")
        mem_obj = Member.objects.create(user_type=0, salutation=salutation_obj, user=user_obj )
        member = Member.objects.get(id=1)
        members = Member.objects.all()
        self.assertEqual(members.count(), 1)
        member.delete()
        members = Member.objects.all()
        self.assertEqual(members.count(), 0)

class test_messages(TestCase):

    def test_add_message(self):
        salutation_obj = Salutation.objects.create(name='Mr')
        sk_obj = Skills.objects.create(name="eating")
        user_obj1 = User.objects.create_user(username='mahiti', password="mahiti")
        user_obj2 = User.objects.create_user(username='usser2', password="dfasfd2")
        mem_obj1 = Member.objects.create(user_type=0, salutation=salutation_obj, user=user_obj1)
        mem_obj2 = Member.objects.create(user_type=0, salutation=salutation_obj, user=user_obj2)
        Messages.objects.create(profile=mem_obj1, msg_from=mem_obj1, msg_to=mem_obj2, message="dfasf", status="success", msg_type="sent")
        messages = Messages.objects.all()
        self.assertEqual(messages.count(), 1)
    
    #def test_reply_message(self):
        
    

class test_all_members(TestCase):

    def test_display_all_members(self):

        user_obj1 = User.objects.create_user(username='mahiti', password="mahiti")
        user_obj2 = User.objects.create_user(username='usser2', password="dfasfd2")
        client_obj = Client()
        client_obj.login(username='mahiti', password='mahiti')
        resp = client_obj.get('/social/all-members/', {})
        self.assertEqual(resp.status_code, 200)

    def test_request_connection(self):

        user_obj1 = User.objects.create_user(username='mahiti', password="mahiti")
        user_obj2 = User.objects.create_user(username='usser2', password="dfasfd2")
        salutation_obj = Salutation.objects.create(name='Mr')
        sk_obj = Skills.objects.create(name="eating")
        mem_obj1 = Member.objects.create(user_type=0, salutation=salutation_obj, user=user_obj1)
        mem_obj2 = Member.objects.create(user_type=0, salutation=salutation_obj, user=user_obj2)
        client_obj = Client()
        client_obj.login(username='mahiti', password="mahiti")
        resp = client_obj.get('/social/request-connection/', {'action_id':mem_obj2.id, 'action':'connection_request'})
        self.assertEqual(resp.status_code, 200)

    def test_request_connection_without_login(self):

        user_obj1 = User.objects.create_user(username='mahiti', password="mahiti")
        user_obj2 = User.objects.create_user(username='usser2', password="dfasfd2")
        salutation_obj = Salutation.objects.create(name='Mr')
        sk_obj = Skills.objects.create(name="eating")
        mem_obj1 = Member.objects.create(user_type=0, salutation=salutation_obj, user=user_obj1)
        mem_obj2 = Member.objects.create(user_type=0, salutation=salutation_obj, user=user_obj2)
        client_obj = Client()
        #client_obj.login(username='mahiti', password="mahiti")
        resp = client_obj.get('/social/request-connection/', {'action_id':mem_obj2.id, 'action':'connection_request'})
        self.assertEqual(resp.status_code, 200)


    def test_request_connection_invalid(self):

        user_obj1 = User.objects.create_user(username='mahiti', password="mahiti")
        user_obj2 = User.objects.create_user(username='usser2', password="dfasfd2")
        salutation_obj = Salutation.objects.create(name='Mr')
        sk_obj = Skills.objects.create(name="eating")
        mem_obj1 = Member.objects.create(user_type=0, salutation=salutation_obj, user=user_obj1)
        mem_obj2 = Member.objects.create(user_type=0, salutation=salutation_obj, user=user_obj2)
        client_obj = Client()
        client_obj.login(username='mahiti', password="mahiti")
        resp1 = client_obj.get('/social/request-connection/', {'action_id':mem_obj2.id, 'action':'connection_request'})
        resp = client_obj.get('/social/request-connection/', {'action_id':mem_obj2.id, 'action':''})
        self.assertEqual(resp.status_code, 200)

    def test_request_connection_invalid_login(self):

        user_obj1 = User.objects.create_user(username='mahiti', password="mahiti")
        user_obj2 = User.objects.create_user(username='usser2', password="dfasfd2")
        salutation_obj = Salutation.objects.create(name='Mr')
        sk_obj = Skills.objects.create(name="eating")
        mem_obj1 = Member.objects.create(user_type=0, salutation=salutation_obj, user=user_obj1)
        mem_obj2 = Member.objects.create(user_type=0, salutation=salutation_obj, user=user_obj2)
        client_obj = Client()
        client_obj.login(username='mahiti1', password="mahiti1")
        resp1 = client_obj.get('/social/request-connection/', {'action_id':mem_obj2.id, 'action':'connection_request'})
        resp = client_obj.get('/social/request-connection/', {'action_id':mem_obj2.id, 'action':''})
        self.assertEqual(resp.status_code, 200)


    def test_cancel_request(self):

        user_obj1 = User.objects.create_user(username='mahiti', password="mahiti")
        user_obj2 = User.objects.create_user(username='usser2', password="dfasfd2")
        salutation_obj = Salutation.objects.create(name='Mr')
        sk_obj = Skills.objects.create(name="eating")
        mem_obj1 = Member.objects.create(user_type=0, salutation=salutation_obj, user=user_obj1)
        mem_obj2 = Member.objects.create(user_type=0, salutation=salutation_obj, user=user_obj2)
        client_obj = Client()
        client_obj.login(username='mahiti', password="mahiti")
        resp1 = client_obj.get('/social/request-connection/', {'action_id':mem_obj2.id, 'action':'connection_request'})
        resp2 = client_obj.get('/social/request-connection/', {'action_id':mem_obj2.id, 'action':'cancel'})
        self.assertEqual(resp1.status_code, 200)
        self.assertEqual(resp2.status_code, 200)

    def test_cancel_request_invalid(self):

        user_obj1 = User.objects.create_user(username='mahiti', password="mahiti")
        user_obj2 = User.objects.create_user(username='usser2', password="dfasfd2")
        salutation_obj = Salutation.objects.create(name='Mr')
        sk_obj = Skills.objects.create(name="eating")
        mem_obj1 = Member.objects.create(user_type=0, salutation=salutation_obj, user=user_obj1)
        mem_obj2 = Member.objects.create(user_type=0, salutation=salutation_obj, user=user_obj2)
        client_obj = Client()
        client_obj.login(username='mahiti', password="mahiti")
        resp1 = client_obj.get('/social/request-connection/', {'action_id':mem_obj2.id, 'action':'connection_request'})
        resp2 = client_obj.get('/social/request-connection/', {'action_id':mem_obj2.id, 'action':''})
        self.assertEqual(resp1.status_code, 200)
        self.assertEqual(resp2.status_code, 200)

    def test_unfriend(self):

        user_obj1 = User.objects.create_user(username='mahiti', password="mahiti")
        user_obj2 = User.objects.create_user(username='usser2', password="dfasfd2")
        salutation_obj = Salutation.objects.create(name='Mr')
        sk_obj = Skills.objects.create(name="eating")
        mem_obj1 = Member.objects.create(user_type=0, salutation=salutation_obj, user=user_obj1)
        mem_obj2 = Member.objects.create(user_type=0, salutation=salutation_obj, user=user_obj2)
        client_obj = Client()
        client_obj.login(username='mahiti', password="mahiti")
        resp1 = client_obj.get('/social/request-connection/', {'action_id':mem_obj2.id, 'action':'connection_request'})
        resp2 = client_obj.get('/social/request-connection/', {'action_id':mem_obj2.id, 'action':'disconnect'})
        self.assertEqual(resp1.status_code, 200)
        self.assertEqual(resp2.status_code, 200)

    def test_unfriend_invalid(self):

        user_obj1 = User.objects.create_user(username='mahiti', password="mahiti")
        user_obj2 = User.objects.create_user(username='usser2', password="dfasfd2")
        salutation_obj = Salutation.objects.create(name='Mr')
        sk_obj = Skills.objects.create(name="eating")
        mem_obj1 = Member.objects.create(user_type=0, salutation=salutation_obj, user=user_obj1)
        mem_obj2 = Member.objects.create(user_type=0, salutation=salutation_obj, user=user_obj2)
        client_obj = Client()
        client_obj.login(username='mahiti', password="mahiti")
        resp1 = client_obj.get('/social/request-connection/', {'action_id':mem_obj2.id, 'action':'connection_request'})
        resp2 = client_obj.get('/social/request-connection/', {'action_id':mem_obj2.id, 'action':'disc'})
        self.assertEqual(resp1.status_code, 200)
        self.assertEqual(resp2.status_code, 200)

    def test_accept_connection_request(self):

        user_obj1 = User.objects.create_user(username='mahiti', password="mahiti")
        user_obj2 = User.objects.create_user(username='usser2', password="dfasfd2")
        salutation_obj = Salutation.objects.create(name='Mr')
        sk_obj = Skills.objects.create(name="eating")
        mem_obj1 = Member.objects.create(user_type=0, salutation=salutation_obj, user=user_obj1)
        mem_obj2 = Member.objects.create(user_type=0, salutation=salutation_obj, user=user_obj2)
        client_obj = Client()
        client_obj.login(username='mahiti', password="mahiti")
        resp1 = client_obj.get('/social/request-connection/', {'action_id':mem_obj2.id, 'action':'connection_request'})
        resp2 = client_obj.get('/social/request-connection/', {'action_id':mem_obj2.id, 'action':'accept'})
        self.assertEqual(resp1.status_code, 200)
        self.assertEqual(resp2.status_code, 200)

    def test_connection_request1_invalid(self):

        user_obj1 = User.objects.create_user(username='mahiti', password="mahiti")
        user_obj2 = User.objects.create_user(username='usser2', password="dfasfd2")
        salutation_obj = Salutation.objects.create(name='Mr')
        sk_obj = Skills.objects.create(name="eating")
        mem_obj1 = Member.objects.create(user_type=0, salutation=salutation_obj, user=user_obj1)
        mem_obj2 = Member.objects.create(user_type=0, salutation=salutation_obj, user=user_obj2)
        client_obj = Client()
        client_obj.login(username='mahiti', password="mahiti")
        resp1 = client_obj.get('/social/request-connection/', {'action_id':mem_obj2.id, 'action':'connection_request'})
        resp2 = client_obj.get('/social/request-connection/', {'action_id':mem_obj2.id, 'action':'accept1'})
        self.assertEqual(resp1.status_code, 200)
        self.assertEqual(resp2.status_code, 200)

    def test_connection_request2_invalid(self):

        user_obj1 = User.objects.create_user(username='mahiti', password="mahiti")
        user_obj2 = User.objects.create_user(username='usser2', password="dfasfd2")
        salutation_obj = Salutation.objects.create(name='Mr')
        sk_obj = Skills.objects.create(name="eating")
        mem_obj1 = Member.objects.create(user_type=0, salutation=salutation_obj, user=user_obj1)
        mem_obj2 = Member.objects.create(user_type=0, salutation=salutation_obj, user=user_obj2)
        client_obj = Client()
        client_obj.login(username='mahiti', password="mahiti")
        resp1 = client_obj.get('/social/request-connection/', {'action_id':mem_obj2.id, 'action':'connection_request'})
        resp2 = client_obj.get('/social/request-connection/', {'action_id':mem_obj2.id, 'action':'accept1'})
        self.assertEqual(resp1.status_code, 200)
        self.assertEqual(resp2.status_code, 302)
