from django.contrib import admin
from usermanagement.models import Menus, Role_Config, Role_Types, User_Roles

admin.site.register(Menus)
admin.site.register(Role_Config)
admin.site.register(Role_Types)
admin.site.register(User_Roles)