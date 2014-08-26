# Create your views here.
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from Member.models import *
from Social.models import *
from django.contrib.auth.models import User
import django
from Social.forms import *
from django.contrib.contenttypes.models import ContentType
from django.forms.formsets import formset_factory
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import json
from django.core.mail import *
from django.template.defaultfilters import slugify
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail, EmailMessage
from django.template import Context
from django.template.loader import get_template


def pagination(request, plist):
    paginator = Paginator(plist, 5)
    page = request.GET.get('page', '')
    try:
       plist = paginator.page(page)
    except PageNotAnInteger:
       plist = paginator.page(1)
    except EmptyPage:
       plist = paginator.page(paginator.num_pages)
    return plist


@login_required
def list_all_members(request):

    ''' list all members on Right Arm '''

    members = Member.objects.all().exclude(user=request.user)
    return render(request, 'social/list_all_members.html', locals())

@login_required
def request_connection(request):

    ''' accept connection request, cancel sent request(deletes record from table), remove connection '''

    action_id = int(request.GET.get('action_id'))
    action = request.GET.get('action')
    mem_obj = Member.objects.get(id=action_id)
    user = User.objects.get(id=request.user.id)
    from_obj = Member.objects.get(user=user)
    mr_obj = MemberRelation.objects.filter(from_id=from_obj, to_id=mem_obj)
    if not mr_obj:
        mr_obj = MemberRelation.objects.filter(from_id=mem_obj , to_id=from_obj)
    if not mr_obj and action == 'connection_request':
        mr_obj = MemberRelation.objects.create(relation_type="Pending", from_id=from_obj, to_id=mem_obj)
        mr_obj.save()
    elif mr_obj and action == "connection_request":
        mr_obj[0].from_id = from_obj
        mr_obj[0].to_id = mem_obj
        mr_obj[0].relation_type = 'Pending'
    elif action == 'cancel':
        mr_obj = mr_obj[0]
        mr_obj.delete()
    elif action == 'disconnect':
        mr_obj[0].relation_type = 'Removed'
    elif action == 'accept':
        mr_obj[0].relation_type = 'Connected'
    if type(mr_obj) == django.db.models.query.QuerySet and not action == 'cancel':
        mr_obj[0].save()

    if request.GET.get('path', '') == 'from_others_profile':
        return render(request, 'social/others_profile_div.html', locals())

    return HttpResponseRedirect('/social/my-connections/')

@login_required
def friend_requests(request):

    ''' Display all connection requests for the user '''

    member_obj = Member.objects.filter(user__email=request.user)
    if member_obj:
        members_list = MemberRelation.objects.filter(relation_type='Pending', to_id=member_obj)
    return render(request, 'social/friend_requests.html', locals())

@login_required
def send_message(request):

    ''' send message to any member on RA. This view makes use of 2 models 'Messages' and 'Attachments' '''

    user = request.user
    to_member = str(request.POST.get('to_member', ''))
    msg = ""
    success = False
    msg_to_obj = None
    if request.method == "POST":
        form1 = Send_Message_Form(request.POST, request.FILES)
        form2 = Attachments_Form(request.POST, request.FILES)
        if form1.is_valid() and form2.is_valid():
            try:
                msg_to_obj = Member.objects.get(id=int(to_member))
            except:
                pass
            if msg_to_obj:
                msg_from_obj = Member.objects.get(user=request.user)

                msg_obj1 = Messages.objects.create(profile=msg_from_obj, subject=request.POST.get('subject', ''), status="success", msg_type='sent', msg_from=msg_from_obj, msg_to=msg_to_obj, message=request.POST['message'])
                msg_obj2 = Messages.objects.create(profile=msg_to_obj, subject=request.POST.get('subject', ''), status="success", msg_type='received', msg_from=msg_from_obj, msg_to=msg_to_obj, message=request.POST['message'])
                ct_obj = ContentType.objects.get_for_model(Messages)

                if request.FILES.get("attachment", ''):
                        Attachments.objects.create(content_type=ct_obj, object_id=msg_obj1.id, file_attachment=request.FILES.get('attachment'))
                        Attachments.objects.create(content_type=ct_obj, object_id=msg_obj2.id, file_attachment=request.FILES.get('attachment'))

                success  = True
                msg = "Message send successfully"
            else:
                success = False
                msg = "Member with this uesrname/email does not exists on RightArm"
        else:
            msg = [i for i in form1.errors]
    response = {'msg':msg, 'success':success}
    return HttpResponse(json.dumps(response), mimetype="application/json")

def send_message_popup(request):

    user = request.user
    msg_to_obj = Member.objects.get(id=int(request.GET.get('to_id')))
    if request.method == "POST":
        form = Send_Message_Form(request.POST, request.FILES)
        if form.is_valid() :
            msg_from_obj = Member.objects.get(user=request.user)
            msg_obj1 = Messages.objects.create(profile=msg_from_obj, subject=request.POST.get('subject', ''), status="success", msg_type='sent', msg_from=msg_from_obj, msg_to=msg_to_obj, message=request.POST['message'])
            msg_obj2 = Messages.objects.create(profile=msg_to_obj, subject=request.POST.get('subject', ''), status="success", msg_type='received', msg_from=msg_from_obj, msg_to=msg_to_obj, message=request.POST['message'])
            ct_obj = ContentType.objects.get_for_model(Messages)

            if request.FILES.get("attachment", ''):
                Attachments.objects.create(content_type=ct_obj, object_id=msg_obj1.id, file_attachment=request.FILES.get('attachment', ''))
                Attachments.objects.create(content_type=ct_obj, object_id=msg_obj2.id, file_attachment=request.FILES.get('attachment', ''))
            record_added  = True
    else:
        subject = ''
        if request.GET.get("reply_id", ''):
            msg_obj = Messages.objects.get(id=int(request.GET['reply_id']))
            subject = msg_obj.subject
        form = Send_Message_Form(initial={'subject':subject})
    return render(request, 'social/popup-message.html', locals())

@login_required
def message_inbox(request):

    ''' display all received messages from members '''

    mem_obj = Member.objects.get(user=request.user)
    msg_list = Messages.objects.filter(profile=mem_obj, msg_type='received').order_by('-created_on')
    total_messages = msg_list.count()
    new_msgs = Messages.objects.filter(seen=False, profile=mem_obj, msg_type='received').count()
    #msg_list = pagination(request,msg_list)
    tot_list1 = Messages.objects.filter(msg_to = mem_obj, msg_type='received').order_by('-delivered_on')
    tot_list1 = list(tot_list1.values_list('msg_from', flat='true').distinct())
    tot_list2 = Messages.objects.filter(msg_from = mem_obj, msg_type='sent').order_by('-delivered_on')
    tot_list2 = list(tot_list2.values_list('msg_to', flat='true').distinct())
    tot_list1.extend(tot_list2)
    tot_list = list(set(tot_list1))
    final_list = []
    for i in tot_list:
        msg1 = Messages.objects.filter(msg_from__id = i, msg_to = mem_obj, msg_type="received" )
        msg2 = Messages.objects.filter(msg_from = mem_obj, msg_to__id=i,  msg_type="sent" )
        msg = msg1 | msg2  # to concatenate 2 querysets . NOTE - works only for querysets from same table
        msg = msg.order_by("-delivered_on")
        final_list.append(msg[0])
    tot_msg = final_list
    tot_msg = pagination(request,tot_msg)
    return render(request, 'social/message_inbox.html', locals())

@login_required
def get_conversation(request):
    from_id = request.GET.get('from_id')
    to_id = request.GET.get('to_id')
    msg1 = Messages.objects.filter(msg_from__id = int(from_id), msg_to__id = int(to_id), msg_type="sent" )
    msg2 = Messages.objects.filter(msg_from__id = int(to_id), msg_to__id = int(from_id),  msg_type="received" )
    msg = msg1 | msg2  # to concatenate 2 querysets . NOTE - works only for querysets from same table
    msg = msg.order_by("-delivered_on")
    return render(request, 'social/conversation.html', locals())


@login_required
def mark_seen(request):

    ''' change the status from unseen(False) to seen(True) when user clicks on view message '''

    msg_id = request.GET.get('msg_id', None)
    msg_obj = Messages.objects.get(id=int(msg_id))
    msg_obj.seen = True
    import datetime
    msg_obj.seen_at = datetime.datetime.now()
    msg_obj.save()
    return HttpResponse(None)

@login_required
def view_all_messages_to_and_from_member(request):

    ''' display all messages sent and received from specific user  '''

    member_id2 = request.GET.get('user_id2')
    member2 = Member.objects.get(id=int(member_id2))
    user_mem_obj = Member.objects.get(user=request.user)
    msg_list = Messages.objects.filter(msg_from__in=[user_mem_obj, member2], msg_to__in=[user_mem_obj, member2], profile=user_mem_obj).order_by('-created_on')
    return render(request, 'social/view_all_messages_to_and_from_specific_user.html', locals())

def about_us(request):
    return render(request, 'about_us.html', locals())

def my_profile(request):

    mem_obj, created = Member.objects.get_or_create(user=User.objects.get(id=request.user.id))
    msg_list = Messages.objects.filter(profile=mem_obj, msg_type='received').order_by('-created_on')
    total_messages = msg_list.count()
    if request.GET.get('key') == 'latest_10' and msg_list.count() > 10:
        msg_list = msg_list[0:10]
    members = Member.objects.all().exclude(user=request.user)
    unread_msgs = Messages.objects.filter(profile=mem_obj, msg_type='received', seen=False).order_by('-created_on').count()
    return render(request, 'social/my_profile.html', locals())

def refresh_new_messages_div(request):

    mem_obj = Member.objects.get(user=request.user)
    unread_msgs = Messages.objects.filter(profile=mem_obj, msg_type='received', seen=False).order_by('-created_on').count()
    return HttpResponse('(<h3 style="font-size: smaller;display: inline">' + str(unread_msgs) + ' Unread</h3>)')

def my_connections(request):

    mem_obj = Member.objects.get(user=request.user)
    connected_members1 = MemberRelation.objects.filter(to_id=mem_obj, relation_type='Connected')
    connected_members2 = MemberRelation.objects.filter(from_id=mem_obj,  relation_type='Connected')
    connected_list = pagination(request,connected_members2)
    return render(request, 'social/my_connections.html', locals())


def pending_connections(request):

    mem_obj = Member.objects.get(user=request.user)
    pending_members1 = MemberRelation.objects.filter(to_id=mem_obj, relation_type='Pending') # pending received requests
    pending_members2 = MemberRelation.objects.filter(from_id=mem_obj, relation_type='Pending') # pending sent requests
    pending_members2 = pagination(request,pending_members2)
    return render(request, 'social/pending_connections.html', locals())

def view_others_profile(request):

    if request.user.is_authenticated():
        new_msgs_count = 0
        new_connections_count = 0
        #user_obj = User.objects.get(username=request.user.email)
        try:
            user_obj = User.objects.get(username=request.user.username)
        except:
            user_obj = User.objects.get(email=request.user.email)

        mem_obj = Member.objects.get(user=user_obj)
        new_msgs_list = Messages.objects.filter(profile=mem_obj,seen=False, msg_type='received').order_by('-created_on')
        new_msgs_count = len(new_msgs_list)
        new_connections_list = MemberRelation.objects.filter(to_id=mem_obj, relation_type='Pending')
        new_connections_count = len(new_connections_list)
        notifications = int(new_msgs_count) + int(new_connections_count)
    view_profile_id = request.GET.get('view_id')
    mem_obj = Member.objects.get(id=int(view_profile_id))

    return render(request, 'social/view_others_profile.html', locals())

from basemodule.models import Skills
def edit_profile_details(request):
    mem_obj = Member.objects.get(user=request.user)
    mem_skill = Member_Skill.objects.filter(member=mem_obj)
    if mem_obj.get_address_obj():
        address_obj = mem_obj.get_address_obj()
    else:
        cont = ContentType.objects.get_for_model(Member)
        addressobj = Address.objects.create(content_type = cont, object_id = mem_obj.id, email = mem_obj.user.email)
        address_obj = mem_obj.get_address_obj()
    skills_list = request.POST.get('skills', '').split(',')
    skills_list = list(set(skills_list)) # set eleminates duplicates and returns dict,so converted to list
    previous_skills = mem_obj.skills.all()
    if request.POST.get('skills', '') != 'Edit Skills' and request.POST.get('skills', '') != '':
        for skill in skills_list:
            if slugify(skill):
                skill_obj, created = Member_Skill.objects.get_or_create(member = mem_obj,
                                                                skill = skill,
                                                                slug = slugify(skill)
                                                               )
    if request.POST.get('email', '') != 'Edit Email' and request.POST.get('email', '') != '':
        email_exists = ""
        try:
            email_exists = User.objects.filter(email=request.POST['email']).exclude(id=request.user.id)
        except:
            pass
        if not email_exists:
            mem_obj.user.email = str(request.POST.get('email', ''))
        else:
            email_exists_msg = 'Email already exists'
    if request.POST.get('mobile', '') != 'Edit Mobile' and request.POST.get('mobile', '') != '':
        address_obj.primary_contact_no = str(request.POST.get('mobile', ''))
    if request.POST.get('location', '') != 'Edit Location' and request.POST.get('location', '') != '':
        address_obj.address1 = str(request.POST.get('location', ''))

    address_obj.save()
    mem_obj.user.save()
    mem_obj.save()

    return render(request, 'social/edit_profile_details.html', locals())


def delete_skill(request):
    skill_id = request.GET.get('sk')
    sk_obj = Member_Skill.objects.get(pk = int(skill_id))
    sk_obj.delete()
    return HttpResponseRedirect('/user-profile/')


def search_results(request):

    search_word = request.GET.get('search_word', '')
    members_list = Member.objects.filter(Q(user__first_name__icontains=search_word) | Q(user__last_name__icontains=search_word)| Q(user__username__icontains=search_word), is_active=2 ).exclude(pk = request.user.id)
    return render(request, 'social/search_results.html', locals())

#----------------Search Location for Profile & Challange ----------------------------#

def search_location(request):
    city = request.GET.get('search_val','')
    city_list = Boundary.objects.filter(name__startswith = city, level = 1).values('name','parent__name')
    return render(request, 'social/location.html', locals())


def edit_profile_photo(request):

    form = EditProfilePhotoForm()
    mem_obj = Member.objects.get(id = int(request.GET.get('edit_id')))
    if request.method == "POST":
        form = EditProfilePhotoForm(request.POST, request.FILES)
        if request.POST.get('clear_image', '') == 'on':
            mem_obj.photo = ''
            mem_obj.save()
            success = True
        elif form.is_valid():
            mem_obj.photo = request.FILES.get('photo', '')
            success = True
            mem_obj.save()

    return render(request, 'social/edit_profile_photo.html', locals())


from uuid import uuid4
def userid():
   return uuid4().hex[:8]

@login_required
def social_accounts_invite_friends(request):

    ''' Invite friends from social accounts '''
    msg ,friend_email = '' , ''
    if request.method == "POST":
        ct_list = request.POST.get('contact_list')
        if ct_list:
            ct_list = ct_list.split(',')
            user_obj = request.user
            mem_obj = Member.objects.get(user = user_obj)
            email_list = []
            email_name = []
            for ct in ct_list:
                frobj = ct.split('<')
                friend_name = frobj[0]
                try:
                    if frobj[1]:
                        friend_email = frobj[1].replace(">","")
                    else:
                        friend_email = frobj[0]
                except:
                    friend_email = frobj[0]
                    pass
                email_list.append(str(friend_email))
                email_name.append(str(friend_name))
                uid = userid()
                rfu = Refer_Friend_Userdata.objects.filter(hash_value = uid).exists()
                if not rfu:
                    if not Refer_Friend.objects.filter(referred = mem_obj,\
                                                    friend_name = friend_name,
                                                    friend_email = friend_email,
                                                ).exists():
                        robj = Refer_Friend.objects.create(referred = mem_obj,
                                                friend_name = friend_name,
                                                friend_email = friend_email,
                                                )
                        rf_obj = Refer_Friend_Userdata.objects.create(
                                                        referrer = robj,
                                                        friend_email = friend_email,
                                                        hash_value = userid()
                                                        )
            d1 = dict(zip(email_name,email_list))
            if email_list:
                for name,to in d1.iteritems():
                    send_mail('Join the RightArm Community!',
                    'Dear '+str(name)+'\n\n\n'+
                    '\tI have just joined RightArm, a platform for people to come together to give and do good to make the world a better place. The RightArm Community will bring together Issues or Problems that need to be addressed and people collaborate and work to address the Issue and support change. I really feel that you would love to be a part of RightArm. You can visit their site and sign up just like I did to start the process of "Giving" and "Receiving"!'+'\n\nVisit http://rightarm.com \n\n\n' + 'Thanks\n'+str(request.user.first_name)+'',
                    'amolpachpute94@gmail.com',[to], fail_silently=False)
                    #send_mass_mail('Right Arm Invitation', 'http://rightarm.mahiti.org', 'harish.t.m@mahiti.org',[email_list])
                    success = True
                msg = "Invitation E-mail sent "
            response = {'msg':msg, 'success':success}
            return HttpResponse(json.dumps(response), mimetype="application/json")
        else:
            msg = "Select the contact list"

    return render(request, 'social/social_accounts_invite_friends.html', locals())










"""

@login_required
def social_accounts_invite_friends(request):

    ''' Invite friends from social accounts '''
    msg ,friend_email = '' , ''
    if request.method == "POST":
        ct_list = request.POST.get('contact_list')
        if ct_list:
            ct_list = ct_list.split(',')
            user_obj = request.user
            mem_obj = Member.objects.get(user = user_obj)
            email_list = []
            for ct in ct_list:
                frobj = ct.split('<')
                friend_name = frobj[0]
                try:
                    if frobj[1]:
                        friend_email = frobj[1].replace(">","")
                    else:
                        friend_email = frobj[0]
                except:
                    friend_email = frobj[0]
                    pass
                email_list.append(str(friend_email))
                uid = userid()
                rfu = Refer_Friend_Userdata.objects.filter(hash_value = uid).exists()
                if not rfu:
                    if not Refer_Friend.objects.filter(referred = mem_obj,\
                                                    friend_name = friend_name,
                                                    friend_email = friend_email,
                                                ).exists():
                        robj = Refer_Friend.objects.create(referred = mem_obj,
                                                friend_name = friend_name,
                                                friend_email = friend_email,
                                                )
                        rf_obj = Refer_Friend_Userdata.objects.create(
                                                        referrer = robj,
                                                        friend_email = friend_email,
                                                        hash_value = userid()
                                                        )
            if email_list:
                for to in email_list:
                    send_mail('Join the RightArm Community!',
                    'Dear '+str(to)+'\n\n\n'+
                    '\tI have just joined RightArm, a platform for people to come together to give and do good to make the world a better place. The RightArm Community will bring together Issues or Problems that need to be addressed and people collaborate and work to address the Issue and support change. I really feel that you would love to be a part of RightArm. You can visit their site and sign up just like I did to start the process of "Giving" and "Receiving"!'+'\n Visit http://dev.rightarm.mahiti.org \n\n\n' + 'Thanks \n RightArm Team',
                    'amolpachpute94@gmail.com',[to], fail_silently=False)
                    #send_mass_mail('Right Arm Invitation', 'http://rightarm.mahiti.org', 'harish.t.m@mahiti.org',[email_list])
                    success = True
                msg = "Invitation E-mail sent "
            response = {'msg':msg, 'success':success}
            return HttpResponse(json.dumps(response), mimetype="application/json")
        else:
            msg = "Select the contact list"

    return render(request, 'social/social_accounts_invite_friends.html', locals())

"""

def msg_to_search(request):

    mem_obj = Member.objects.get(user=request.user)
    search_word = request.GET.get('search_word', '' )

    connected_members2 = MemberRelation.objects.filter(Q(to_id__user__first_name__icontains=search_word) | \
                                                       Q(to_id__user__last_name__icontains=search_word), from_id=mem_obj, \
                                                        relation_type='Connected')
    connected_members1 = MemberRelation.objects.filter(Q(from_id__user__first_name__icontains=search_word) | \
                                                       Q(from_id__user__last_name__icontains=search_word),to_id=mem_obj,  \
                                                        relation_type='Connected')
    return render(request, 'social/msg_to_search_results.html', locals())

def add_name(request):

    mem_obj = Member.objects.get(user=request.user)
    form = Add_Name_Form()
    if request.method == "POST":
        form = Add_Name_Form(request.POST)
        if form.is_valid():
            mem_obj.user.first_name = request.POST.get('first_name', '')
            mem_obj.user.last_name = request.POST.get('last_name', '')
            mem_obj.user.save()
            record_added = True
    return render(request, 'social/add_name.html', locals())

def update_notifications_div(request):

    if request.user.is_authenticated():
        new_msgs_count = 0
        new_connections_count = 0
        #user_obj = User.objects.get(username=request.user.email)
        if User.objects.filter(username=request.user.email):
            user_obj = User.objects.get(username=request.user.email)
        else:
            user_obj = User.objects.get(username=request.user.username)
        mem_obj = Member.objects.get(user=user_obj)
        new_msgs_list = Messages.objects.filter(msg_to=mem_obj,seen=False, msg_type='received').order_by('-created_on')
        new_msgs_count = len(new_msgs_list)
        new_connections_list = MemberRelation.objects.filter(to_id=mem_obj, relation_type='Pending')
        new_connections_count = len(new_connections_list)
        notifications = int(new_msgs_count) + int(new_connections_count)

    response = {'notifications':notifications, 'new_connections_count':new_connections_count, 'new_msgs_count':new_msgs_count}
    return HttpResponse(json.dumps(response), mimetype="application/json")

@csrf_exempt
def invite_friends(request):
    success = False
    selected_contacts = request.POST.values()
    invitation_template = get_template('social/invitation.html')
    context = Context({'user': request.user})
    mail_message = invitation_template.render(context)
    if selected_contacts:
        for i in request.POST.values():
            em_obj = EmailMessage('Join the RightArm Community!', mail_message, 'webmaster@rightarm.com',[str(i)],headers = {'Reply-To': 'webmaster@rightarm.com'})
            em_obj.content_subtype = "html"
            em_obj.send()
        success = True


    return render(request, "social/invite.html", locals())