from django import template
register = template.Library()
from Social.models import *

@register.filter
def get_status(request, to_member):

    """ getting connection status  """

    from_obj = Member.objects.get(user=request.user)
    member_rel_obj1 = MemberRelation.objects.filter(from_id = from_obj, to_id=to_member)
    member_rel_obj2 = MemberRelation.objects.filter(from_id = to_member , to_id=from_obj)
    if member_rel_obj1:
        return member_rel_obj1[0]
    if member_rel_obj2:
        if member_rel_obj2[0].relation_type == 'Pending':
            return 'received_request'
        else:
            return member_rel_obj2[0]
    return False

@register.filter
def get_attachment_name(attch_path):

    return str(attch_path).split('/')[-1]
