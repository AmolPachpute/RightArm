from Member.models import *


class Menus(Base):
    name = models.CharField(max_length=100)
    slug = models.SlugField("SEO friendly url, use only aplhabets and hyphen", max_length=60)
    parent = models.ForeignKey('self', blank = True, null = True)
    link = models.CharField(max_length=512L, blank=True)
    menu_order = models.IntegerField(null=True, blank=True)
    active = models.IntegerField(default=2)
    created_by = models.ForeignKey(User)

    def __unicode__(self):
        return self.name

    def get_sub_menus(self):
        return Menus.objects.filter(parent=self, active = 2)


class Role_Types(Base):
    name = models.CharField(max_length=100)
    slug = models.SlugField("SEO friendly url, use only aplhabets and hyphen", max_length=60)
    created_by = models.ForeignKey(User)
    active = models.IntegerField(default=2)

    def __unicode__(self):
        return self.name


class Role_Config(Base):
    role = models.ForeignKey(Role_Types)
    feature_id = models.ForeignKey(Menus)
    add = models.IntegerField(null=True, blank=True)
    edit = models.IntegerField(null=True, blank=True)
    view = models.IntegerField(null=True, blank=True)
    delete = models.IntegerField(null=True, blank=True)
    search = models.IntegerField(null=True, blank=True)
    mlist = models.IntegerField(null=True, blank=True)
    generate = models.IntegerField(null=True, blank=True)
    task_status = models.IntegerField(null=True, blank=True)
    created_by = models.ForeignKey(User)
    modified_by = models.ForeignKey(User, related_name = 'Role_Config_CreatedBy')


class User_Roles(Base):
    user = models.ForeignKey(User)
    role_type = models.ManyToManyField(Role_Types)
    active = models.IntegerField(default=2)
    created_by = models.ForeignKey(User, related_name = 'User_Role_CreatedBy')
    modified_by = models.ForeignKey(User, related_name = 'User_Role_ModifiedBy')
