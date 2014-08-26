from django.test import TestCase
from basemodule.models import *
from django.test import Client

class SimpleTest(TestCase):
    def test_add_salutation(self):
        c = Client()
        s_obj = Salutation.objects.create(name='Dr')
        res = c.post('/configure/salutations/add/')
        self.assertEqual(res.status_code, 200)
    def test_edit_salutation(self):
        c = Client()
        s_obj = Salutation.objects.create(name='Ms.')
        res = c.post('/configure/salutations/edit/?objid=1')
        self.assertEqual(res.status_code,200)
    def test_activate_salutation(self):
        c =Client()
        s_obj = Salutation.objects.create(name='Ms.')
        s_obj = Salutation.objects.get(id=s_obj.id)
        s_obj.is_active = 2
        s_obj.save()
        res = c.post('/configure/salutations/active/?objid=1')
        self.assertEqual(res.status_code,200)
    def test_deactivate_salutation(self):
        c =Client()
        s_obj = Salutation.objects.create(name='Ms.')
        s_obj = Salutation.objects.get(id=s_obj.id)
        s_obj.is_active = 0
        s_obj.save()
        res = c.post('/configure/salutations/delete/?objid=1')
        self.assertEqual(res.status_code,200)
    def test_add_comm(self):
        c = Client()
        c_obj = CommType.objects.create(name='Oral')
        res = c.post('/configure/communicationtype/add/')
        self.assertEqual(res.status_code, 200)
    def test_edit_comm(self):
        c = Client()
        c_obj = CommType.objects.create(name='Written')
        res = c.post('/configure/communicationtype/edit/?objid=1')
        self.assertEqual(res.status_code,200)
    def test_activate_salutation(self):
        c =Client()
        c_obj = CommType.objects.create(name='Written')
        c_obj = CommType.objects.get(id=c_obj.id)
        c_obj.is_active = 2
        c_obj.save()
        res = c.post('/configure/communicationtype/active/?objid=1')
        self.assertEqual(res.status_code,200)
    def test_deactivate_salutation(self):
        c =Client()
        c_obj = CommType.objects.create(name='Written')
        c_obj = CommType.objects.get(id=c_obj.id)
        c_obj.is_active = 0
        c_obj.save()
        res = c.post('/configure/communicationtype/delete/?objid=1')
        self.assertEqual(res.status_code,200)
    def test_add_skills(self):
        c = Client()
        s_obj = Skills.objects.create(name='Painting')
        res = c.post('/configure/skills/add/')
        self.assertEqual(res.status_code, 200)
    def test_edit_skills(self):
        c = Client()
        s_obj = Skills.objects.create(name='Painting')
        res = c.post('/configure/skills/edit/?objid=1')
        self.assertEqual(res.status_code,200)
    def test_activate_skills(self):
        c =Client()
        s_obj = Skills.objects.create(name='Ms.')
        s_obj = Skills.objects.get(id=s_obj.id)
        s_obj.is_active = 2
        s_obj.save()
        res = c.post('/configure/skills/active/?objid=1')
        self.assertEqual(res.status_code,200)
    def test_deactivate_salutation(self):
        c =Client()
        s_obj = Skills.objects.create(name='Ms.')
        s_obj = Skills.objects.get(id=s_obj.id)
        s_obj.is_active = 0
        s_obj.save()
        res = c.post('/configure/skills/delete/?objid=1')
        self.assertEqual(res.status_code,200)
    def test_add_tags(self):
        c = Client()
        t_obj = Tags.objects.create(name='t1')
        res = c.post('/configure/tags/add/')
        self.assertEqual(res.status_code, 200)
    def test_add_tags_test(self):
        c = Client()
        t_obj = Tags.objects.create(name='testtag')
        res = c.post('/configure/tags/add/')
        self.assertEqual(res.status_code, 200)
    def test_edit_skills(self):
        c = Client()
        t_obj = Tags.objects.create(name='t1')
        res = c.post('/configure/tags/edit/?objid=1')
        self.assertEqual(res.status_code,200)
    def test_activate_skills(self):
        c =Client()
        t_obj = Tags.objects.create(name='t1')
        t_obj = Tags.objects.get(id=t_obj.id)
        t_obj.is_active = 2
        t_obj.save()
        res = c.post('/configure/tags/active/?objid=1')
        self.assertEqual(res.status_code,200)
    def test_deactivate_salutation(self):
        c =Client()
        t_obj = Tags.objects.create(name='Ms.')
        t_obj = Tags.objects.get(id=t_obj.id)
        t_obj.is_active = 0
        t_obj.save()
        res = c.post('/configure/tags/delete/?objid=1')
        self.assertEqual(res.status_code,200)
    def test_add_Projcat(self):
        c = Client()
        p_obj = Project_Category.objects.create(name='t1')
        res = c.post('/configure/projectcategory/add/')
        self.assertEqual(res.status_code, 200)
    def test_edit_Projcat(self):
        c = Client()
        p_obj = Project_Category.objects.create(name='t1')
        res = c.post('/configure/projectcategory/edit/?objid=1')
        self.assertEqual(res.status_code,200)
    def test_activate_Projcat(self):
        c =Client()
        p_obj = Project_Category.objects.create(name='t1')
        p_obj = Project_Category.objects.get(id=p_obj.id)
        p_obj.is_active = 2
        p_obj.save()
        res = c.post('/configure/projectcategory/active/?objid=1')
        self.assertEqual(res.status_code,200)
    def test_deactivate_Projcat(self):
        c =Client()
        p_obj = Project_Category.objects.create(name='p1')
        p_obj = Project_Category.objects.get(id=p_obj.id)
        p_obj.is_active = 0
        p_obj.save()
        res = c.post('/configure/projectcategory/delete/?objid=1')
        self.assertEqual(res.status_code,200)
    def test_add_salutation1(self):
        c = Client()
        s_obj = Salutation.objects.create(name='Dr')
        res = c.post('/configure/salutations/add/')
        self.assertEqual(res.status_code, 200)
    def test_edit_salutation1(self):
        c = Client()
        s_obj = Salutation.objects.create(name='Ms.')
        res = c.post('/configure/salutations/edit/?objid=1')
        self.assertEqual(res.status_code,200)
    def test_activate_salutation1(self):
        c =Client()
        s_obj = Salutation.objects.create(name='Ms.')
        s_obj = Salutation.objects.get(id=s_obj.id)
        s_obj.is_active = 2
        s_obj.save()
        res = c.post('/configure/salutations/active/?objid=1')
        self.assertEqual(res.status_code,200)
    def test_deactivate_salutation1(self):
        c =Client()
        s_obj = Salutation.objects.create(name='Ms.')
        s_obj = Salutation.objects.get(id=s_obj.id)
        s_obj.is_active = 0
        s_obj.save()
        res = c.post('/configure/salutations/delete/?objid=1')
        self.assertEqual(res.status_code,200)
    def test_add_comm1(self):
        c = Client()
        c_obj = CommType.objects.create(name='Oral')
        res = c.post('/configure/communicationtype/add/')
        self.assertEqual(res.status_code, 200)
    def test_edit_comm1(self):
        c = Client()
        c_obj = CommType.objects.create(name='Written')
        res = c.post('/configure/communicationtype/edit/?objid=1')
        self.assertEqual(res.status_code,200)
    def test_activate_comm1(self):
        c =Client()
        c_obj = CommType.objects.create(name='Written')
        c_obj = CommType.objects.get(id=c_obj.id)
        c_obj.is_active = 2
        c_obj.save()
        res = c.post('/configure/communicationtype/active/?objid=1')
        self.assertEqual(res.status_code,200)
    def test_deactivate_comm1(self):
        c =Client()
        c_obj = CommType.objects.create(name='Written')
        c_obj = CommType.objects.get(id=c_obj.id)
        c_obj.is_active = 0
        c_obj.save()
        res = c.post('/configure/communicationtype/delete/?objid=1')
        self.assertEqual(res.status_code,200)
    def test_add_Projcat(self):
        c = Client()
        p_obj = Project_Category.objects.create(name='t1')
        res = c.post('/configure/projectcategory/add/')
        self.assertEqual(res.status_code, 200)
    def test_edit_Projcatest(self):
        c = Client()
        p_obj = Project_Category.objects.create(name='t1')
        res = c.post('/configure/projectcategory/edit/?objid=1')
        self.assertEqual(res.status_code,200)
    def test_activate_Projcatest(self):
        c =Client()
        p_obj = Project_Category.objects.create(name='t1')
        p_obj = Project_Category.objects.get(id=p_obj.id)
        p_obj.is_active = 2
        p_obj.save()
        res = c.post('/configure/projectcategory/active/?objid=1')
        self.assertEqual(res.status_code,200)
    def test_deactivate_Projcattest(self):
        c =Client()
        p_obj = Project_Category.objects.create(name='p1')
        p_obj = Project_Category.objects.get(id=p_obj.id)
        p_obj.is_active = 0
        p_obj.save()
        res = c.post('/configure/projectcategory/delete/?objid=1')
        self.assertEqual(res.status_code,200)
    def test_deactivate_comm(self):
        c =Client()
        c_obj = CommType.objects.create(name='Written')
        c_obj = CommType.objects.get(id=c_obj.id)
        c_obj.is_active = 0
        c_obj.save()
        res = c.post('/configure/communicationtype/delete/?objid=1')
        self.assertEqual(res.status_code,200)
    def test_add_skilltest(self):
        c = Client()
        s_obj = Skills.objects.create(name='Painting')
        res = c.post('/configure/skills/add/')
        self.assertEqual(res.status_code, 200)
    def test_edit_skill(self):
        c = Client()
        s_obj = Skills.objects.create(name='Painting')
        res = c.post('/configure/skills/edit/?objid=1')
        self.assertEqual(res.status_code,200)
    def test_activate_skilltest(self):
        c =Client()
        s_obj = Skills.objects.create(name='Ms.')
        s_obj = Skills.objects.get(id=s_obj.id)
        s_obj.is_active = 2
        s_obj.save()
        res = c.post('/configure/skills/active/?objid=1')
        self.assertEqual(res.status_code,200)

