# Create your views here.
from django.shortcuts import render
from usermanagement.forms import *
from django.contrib.auth import authenticate, login ,logout
from django.http import HttpResponse, HttpResponseRedirect, Http404
from Projects.models import *
from usermanagement.models import *
from Social.models import *
from basemodule.models import *
from django.template.defaultfilters import slugify
from anonymous.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import REDIRECT_FIELD_NAME
#from social.actions import do_auth
from django_user_agents.utils import get_user_agent
import json
from Problems.models import *
from Problems.forms import *
from forums.models import *
from  RightArmCms.models import *
from django.core.mail import send_mail, EmailMessage
from django.template import Context
from django.template.loader import get_template

def generate_password(size):
    import random
    import string
    return "".join([random.choice(string.lowercase) for i in range(0,4)]) + "".join([random.choice(string.digits) for i in range(0,4)])



def user_login(request):

    """ Login function for member/superuser. If user is not superuser his record
    should be in User_Roles model then only he can log in """

    form = LOGIN_FORM()
    error_msg = ""
    success = False
    if request.method == "POST":
        form = LOGIN_FORM(request.POST)
        if form.is_valid():
            email = request.POST.get('username')

            password = request.POST.get('password')
            #post_data = request.POST.copy()
            #print "POST DATA===========>",post_data
            userobj = User.objects.filter(email=email, is_active = True)
            if userobj:
                user = userobj[0]
                valid_pwd = user.check_password(password)
                if valid_pwd:
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    login(request, user)
                    response = {'success':True}
                    return HttpResponse(json.dumps(response), mimetype="application/json")
                    #if not user.is_superuser:
                    #    #try:
                    #    #    user_role = User_Roles.objects.get(user = user)
                    #    #    if user_role.role_type.all():
                    #    #        login(request, user)
                    #    #        response = {'success':True}
                    #    #        return HttpResponse(json.dumps(response), mimetype="application/json")
                    #    #        #return HttpResponseRedirect('/user-profile/')
                    #    #    else:
                    #    #        error_msg = "You are not an authorized person"
                    #    #except:
                    #    #    error_msg = "You are not an authorized person"
                    #else:
                    #    detect_device_info(request, user)
                    #    login(request, user) # direct login for super_user
                    #    response = {'success':True}
                    #    return HttpResponse(json.dumps(response), mimetype="application/json")
                    #    #return HttpResponseRedirect('/user-profile/')
                else:
                    error_msg = "Authentication failure"
            else:
                error_msg = 'User is not activated'

    response = {'error_msg':error_msg, 'success':False}
    return HttpResponse(json.dumps(response), mimetype="application/json")


def detect_device_info(request, user):

    ''' this view makes use of get_user_agent class from
    django app named  django_user_agents. This app inserts
    a middleware which adds user_agent object to request
    object for detecting users device, browser, etc '''

    user_agent = get_user_agent(request)
    mem_info_obj = Member_Information()
    mem_obj = Member.objects.get(user=user)
    if user_agent.is_mobile:
        mem_info_obj.type_of_device = 'Mobile'
    if user_agent.is_pc:
        mem_info_obj.type_of_device = 'PC'
    if user_agent.is_tablet:
        mem_info_obj.type_of_device = 'Tablet'
    if user_agent.is_bot:
        mem_info_obj.is_bot = user_agent.is_bot
    mem_info_obj.browser = str(user_agent.browser)
    mem_info_obj.os_info = str(user_agent.os)
    mem_info_obj.member = mem_obj
    mem_info_obj.ip_address = request.META['REMOTE_ADDR']

    mem_info_obj.save()

    return None

@login_required
def social_account_login_or_sign_up(request):

    ''' User login or sign up using his social accounts i.e facebook, linkedIn or Gmail '''

    user = ""
    username = request.user.username
    if not username:
        username = request.user.first_name + request.user.last_name
    users_list = User.objects.filter(email = request.user.email).order_by("id")

    if users_list.count() > 1: # if user already exists
        for i in range(1,users_list.count()):
                users_list[i].delete()

        member_obj, created1 = Member.objects.get_or_create(user_type='Member', user=users_list[0])
        user = member_obj.user
        #member_obj2, created2 = Member.objects.get_or_create(user_type='Member', user=users_list[1])
        if created1:
            con_typ = ContentType.objects.get_for_model(member_obj)
            address = Address.objects.get_or_create(content_type = con_typ, object_id = member_obj.id, email = member_obj.user.email )

    else:
        member_obj, created = Member.objects.get_or_create(user_type='Member', user=users_list[0])
        user = member_obj.user
        if created:
            password = generate_password(8)
            user.set_password(password)
            user.save()
            template3 = get_template('social/social_registration_mail.html')
            context = Context({'user': user, 'username':username, 'password': password})
            mail_message = template3.render(context)
            em_obj = EmailMessage('RightArm Credentials', mail_message, 'webmaster@rightarm.com',[user.email],headers = {'Reply-To': 'webmaster@rightarm.com'})
            em_obj.content_subtype = "html"
            em_obj.send()

            con_typ = ContentType.objects.get_for_model(member_obj)
            address = Address.objects.get_or_create(content_type = con_typ, object_id = member_obj.id, email = member_obj.user.email )

    if user:
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        return HttpResponseRedirect('/user-profile/')
    form = LOGIN_FORM()
    return render(request, 'usermanagement/login.html', locals())



def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required
def done(request):
    """
    User has linked account successfully. This view is called after a new user
    signs up through Linkedin.
    """
    details = request.user.social_auth.get().extra_data
    # extra_data is the json formatted linkedin profile of the user, and
    # Prospect is our custom user profile model, one-to-one with
    # `django.contrib.auth.User`. It knows how to convert the JSON in
    # extra_data into individual attributes of the Prospect.
    new_prospect = (Prospect.objects
                    .create_from_linkedin_data(request.user, details))
    return HttpResponseRedirect(reverse('show_prospect',
                                        kwargs={'id': new_prospect.id}))


def check_user(request):

    user_exists = User.objects.filter(email=request.GET.get('email',''))
    success = True
    msg = ''
    if user_exists:
        msg = 'User with this mail already exists'
        success = False
    response = {'msg':msg, 'success':success}
    return HttpResponse(json.dumps(response), mimetype="application/json")



def home(request):

    ''' Member homepage with all details related to the project he is connected with,list all projects ,friend requests '''
    #projects = Project.objects.all()
    #member_obj = Member.objects.filter(user=request.user)
    #if member_obj:
    #    request_count = MemberRelation.objects.filter(relation_type='Pending', to_id=member_obj).count()
    country_list1 = list(Boundary.objects.filter(active=2,level=0).exclude(name__icontains='Singapore'))
    country_list = list(Boundary.objects.filter(name='Singapore', level=0))
    country_list.extend(country_list1)
    return render(request, 'index.html', locals())

def user_profile(request):

    ''' Member homepage '''

    new_msgs_count = 0
    new_connections_count = 0
    connections = False
    try:
        user_obj = User.objects.get(email=request.user.email)
        mem_obj, created = Member.objects.get_or_create(user_type='Member', user=user_obj)
    except:
        pass
    msg_list = Messages.objects.filter(profile=mem_obj, msg_type='received').order_by('-created_on')
    new_msgs_list = [i for i in msg_list if i.seen == False]
    new_msgs_count = len(new_msgs_list)
    new_connections_list = MemberRelation.objects.filter(to_id=mem_obj, relation_type='Pending')
    new_connections_count = len(new_connections_list)
    notifications = int(new_msgs_count) + int(new_connections_count)
    if request.GET.get('base_notifications', ''):
        return HttpResponse(notifications);

    mem_obj = Member.objects.get(user=request.user)
    mem_skill = Member_Skill.objects.filter(member=mem_obj)

    connected_members1 = MemberRelation.objects.filter(to_id=mem_obj, relation_type='Connected')
    connected_members2 = MemberRelation.objects.filter(from_id=mem_obj,  relation_type='Connected')
    if connected_members1 or connected_members2:
        connections = True
    return render(request, 'usermanagement/profile.html', locals())



def has_changed(instance, field):
    if not instance.pk:
        return False
    old_value = instance.__class__._default_manager.\
        filter(pk=instance.pk).values(field).get()[field]
    return not getattr(instance, field) == old_value



def configure(request, key=''):
    item_list = []
    if key == '':
        key = request.GET.get('key')
    if key == "salutations":
        item_list = Salutation.objects.all()
    if key == "communicationtype":
        item_list = CommType.objects.all()
    if key == "skills":
        item_list = Skills.objects.all()
    if key == "tags":
        item_list = Tags.objects.all()
    if key == "projectcategory":
        item_list = Project_Category.objects.all()
    if key == "problemcategory":
        item_list = Problem_Category.objects.all()
    if key == "country":
        item_list = Boundary.objects.filter(level=0)
    if key == "state":
        item_list = Boundary.objects.filter(level=1)
    if key == "district":
        item_list = Boundary.objects.filter(level=2)
    if key == "add-faq-category":
        item_list = FAQ_Category.objects.all()
    if key == "add-question":
        faq_id = request.GET.get('objid','')
        cat_obj = FAQ_Category.objects.get(id=faq_id)
        item_list = Question.objects.filter(category=cat_obj)
    if key == "add-answer":
        ques_id = request.GET.get('objid','')
        ques_obj = Question.objects.get(id=ques_id)
        item_list = Answer.objects.filter(question=ques_obj)
    if key == 'challenge':
        ch_list = Challenge.objects.all()
        item_list = ch_list
    if key == "topic":
        topic_list = Topic.objects.all()
        item_list = topic_list
    if key == 'article':
        article_list = Article.objects.filter(status='PU')
        section_id = request.GET.get('section_name')
        status_name =request.GET.get('status_name')
        section_id = request.GET.get('section_name')
        keyword=request.GET.get('keyword')
        if status_name == "True":
            article_list = article_list.filter(active=True)
        if status_name == "False":
            article_list = article_list.filter(active=False)
        if keyword:
            article_list = article_list.filter(name__istartswith=keyword)
        if section_id:
            article_list = article_list.filter(section__id=section_id)
        section_list = Section.objects.all()
        item_list = article_list
        title = "Article"
    if key == "manage-articles":
        objid = request.GET.get('objid')
        article_lists = Article.objects.filter(id = objid)
        get_article = Article.objects.get(id = objid)
        item_list = article_lists
        title = "Article Items"
        img_title = "Images"
        attach_title = "Attachments"
        link_title = "Links"
        code_title = "Codes"
    if key == "donation_category":
        item_list = GiverMaster.objects.filter(parent = None)
    if key == "donation_type":
        item_list = GiverMaster.objects.exclude(parent=None,active = 2)
    return render(request, 'configure.html', locals())


def add_form(request, form):
    f= form.save(commit=False)
    f.url4SEO = slugify(request.POST.get('name'))
    f.save()


def edit_form(request, form):
    f= form.save(commit=False)
    f.url4SEO = slugify(request.POST.get('name'))
    f.save()


#--------------------------------Configuration --------------------------------------------#

def manage_configure(request, key='', task='',id=''):
    msg = ''
    if key == '':
        key = request.GET.get('key')
    if task == '':
        task = request.GET.get('task')
    if key == "salutations":
        if task == "add":
            form = SalutationForm()
            if request.method == "POST":
                form = SalutationForm(request.POST)
                if form.is_valid():
                    if not Salutation.objects.filter(name__iexact = request.POST.get('name')).exists():
                        add_form(request, form)
                        added = True
                    else:
                        msg = "Salutation name already exists"
                else:
                    form = SalutationForm(request.POST)
            else:
                form = SalutationForm()
        if task == "edit":
            edit=True
            objid = ''
            if objid == "":
                objid = request.GET.get('objid', '')
            sobj = Salutation.objects.get(id=objid)
            form = SalutationForm(instance = sobj)
            if request.method == "POST":
                form = SalutationForm(request.POST, instance = sobj)
                if form.is_valid():
                    if not Salutation.objects.filter(name__iexact=request.POST.get('name')).exclude(id=objid):
                        edit_form(request, form)
                        edit_done = True
                    else:
                        msg = "Salutation name already exists"
                else:
                    msg = "Invalid form data"
        if task == "delete":
            if id == '':
                id = request.GET.get('id')
            obj = Salutation.objects.get(id=id)
            obj.is_active = 0
            obj.save()
            return HttpResponseRedirect('/configure/salutations/')
        if task == "active":
            if id == '':
                id = request.GET.get('id')
            obj = Salutation.objects.get(id=id)
            obj.is_active = 2
            obj.save()
            return HttpResponseRedirect('/configure/salutations/')


#--------------------------------CommType --------------------------------------------#


    if key == "communicationtype":
        if task == "add":
            form = CommTypeForm()
            if request.method == "POST":
                form = CommTypeForm(request.POST)
                if form.is_valid():
                    if not CommType.objects.filter(name__iexact = request.POST.get('name')).exists():
                        add_form(request, form)
                        added = True
                    else:
                        msg = "Communication Type already exists"
                else:
                    form = CommTypeForm(request.POST)
            else:
                form = CommTypeForm()
        if task == "edit":
            edit=True
            objid = ''
            if objid == "":
                objid = request.GET.get('objid', '')
            cobj = CommType.objects.get(id=objid)
            form = CommTypeForm(instance = cobj)
            if request.method == "POST":
                form = CommTypeForm(request.POST, instance = cobj)
                if form.is_valid():
                    if not CommType.objects.filter(name__iexact = request.POST.get('name')).exclude(id=objid):
                        edit_form(request, form)
                        edit_done = True
                    else:
                        msg = "CommunicationType already exists"
                else:
                    msg = "Invalid Form "
        if task == "delete":
            if id == '':
                id = request.GET.get('id')
            obj = CommType.objects.get(id=id)
            obj.is_active = 0
            obj.save()
            return HttpResponseRedirect('/configure/communicationtype/')
        if task == "active":
            if id == '':
                id = request.GET.get('id')
            obj = CommType.objects.get(id=id)
            obj.is_active = 2
            obj.save()
            return HttpResponseRedirect('/configure/communicationtype/')

#-------------------------------------------Skills ---------------------------------------------#

    if key == "skills":
        if task == "add":
            form = SkillsForm()
            if request.method == "POST":
                form = SkillsForm(request.POST)
                if form.is_valid():
                    if not Skills.objects.filter(name__iexact = request.POST.get('name')).exists():
                        add_form(request, form)
                        added = True
                    else:
                        msg = "Skills name already exist "
                else:
                    form = SkillsForm(request.POST)
            else:
                form = SkillsForm()
        if task == "edit":
            edit=True
            objid = ''
            if objid == "":
                objid = request.GET.get('objid', '')
            sobj = Skills.objects.get(id=objid)
            form = SkillsForm(instance = sobj)
            if request.method == "POST":
                form = SkillsForm(request.POST, instance = sobj)
                if form.is_valid():
                    if not Skills.objects.filter(name__iexact = request.POST.get('name')).exclude(id=objid):
                        edit_form(request, form)
                        edit_done = True
                    else:
                        msg = "Skills name already exists"
                else:
                    msg = "Invalid Form"
        if task == "delete":
            if id == '':
                id = request.GET.get('id')
            obj = Skills.objects.get(id=id)
            obj.is_active = 0
            obj.save()
            return HttpResponseRedirect('/configure/skills/')
        if task == "active":
            if id == '':
                id = request.GET.get('id')
            obj = Skills.objects.get(id=id)
            obj.is_active = 2
            obj.save()
            return HttpResponseRedirect('/configure/skills/')

#-------------------------------------------Tags -----------------------------------------------#

    if key == "tags":
        if task == "add":
            form = TagsForm()
            if request.method == "POST":
                form = TagsForm(request.POST)
                if form.is_valid():
                    if not Tags.objects.filter(name__iexact = request.POST.get('name')).exists():
                        add_form(request,form)
                        added = True
                    else:
                        msg = "Tags name already exists"
                else:
                    form = TagsForm(request.POST)
            else:
                form = TagsForm()
        if task == "edit":
            edit=True
            objid = ''
            if objid == "":
                objid = request.GET.get('objid', '')
            tobj = Tags.objects.get(id=objid)
            form = TagsForm(instance = tobj)
            if request.method == "POST":
                form = TagsForm(request.POST, instance = tobj)
                if form.is_valid():
                    if not Tags.objects.filter(name__iexact = request.POST.get('name')).exclude(id=objid):
                        edit_form(request,form)
                        edit_done = True
                    else:
                        msg = "Tags name already exist"
                else:
                    msg = "Invalid form"
        if task == "delete":
            if id == '':
                id = request.GET.get('id')
            obj = Tags.objects.get(id=id)
            obj.is_active = 0
            obj.save()
            return HttpResponseRedirect('/configure/tags/')
        if task == "active":
            if id == '':
                id = request.GET.get('id')
            obj = Tags.objects.get(id=id)
            obj.is_active = 2
            obj.save()
            return HttpResponseRedirect('/configure/tags/')

#-----------------------------------------------Project Category --------------------------------------#

    if key == "projectcategory":
        if task == "add":
            form = ProjectCategoryForm()
            if request.method == "POST":
                form = ProjectCategoryForm(request.POST,request.FILES)
                if form.is_valid():
                    if not Project_Category.objects.filter(name__iexact = request.POST.get('name')).exists():
                        add_form(request,form)
                        added = True
                    else:
                        msg = "Project Category name already exist"
                else:
                    form = ProjectCategoryForm(request.POST,request.FILES)
            else:
                form = ProjectCategoryForm()
        if task == "edit":
            edit=True
            objid = ''
            if objid == "":
                objid = request.GET.get('objid', '')
            pobj = Project_Category.objects.get(id=objid)
            form = ProjectCategoryForm(instance = pobj)
            if request.method == "POST":
                form = ProjectCategoryForm(request.POST, request.FILES, instance = pobj)
                if form.is_valid():
                    if not Project_Category.objects.filter(name__iexact = request.POST.get('name')).exclude(id=objid):
                        edit_form(request,form)
                        edit_done = True
                    else:
                        msg = "Project Category name already exist"
                else:
                    msg = "Invalid form"
        if task == "delete":
            if id == '':
                id = request.GET.get('id')
            obj = Project_Category.objects.get(id=id)
            obj.is_active = 0
            obj.save()
            return HttpResponseRedirect('/configure/projectcategory/')
        if task == "active":
            if id == '':
                id = request.GET.get('id')
            obj = Project_Category.objects.get(id=id)
            obj.is_active = 2
            obj.save()
            return HttpResponseRedirect('/configure/projectcategory/')

#---------------------------------------Problem Category ---------------------------------------------#

    if key == "problemcategory":
        if task == "add":
            form = ProblemCategoryForm()
            if request.method == "POST":
                form = ProblemCategoryForm(request.POST,request.FILES)
                if form.is_valid():
                    if not Problem_Category.objects.filter(name__iexact = request.POST.get('name')).exists():
                        add_form(request,form)
                        added = True
                    else:
                        msg = "Problem categories already exists"
                else:
                    form = ProblemCategoryForm(request.POST,request.FILES)
            else:
                form = ProblemCategoryForm()
        if task == "edit":
            edit=True
            objid = ''
            if objid == "":
                objid = request.GET.get('objid', '')
            pobj = Problem_Category.objects.get(id=objid)
            form = ProblemCategoryForm(instance = pobj)
            if request.method == "POST":
                form = ProblemCategoryForm(request.POST, request.FILES, instance = pobj)
                if form.is_valid():
                    if not Problem_Category.objects.filter(name__iexact = request.POST.get('name')).exclude(id=objid):
                        edit_form(request,form)
                        edit_done = True
                    else:
                        msg = "Problem Category name already exist"
                else:
                    msg = "Invalid form"
        if task == "delete":
            if id == '':
                id = request.GET.get('id')
            obj = Problem_Category.objects.get(id=id)
            obj.is_active = 0
            obj.save()
            return HttpResponseRedirect('/configure/problemcategory/')
        if task == "active":
            if id == '':
                id = request.GET.get('id')
            obj = Problem_Category.objects.get(id=id)
            obj.is_active = 2
            obj.save()
            return HttpResponseRedirect('/configure/problemcategory/')

#-------------------------------------Country --------------------------------------------#

    if key == "country":
        if task == "add":
            form = BoundaryCountryForm()
            if request.method == "POST":
                form = BoundaryCountryForm(request.POST)
                if form.is_valid():
                    if not Boundary.objects.filter(name = request.POST.get('name')).exists():
                        f= form.save(commit=False)
                        f.url4SEO = slugify(request.POST.get('name'))
                        f.level = 0
                        f.save()
                        added = True
                    else:
                        msg = "Country name already exists"
                else:
                    form = BoundaryCountryForm(request.POST)
            else:
                form = BoundaryCountryForm()
        if task == "edit":
            edit=True
            objid = ''
            if objid == "":
                objid = request.GET.get('objid', '')
            countryobj = Boundary.objects.get(id=objid)
            form = BoundaryCountryForm(instance = countryobj)
            if request.method == "POST":
                form = BoundaryCountryForm(request.POST, instance = countryobj)
                if form.is_valid():
                    if not Boundary.objects.filter(name = request.POST.get('name')).exclude(id=objid):
                        f= form.save(commit=False)
                        f.url4SEO = slugify(request.POST.get('name'))
                        f.level = 0
                        f.save()
                        edit_done = True
                    else:
                        msg = "Country name already exists"
                else:
                    msg = "Invalid Form Data"
        if task == "delete":
            if id == '':
                id = request.GET.get('id')
            obj = Boundary.objects.get(id=id)
            obj.active = 0
            obj.save()
            return HttpResponseRedirect('/configure/country/')
        if task == "active":
            if id == '':
                id = request.GET.get('id')
            obj = Boundary.objects.get(id=id)
            obj.active = 2
            obj.save()
            return HttpResponseRedirect('/configure/country/')

#----------------------------------State -------------------------------------------------#

    if key == "state":
        if task == "add":
            form = BoundaryStateForm()
            if request.method == "POST":
                form = BoundaryStateForm(request.POST)
                if form.is_valid():
                    if not Boundary.objects.filter(name = request.POST.get('name'), \
                    parent = int(request.POST.get('country'))).exists():
                        county_id = request.POST.get('country')
                        county_list = Boundary.objects.filter(id = county_id)
                        f = form.save(commit= False)
                        if county_list:
                            f.parent = county_list[0]
                        f.level = 1
                        f.save()
                        added = True
                    else:
                        msg = "State name already exists"
                else:
                    form = BoundaryStateForm(request.POST)
            else:
                form = BoundaryStateForm()
        if task == "edit":
            edit=True
            objid = ''
            if objid == "":
                objid = request.GET.get('objid', '')
            state_obj = Boundary.objects.get(id=objid)
            form = BoundaryStateForm(initial = {'country':state_obj.parent.id,'name':state_obj.name})
            if request.method == 'POST':
                form = BoundaryStateForm(request.POST)
                if form.is_valid():
                    if not Boundary.objects.filter(
                        name__iexact=request.POST.get('name'),
                        parent__id=int(request.POST.get('country'))
                        ).exclude(id=objid).exists():
                        state_obj.name = request.POST.get('name')
                        country_obj = Boundary.objects.get(id=int(request.POST.get('country')))
                        state_obj.parent = country_obj
                        state_obj.save()
                        edit_done = True
                    else:
                        msg = "State name Already exist"
                else:
                    msg = "Invalid Form Data"
        if task == "delete":
            if id == '':
                id = request.GET.get('id')
            obj = Boundary.objects.get(id=id)
            obj.active = 0
            obj.save()
            return HttpResponseRedirect('/configure/state/')
        if task == "active":
            if id == '':
                id = request.GET.get('id')
            obj = Boundary.objects.get(id=id)
            obj.active = 2
            obj.save()
            return HttpResponseRedirect('/configure/state/')

#-------------------------------District -------------------------------------------------#

    if key == "district":
        if task == "add":
            form = BoundaryDistrictForm()
            if request.method == "POST":
                form = BoundaryDistrictForm(request.POST)
                if form.is_valid():
                    if not Boundary.objects.filter(name = request.POST.get('name'), \
                    parent__parent__id = int(request.POST.get('country')), parent__id = int(request.POST.get('state'))).exists():
                        county_id = request.POST.get('country')
                        state_id = request.POST.get('state')
                        county_list = Boundary.objects.filter(id = county_id)
                        state_list = Boundary.objects.filter(id = state_id)
                        f = form.save(commit= False)
                        if state_list:
                            f.parent = state_list[0]
                        if county_list:
                            f.parent.parent = county_list[0]
                        f.level = 2
                        f.save()
                        added = True
                    else:
                        msg = "District name already exists"
                else:
                    form = BoundaryDistrictForm(request.POST)
            else:
                form = BoundaryDistrictForm()
        if task == "edit":
            edit=True
            objid = ''
            if objid == "":
                objid = request.GET.get('objid', '')
            district_obj = Boundary.objects.get(id=objid)
            form = BoundaryDistrictForm(initial = {'country':district_obj.parent.parent.id, \
            'state':district_obj.parent.id,'name':district_obj.name})
            if request.method == 'POST':
                form = BoundaryDistrictForm(request.POST)
                if form.is_valid():
                    if not Boundary.objects.filter(
                        name__iexact=request.POST.get('name'),
                        parent__parent__id=int(request.POST.get('country')),parent__id=int(request.POST.get('state'))
                        ).exclude(id=objid).exists():
                        district_obj.name = request.POST.get('name')
                        country_obj = Boundary.objects.get(id=int(request.POST.get('country')))
                        state_obj = Boundary.objects.get(id=int(request.POST.get('state')))
                        district_obj.parent = state_obj
                        district_obj.parent.parent = country_obj
                        district_obj.save()
                        edit_done = True
                    else:
                        msg = "District name Already exist"
                else:
                    msg = "Invalid Form Data"
        if task == "delete":
            if id == '':
                id = request.GET.get('id')
            obj = Boundary.objects.get(id=id)
            obj.active = 0
            obj.save()
            return HttpResponseRedirect('/configure/district/')
        if task == "active":
            if id == '':
                id = request.GET.get('id')
            obj = Boundary.objects.get(id=id)
            obj.active = 2
            obj.save()
            return HttpResponseRedirect('/configure/district/')
    #return render(request, 'manage_configure.html', locals())



#----------------------------------------FAQ Category -------------------------------------------------------------#


    if key == "add-faq-category":
        if task == "add":
            form = FAQ_CategoryForm()
            if request.method == "POST":
                form = FAQ_CategoryForm(request.POST)
                if form.is_valid():
                    check=FAQ_Category.objects.filter(name__iexact=request.POST.get('name'))
                    if not check:
                        form.save()
                        added = True
                    else:
                        msg= "Category name already exist."
                        form = FAQ_CategoryForm(request.POST)
                        return render(request, 'add_faq_category.html', locals())
                else:
                    form = FAQ_CategoryForm(request.POST)
            else:
                form = FAQ_CategoryForm()
        if task == "edit":
            edit = True
            objid = ''
            if objid == '':
                objid=request.GET.get('objid', '')
            category=FAQ_Category.objects.get(id=objid)
            form = FAQ_CategoryForm(instance=category)
            if request.method == "POST":
                form = FAQ_CategoryForm(request.POST, instance = category)
                if form.is_valid():
                    if not has_changed(instance = category,field='name'):
                        form.save()
                        edit_done = True
                    else:
                        check=FAQ_Category.objects.filter(name__iexact=request.POST.get('name'))
                        if not check:
                            form.save()
                            edit_done = True
                        else:
                            msg= "Category name already exist"
                            form = FAQ_CategoryForm(request.POST,instance = category)
            else:
                form = FAQ_CategoryForm(instance=category)
        if task == "delete":
            if id == '':
                id = request.GET.get('id')
            obj = FAQ_Category.objects.get(id=id)
            obj.is_active = False
            obj.save()
            return HttpResponseRedirect('/configure/add-faq-category/')
        if task == "active":
            if id == '':
                id = request.GET.get('id')
            obj = FAQ_Category.objects.get(id=id)
            obj.is_active = True
            obj.save()
            return HttpResponseRedirect('/configure/add-faq-category/')


#---------------------------------------- Question  -------------------------------------------------------------#

    if key == "add-question":
        if task == "add":
            objid = request.GET.get('objid')
            print "================>",objid
            faq_cat = FAQ_Category.objects.get(id=objid)
            if request.method == "POST":
                form = QuestionForm(request.POST)
                if form.is_valid():
                        check=Question.objects.filter(question__iexact=request.POST.get('question'))
                        if not check:
                            f=form.save(commit=False)
                            f.category = faq_cat
                            f.save()
                            added = True
                        else:
                            msg= "Question already exist."
                            form = Question(request.POST)
                else:
                    form = QuestionForm(request.POST)
            else:
                form = QuestionForm()
        if task == "edit":
            edit = True
            objid=request.GET.get('objid', '')
            question=Question.objects.get(id=objid)
            if request.method == "POST":
                form = QuestionForm(request.POST, instance = question)
                if form.is_valid():
                    form.save()
                    edit_done = True
                else:
                    form = QuestionForm(request.POST)
                    edit = True
            else:
                form = QuestionForm(instance=question)
        if task == "delete":
            if id == '':
                id = request.GET.get('id')
            cat_id = request.GET.get('cat_id')
            obj = Question.objects.get(id=id)
            obj.is_active = False
            obj.save()
            return HttpResponseRedirect('/configure/add-question/?objid='+cat_id)
        if task == "active":
            if id == '':
                id = request.GET.get('id')
            cat_id = request.GET.get('cat_id')
            obj = Question.objects.get(id=id)
            obj.is_active = True
            obj.save()
            return HttpResponseRedirect('/configure/add-question/?objid='+cat_id)

    if key == "add-answer":
        if task == "add":
            objid = request.GET.get('objid')
            ques_cat = Question.objects.get(id=objid)
            if request.method == "POST":
                form = AnswerForm(request.POST)
                if form.is_valid():
                        check=Answer.objects.filter(answer__iexact=request.POST.get('answer'))
                        if not check:
                            f=form.save(commit=False)
                            f.question = ques_cat
                            f.save()
                            added = True
                        else:
                            msg= "Answer already exist."
                            form = Answer(request.POST)
                else:
                    form = AnswerForm(request.POST)
            else:
                form = AnswerForm()
        if task == "edit":
            edit = True
            objid=request.GET.get('objid', '')
            answer=Answer.objects.get(id=objid)
            if request.method == "POST":
                form = AnswerForm(request.POST, instance = answer)
                if form.is_valid():
                    form.save()
                    edit_done = True
                else:
                    form = AnswerForm(request.POST)
                    edit = True
            else:
                form = AnswerForm(instance=answer)
        if task == "delete":
            if id == '':
                id = request.GET.get('id')
            ques_id = request.GET.get('ques_id')
            obj = Answer.objects.get(id=id)
            obj.is_active = False
            obj.save()
            return HttpResponseRedirect('/configure/add-answer/?objid='+ques_id)
        if task == "active":
            if id == '':
                id = request.GET.get('id')
            ques_id = request.GET.get('ques_id')
            obj = Answer.objects.get(id=id)
            obj.is_active = True
            obj.save()
            return HttpResponseRedirect('/configure/add-answer/?objid='+ques_id)

#---------------------------------------- Challange  -------------------------------------------------------------#

    if key == 'challenge':
        if task == "edit":
            edit = True
            objid=request.GET.get('objid', '')
            ch_obj=Challenge.objects.get(id=objid)
            if request.method == "POST":
                form = Challenge_Form(request.POST, instance = ch_obj)
                if form.is_valid():
                    form.save()
                    edit_done = True
                else:
                    form = Challenge_Form(request.POST)
                    edit = True
            else:
                form = Challenge_Form(instance=ch_obj)
        if task == 'viewmore':
            objid=request.GET.get('objid', '')
            ch_obj = Challenge.objects.get(id=objid)



#---------------------------------------- Donation category   -------------------------------------------------------------#

    if key == 'donation_category':
        if task == 'add':
            form = DonationCategoryForm()
            if request.method == "POST":
                form = DonationCategoryForm(request.POST)
                if form.is_valid():
                    name = request.POST.get('name','')
                    f = form.save(commit = False)
                    f.name = name
                    f.save()
                    added = True
                else:
                    form = DonationCategoryForm()
        if task == 'edit':
            edit = True
            objid = request.GET.get('objid','')
            giver_obj = GiverMaster.objects.get(id=objid)
            if request.method == "POST":
                form = DonationCategoryForm(request.POST, instance = giver_obj)
                if form.is_valid():
                    form.save()
                    edit_done = True
                else:
                    form = DonationCategoryForm(request.POST)
                    edit = True
            else:
                form = DonationCategoryForm(instance = giver_obj)
        if task == "delete":
            if id == '':
                id = request.GET.get('id')
            obj = GiverMaster.objects.get(id=id)
            obj.active = 0
            obj.save()
            return HttpResponseRedirect('/configure/donation_category/')
        if task == "active":
            if id == '':
                id = request.GET.get('id')
            obj = GiverMaster.objects.get(id=id)
            obj.active = 2
            obj.save()
            return HttpResponseRedirect('/configure/donation_category/')



#---------------------------------------- Donation Type   -------------------------------------------------------------#

    if key == 'donation_type':
        if task == 'add':
            form = DonationTypeForm()
            if request.method == "POST":
                form = DonationTypeForm(request.POST)
                if form.is_valid():
                    form.save()
                    added = True
                else:
                    form = DonationTypeForm()
        if task == 'edit':
            edit = True
            objid = request.GET.get('objid','')
            giver_obj = GiverMaster.objects.get(id=objid)
            if request.method == "POST":
                form = DonationTypeForm(request.POST, instance = giver_obj)
                if form.is_valid():
                    form.save()
                    edit_done = True
                else:
                    form = DonationTypeForm(request.POST)
                    edit = True
            else:
                form = DonationTypeForm(instance = giver_obj)
        if task == "delete":
            if id == '':
                id = request.GET.get('id')
            obj = GiverMaster.objects.get(id=id)
            obj.active = 0
            obj.save()
            return HttpResponseRedirect('/configure/donation_type/')
        if task == "active":
            if id == '':
                id = request.GET.get('id')
            obj = GiverMaster.objects.get(id=id)
            obj.active = 2
            obj.save()
            return HttpResponseRedirect('/configure/donation_type/')


#---------------------------------------- Topic  -------------------------------------------------------------#

    if key == "topic":
        if task == "delete":
            if id == '':
                id = request.GET.get('id')
            obj = Topic.objects.get(id=id)
            obj.is_public = False
            obj.save()
            return HttpResponseRedirect('/configure/topic/')
        if task == "active":
            if id == '':
                id = request.GET.get('id')
            obj = Topic.objects.get(id=id)
            obj.is_public = True
            obj.save()
            subject = "We have received your discussion topic!"
            message = "Dear "+str(obj.user.first_name)+' '+str(obj.user.last_name)+','+"\n\n"+"You have started/ commented/ posted on the discussion "+str(obj.name)+"."+"Your post has been published. Please, "+"visit http://rightarm.com "+"to view your post and see what others are discussing.We are sure the discussions will MAKE A DIFFERENCE.\n\n\nThank you,\nDevendra Bahadur,\nHead - India Operations\nRightArm"
            send_mail(subject,message,'webmaster@rightarm.com',[obj.user.email],fail_silently=False)
            return HttpResponseRedirect('/configure/topic/')

#----------------------------------------article-------------------------------------------------------------#

    if key == "article":
        if task == "add":
            if request.method == "POST":
                form = ArticleForm(request.POST, request.FILES)
                if form.is_valid():
                    obj=form.save(commit=False)
                    obj.url4SEO=slugify(request.POST.get('title'))
                    obj.status = 'PU'
                    obj.save()
                    added = True
                else:
                    form = ArticleForm(request.POST, request.FILES)
            else:
                form = ArticleForm()
        if task == "edit":
            edit ,check = True , ''
            objid=request.GET.get('objid', '')
            article=Article.objects.get(id=objid)
            if request.method == "POST":
                form = ArticleForm(request.POST, request.FILES,instance =article)
                if form.is_valid():
                    if not has_changed(instance=article,field='title'):
                        form.save()
                        edit_done = True
                    else:
                        check=Article.objects.filter(title__iexact=request.POST.get('title'))
                    if not check:
                        form.save()
                        edit_done = True
                    else:
                        error= "Article name already exist"
                        form = ArticleForm(request.POST, request.FILES,instance = article)
                else:
                    form = ArticleForm(request.POST, request.FILES,instance =article )
            else:
                form = ArticleForm(instance=article)
        if task == "delete":
            if id == '':
                id = request.GET.get('id')
            obj = Article.objects.get(id=id)
            obj.is_active = False
            obj.save()
            return HttpResponseRedirect('/configure/article/')
        if task == "active":
            if id == '':
                id = request.GET.get('id')
            obj = Article.objects.get(id=id)
            obj.is_active = True
            obj.save()
            return HttpResponseRedirect('/configure/article/')


#----------------------------------------Manage Article images, links, attachments-----------------------------------------------------#

    if key == "manage-articles":
        objid = request.GET.get('objid')
        subkey = request.GET.get('subkey')
        print '-----',subkey
        if subkey=='image':
            if task == "add":
                if request.method == "POST":
                    form=ImageForm(request.POST,request.FILES)
                    if form.is_valid():
                        art_id = Article.objects.get(id=objid)
                        obj= form.save(commit=False)
                        obj.content_type = ContentType.objects.get(model__iexact = 'Article')
                        obj.object_id = art_id.id
                        obj.listingOrder = 0
                        obj.status = 'PU'
                        obj.save()
                        added = True
                    else:
                        form = ImageForm(request.POST, request.FILES)
                else:
                    form = ImageForm()
            if task == "edit":
                edit = True
                img_id=request.GET.get('objid')
                image=Image.objects.get(id=img_id)
                if request.method== "POST":
                    form=ImageForm(request.POST,request.FILES,instance=image)
                    if form.is_valid():
                        form.save()
                        edit_done = True
                    else:
                        form=ImageForm(request.POST,request.FILES)
                else:
                    form=ImageForm(instance=image)
            if task == "delete":
                if id == '':
                    id = request.GET.get('id')
                obj = Image.objects.get(id=id)
                obj.is_active = False
                obj.save()
                return HttpResponseRedirect('/configure/manage-articles/?objid='+str(objid))
            if task == "active":
                if id == '':
                    id = request.GET.get('id')
                obj = Image.objects.get(id=id)
                obj.is_active = True
                obj.save()
                return HttpResponseRedirect('/configure/manage-articles/?objid='+str(objid))
        if subkey=='link':
            if task == "add":
                if request.method == "POST":
                    form=LinkForm(request.POST,request.FILES)
                    if form.is_valid():
                        art_id = Article.objects.get(id=objid)
                        obj= form.save(commit=False)
                        obj.content_type = ContentType.objects.get(model__iexact = 'Article')
                        obj.object_id = art_id.id
                        obj.listingOrder = 0
                        obj.status = 'PU'
                        obj.save()
                        added = True
                    else:
                        form = LinkForm(request.POST, request.FILES)
                else:
                    form = LinkForm()
            if task == "edit":
                edit = True
                link_id=request.GET.get('objid')
                link=Link.objects.get(id=link_id)
                if request.method== "POST":
                    form=LinkForm(request.POST,request.FILES,instance=link)
                    if form.is_valid():
                        form.save()
                        edit_done = True
                    else:
                        form=LinkForm(request.POST,request.FILES)
                else:
                    form=LinkForm(instance=link)
            if task == "delete":
                if id == '':
                    id = request.GET.get('id')
                obj = Link.objects.get(id=id)
                obj.is_active = False
                obj.save()
                return HttpResponseRedirect('/configure/manage-articles/?objid='+str(objid))
            if task == "active":
                if id == '':
                    id = request.GET.get('id')
                obj = Link.objects.get(id=id)
                obj.is_active = True
                obj.save()
                return HttpResponseRedirect('/configure/manage-articles/?objid='+str(objid))
        if subkey=='attach':
            if task == "add":
                if request.method == "POST":
                    form=AttachmentForm(request.POST,request.FILES)
                    if form.is_valid():
                        art_id = Article.objects.get(id=objid)
                        obj= form.save(commit=False)
                        obj.content_type = ContentType.objects.get(model__iexact = 'Article')
                        obj.object_id = art_id.id
                        obj.listingOrder = 0
                        obj.status = 'PU'
                        obj.save()
                        added = True
                    else:
                        form = AttachmentForm(request.POST, request.FILES)
                else:
                    form = AttachmentForm()
            if task == "edit":
                edit = True
                att_id=request.GET.get('objid')
                attach=Attachment.objects.get(id=att_id)
                if request.method== "POST":
                    form=AttachmentForm(request.POST,request.FILES,instance=attach)
                    if form.is_valid():
                        form.save()
                        edit_done = True
                    else:
                        form=AttachmentForm(request.POST,request.FILES)
                else:
                    form=AttachmentForm(instance=attach)
            if task == "delete":
                if id == '':
                    id = request.GET.get('id')
                obj = Attachment.objects.get(id=id)
                obj.is_active = False
                obj.save()
                return HttpResponseRedirect('/configure/manage-articles/?objid='+str(objid))
            if task == "active":
                if id == '':
                    id = request.GET.get('id')
                obj = Attachment.objects.get(id=id)
                obj.is_active = True
                obj.save()
                return HttpResponseRedirect('/configure/manage-articles/?objid='+str(objid))


    return render(request, 'manage_configure.html', locals())


#------------------------------Facebook Login Function's----------------------------------------------------------#


from RightArm.settings import FACEBOOK_APP_ID, FACEBOOK_SECRET_KEY, FACEBOOK_REDIRECT_URL
from pyfb import Pyfb

# This view redirects the user to facebook in order to get the code that allows
# pyfb to obtain the access_token in the facebook_login_success view

def facebook_login(request):
    facebook = Pyfb(FACEBOOK_APP_ID)
    return HttpResponseRedirect(facebook.get_auth_code_url(redirect_uri=FACEBOOK_REDIRECT_URL))


#This view must be refered in your FACEBOOK_REDIRECT_URL. For example: http://www.mywebsite.com/facebook_login_success/

def facebook_login_success(request):

    code = request.GET.get('code')
    user = ""
    if code:
        facebook = Pyfb(FACEBOOK_APP_ID)
        facebook.get_access_token(FACEBOOK_SECRET_KEY, code, redirect_uri=FACEBOOK_REDIRECT_URL)
        me = facebook.get_myself()
        fname = me.first_name
        lname = me.last_name
        username = fname+lname
        if not username:
            username = fname + lname
        email = me.email
        try:
            user = User.objects.get(email = email)
        except:
            pass
        if not user:
            password = generate_password(8)
            user = User.objects.create_user(email=email, username=username, password=password, first_name=fname, last_name=lname)

            member_obj, created = Member.objects.get_or_create(user_type='Member', user=user)

            template3 = get_template('social/social_registration_mail.html')
            context = Context({'user': user, 'username':username, 'password': password})
            mail_message = template3.render(context)
            em_obj = EmailMessage('RightArm Credentials', mail_message, 'webmaster@rightarm.com',[user.email],headers = {'Reply-To': 'webmaster@rightarm.com'})
            em_obj.content_subtype = "html"
            em_obj.send()


            con_typ = ContentType.objects.get_for_model(member_obj)
            address = Address.objects.get_or_create(content_type = con_typ, object_id = member_obj.id, email = member_obj.user.email )

        if user:
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return HttpResponseRedirect('/user-profile/')
        else:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')

#Login with the js sdk and backend queries with pyfb

def facebook_javascript_login_sucess(request):
    access_token = request.GET.get("access_token")
    facebook = Pyfb(FACEBOOK_APP_ID)
    facebook.set_access_token(access_token)
    return _render_user(facebook)

def _render_user(request,facebook):
    me = facebook.get_myself()
    return None

def loginpage(request):
    return render_to_response('usermanagement/login.html',{ "FACEBOOK_APP_ID": FACEBOOK_APP_ID }, context_instance=RequestContext(request))


def search_function(request):

    """ Country Search Function """

    results = {}
    search_val = request.GET.get('search_val')
    country_list = Boundary.objects.filter(name__icontains = search_val, active = 2, level = 0).order_by('name')
    return render(request, 'usermanagement/country_search_results.html', locals())


def join_function(request):

    """ Join Function In RightArm """

    country_list = Boundary.objects.filter(active=2,level=0)
    return render(request, 'usermanagement/join.html', locals())


def change_password(request):
    user = request.user
    old_pwd = request.POST.get('old_pwd')
    new_pwd = request.POST.get('new_pwd')
    chg_pwd = request.POST.get('chg_pwd')
    if old_pwd and new_pwd and chg_pwd:
        if request.method == 'POST':
            user = authenticate(username = user.username, password = old_pwd)
            if user:
                user.set_password(chg_pwd)
                user.save()
                return HttpResponseRedirect('/logout/')
            else:
                msg = "Please, enter your old password correctly.!"
    return render(request,'change-password.html', locals())
