from Member.models import *
from django.contrib.auth.models import User
from basemodule.models import *

def removeusers(userlist):
    import ipdb;ipdb.set_trace()
    userlist = User.objects.filter(id__in = userlist)
    for i in userlist:
        mem = Member.objects.filter(user = i).latest('id')
        if mem and mem.get_address_obj():
            print "===================================",mem,mem.get_address_obj()
            mem.get_address_obj().delete()
        mem.delete()
        i.delete()
