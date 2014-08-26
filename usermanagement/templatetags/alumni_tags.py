""" all Template tags Stores here """

from django import template

from schools.models import Institution, Programme
from django.contrib.auth.models import User
from alumni.manage_views import getSubDom
from alumni.models import Alumni, AlumniRelation, NewsFeed, AlumniStatus
from django.db.models import Q
from mcms.models import Image
from alumni.manage_views import getSubDom

register = template.Library()

@register.filter
def getschool(value):
    """ getting subdomain name of School """
    try:
        obj = Institution.objects.get(id=value)
    except:
        pass
    url = "http://" + obj.url4SEO +".alumni.com:8000/school-detail/"
    return url


@register.filter
def get_fren_request(request, value):
    alumni = Alumni.objects.get(userprofile__user = request.user)
    fren = Alumni.objects.get(id = value)
    (torelation, fromrelation) = ([], [])
    try:
        torelation = AlumniRelation.objects.get(from_id = alumni, to_id = fren)
    except:
        pass
    try:
        fromrelation = AlumniRelation.objects.get(to_id = alumni, \
                    from_id = fren)
    except:
        pass
    if torelation:
        return torelation
    elif fromrelation:
        return fromrelation
    else:
        return None

@register.filter
def get_fren_images(request, alumni_id):
    alumni = Alumni.objects.get(id=alumni_id)
    friends = AlumniRelation.objects.filter(Q(from_id=alumni)|Q(to_id=alumni),is_active=True)
    frn_list = []
    urldict = {}
    for i in friends:
        if i.from_id == alumni:
            frn_list.append(i.to_id)
        if i.to_id == alumni:
            frn_list.append(i.from_id)
    for j in frn_list:
        if j.get_alumni_profileinfo():
            urldict[j]=j.get_alumni_profileinfo().image
        else:
            urldict[j]=''
    return urldict


@register.filter
def get_alumni(request, value):
    """ getting subdomain name of School """
    obj = ""
    try:
        obj = Alumni.objects.get(userprofile__user_id=value)
    except:
        pass
    return obj

@register.filter
def get_feed_msg(request, value):
    """ getting subdomain name of School """
    msg =""
    feed_dict = {}
    feed = NewsFeed.objects.get(id=value)
    if feed.feedtype == 'Event':
        pgm = Programme.objects.get(id=feed.object_id)
        msg = "Participating in the Event: " + "<a href = "+'/events/'+str(int(pgm.id))+">" + pgm.name + "</a>"
        return msg
    if feed.feedtype == 'Friend':
        alumni = Alumni.objects.get(id=feed.object_id)
        msg = "is Friend with " + "<a href = "+'/public-profile/'+str(alumni.uid)+">" + alumni.userprofile.user.first_name + "</a>"
        return msg
    if feed.feedtype == 'Comment':
        astatus = AlumniStatus.objects.get_or_create(id=feed.object_id)
        msg = "Commented on " 
        if request.user == astatus.alumni.userprofile.user:
            msg += "your status"
        else:
            msg += "<a href = "+'/public-profile/'+str(astatus.alumni.uid)+">" + astatus.alumni.userprofile.user.first_name +"'s "+ "</a>" + " status"
        return msg

@register.filter
def get_prt_evt(request, value):
    """ getting subdomain name of School """
    obj = ""
    try:
        obj = Programme.objects.get(id=value)
    except:
        pass
    return obj

@register.filter
def get_alumni_status(value):
    """ getting subdomain name of School """
    obj = ""
    try:
        obj = AlumniStatus.objects.get(id=value)
    except:
        pass
    return obj


@register.filter
def get_comment_alumni(value):
    """ getting subdomain name of School """
    obj = ""
    try:
        obj = Alumni.objects.get(userprofile__user_id=value)
    except:
        pass
    return obj


@register.filter
def get_school_logo(request):
    """ getting subdomain name of School """
    data = getSubDom(request)
    name = data['code']
    schoolid = data['insti_id']
    obj = Institution.objects.get(id=schoolid)
    return obj

