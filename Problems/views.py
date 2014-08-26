from django.shortcuts import render_to_response, get_object_or_404, render
from django.template import Context, loader, RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.contenttypes.models import ContentType
import json
from Problems.models import *
from django.http import HttpResponse
import os
from uuid import uuid4
from datetime import *
#from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.forms.fields import DateField
from django.template.defaultfilters import slugify
#from collections import OrderedDict
from Problems.forms import *
from django.core.mail import send_mail,EmailMessage
from Social.models import *
from Member.models import *
from django.template import Context
from django.template.loader import get_template



def manage_challange(request):
    giver_all = GiverMaster.objects.filter(parent=None,active=2)
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
    msg , success = '', False
    country_list = Boundary.objects.filter(active=2,level=0)
    task = request.GET.get('task')
    form1 = ChallengeForm()
    form2 = ChallengeKeywordsForm()
    form3 = AddressForm()
    form4 = OtherContactsForm()
    sbscript, alert_msg = '', ''
    if 'show_msg' in request.session.keys():
        alert_msg = request.session.get('alert_msg')
        sbscript = """
                <script>
                    $(document).ready(function(){
                        alert('%s');
                        window.location.reload();
                    });
                </script>
            """ %(alert_msg)
        del request.session['show_msg']
        del request.session['alert_msg']
    if task == 'receiver':
        if request.method == "POST":
            form1 = ChallengeForm(request.POST, request.FILES)
            form2 = ChallengeKeywordsForm(request.POST)
            form3 = AddressForm(request.POST)
            form4 = OtherContactsForm(request.POST)
            if form1.is_valid() and form2.is_valid() and form3.is_valid():
                user_obj = User.objects.get(id=request.user.id)
                mem_obj = Member.objects.get(user = user_obj)
                chal_obj = Challenge.objects.create(description=request.POST.get('description'),
                                video=request.POST.get('video'),
                                created_by = mem_obj,
                                updated_by = mem_obj,
                                )
                count = int(request.POST.get('bcount')) if request.POST.get('bcount') else 1
                for i in range(0,count+1):
                    var = request.POST.get('city'+str(i))
                    try:
                        city_coutry = var.split(',')
                        con1 = city_coutry[1] if city_coutry[1] else ''
                    except:
                        con1 = ''
                    try:
                        if city_coutry[0] and con1:
                            other_ct_obj = OtherContacts.objects.create(
                                        name=request.POST.get('fname'+str(i)) if request.POST.get('fname'+str(i)) else None,
                                        mobile=request.POST.get('mobile'+str(i)) if request.POST.get('mobile'+str(i)) else None,
                                        city = city_coutry[0] if city_coutry[0] else '',
                                        country = city_coutry[1] if city_coutry[1] else '',
                                        content_type=ContentType.objects.get_for_model(Challenge),
                                        object_id = chal_obj.id
                                    )
                        else:
                            if request.POST.get('fname'+str(i)) or request.POST.get('mobile'+str(i)) or city_coutry[0]:
                                other_ct_obj = OtherContacts.objects.create(
                                    name=request.POST.get('fname'+str(i)) if request.POST.get('fname'+str(i)) else None,
                                    mobile=request.POST.get('mobile'+str(i)) if request.POST.get('mobile'+str(i)) else None,
                                    city = city_coutry[0] if city_coutry[0] else '',
                                    country = '',
                                    content_type=ContentType.objects.get_for_model(Challenge),
                                    object_id = chal_obj.id
                                    )
                    except Exception as e:
                        pass
                keys = request.POST.get('keywords')
                key_list = keys.split(',')
                f = form2.save(commit=False)
                for i in key_list:
                    c = ChallengeKeywords.objects.create(name = i)
                    chal_obj.keywords.add(c)
                #chal_obj.beneficiary.add(other_ct_obj)
                #f.short_desc = request.POST.get('short_desc')
                f3 = form3.save(commit=False)
                f3.content_type = ContentType.objects.get_for_model(Challenge)
                f3.object_id = chal_obj.id
                f3.primary_contact_no = request.POST.get('primary_contact_no')
                f3.save()
                to_mail = request.POST.get('email') if request.POST.get('email') else request.user.email
                description = request.POST.get('description')
                select_catagory = request.POST.get('select_catagory')
                msg = "Issue submitted successfully. We will revert back in 3 working days"
                success = True
                template3 = get_template('signature.html')
                #context = Context({'user': user, 'username':username, 'password': password})
                mail_signature = template3.render(Context({}))
                try:
                    email_obj = EmailMessage('We have received your Issue submission!',
                        'Dear '+str(request.user.first_name)+','+'<br/>'+'We, at RightArm are thankful to you for submitting the following Issue:'+'<br/><br/>'+ "" + "\""+description+"\"" + "" +
                        '<br/><br/>We highly appreciate your spirit of identifying and raising issues which needs to be addressed for making lives better for many.<br/><br>We will get into the details of the issue submitted by you and at an opportune time align Givers and Moderators and convert the same into a project and will keep you updated.<br/><br/>We also appreciate your choosing to be '+select_catagory+' for the same.<br/><br/>Meanwhile, we request you to keep visiting our website and keep contributing by making suggestions .<br/><br/>Please also Invite your friends to visit RightArm and join us for making a difference to the world we live in.<br/><br/><br/>' + mail_signature,
                        'webmaster@rightarm.com',[to_mail], headers = {'Reply-To': 'webmaster@rightarm.com'})
                    email_obj.content_subtype = "html"
                    email_obj.send()
                except:
                    pass
                request.session['show_msg'] = True
                request.session['alert_msg'] = msg
                return HttpResponseRedirect('/problems/challenge/')
        else:
            msg = "Invlaid request"
    elif task == 'giver':
        if request.method == "POST":
            keys = request.POST.get('keywords')
            giver_category = request.POST.getlist('giver_category')
            category_values = request.POST.getlist('category_values')
            all_list = []
            all_list = giver_category + category_values
            donation_list = GiverMaster.objects.filter(id__in = all_list)
            user_obj = User.objects.get(id=request.user.id)
            mem_obj = Member.objects.get(user = user_obj)
            giver_obj = Giver.objects.create(member = mem_obj)
            for i in donation_list:
                giver_obj.givermaster.add(i)
            giver_obj.giver_keywords = keys
            giver_obj.save()
            msg = "Giver details submit successfully"
            success = True
    return render_to_response('Challenge.html', locals(), context_instance = RequestContext(request))






