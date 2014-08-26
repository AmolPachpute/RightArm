from django import template
register = template.Library()

from Member.models import *
from basemodule.models import *

@register.filter
def get_skill_list(request):
    usr = request.user.id
    if usr:
        skill_list = Skills.objects.filter(member__user__id=usr)
        return skill_list
    else:
        skill_list = Skills.objects.filter(is_active = 2)
        return skill_list


