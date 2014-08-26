from Projects.models import *
from django.shortcuts import render_to_response, get_object_or_404, render
from django.template import Context, loader, RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.mail import send_mail, EmailMessage, BadHeaderError
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.shortcuts import render
from Projects.forms import *
from django.template.defaultfilters import slugify
from datetime import *
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify
from Social.models import *


def list_all_projects(request):
    ''' list all projects on Right Arm '''
    #import ipdb;ipdb.set_trace()
    project_list = Project.objects.all()
    return render(request, 'projects/list_all_projects.html', locals())



def has_changed(instance, field):
    if not instance.pk:
        return False
    old_value = \
        instance.__class__._default_manager.filter(pk=instance.pk).values(field).get()[field]
    return not getattr(instance, field) == old_value

def add_project(request):
    
    form = Project_Manage_Form()    
    if request.method == 'POST':
        form = Project_Manage_Form(request.POST, request.FILES)
        if form.is_valid():
            proj_cat = Project_Category.objects.get(id=request.POST.get("project_category"))
            member_obj = Member.objects.get(user=request.user)
            from django.forms.fields import DateField
            d = DateField()
            start_date = d.to_python(request.POST.get('start_date', ""))
            end_date = d.to_python(request.POST.get('end_date', ""))
            project_obj = Project.objects.create(project_category=proj_cat,name=request.POST.get("name"),image=request.FILES.get("image"),
                        summary= request.POST.get("summary"), description=request.POST.get("description"),
                        requirement=request.POST.get("requirement"),target_amount=request.POST.get("target_amount"),
                        status=request.POST.get("status"),created_by=member_obj,start_date=start_date,
                        end_date=end_date)
            if request.POST.getlist("beneficiaries", ""):   
                for i in request.POST.getlist("beneficiaries"):
                    project_obj.beneficiaries.add(i)
            if request.POST.getlist("transactions", ""):   
                for i in request.POST.getlist("transactions"):
                    project_obj.transactions.add(i)
            if request.POST.getlist("goals", ""):   
                for i in request.POST.getlist("goals"):
                    project_obj.goals.add(i)
            
            return render(request, 'projects/add_project.html', {'added': True},
                        context_instance=RequestContext(request))
        else:
            form = Project_Manage_Form(request.POST, request.FILES)
    else:
        form = Project_Manage_Form()    
    return render(request, 'projects/add_project.html', locals())        


def edit_project(request, pro_id= ''):
    if pro_id == '':
            pro_id = request.GET.get('pro_id')
            projects = Project.objects.get(id=pro_id)
            form = Project_Manage_Form(instance=projects)    
    if request.method == 'POST':
        form = Project_Manage_Form(request.POST, request.FILES, instance=projects)
        if form.is_valid():
            proj_cat = Project_Category.objects.get(id=request.POST.get("project_category"))
            #import ipdb; ipdb.set_trace()
            projects = Project.objects.filter(name__iexact=request.POST.get('name', "")).exclude(id=int(pro_id))
            if projects:
                msg="Project already exists"
            else:
                #import ipdb; ipdb.set_trace()
                from django.forms.fields import DateField
                d = DateField()
                start_date = d.to_python(request.POST.get('start_date', ""))
                end_date = d.to_python(request.POST.get('end_date', ""))
                project_obj = Project.objects.get(id=request.GET.get('pro_id'))
                cat_obj = Project_Category.objects.get(id=int(request.POST.get('project_category')))
                member_obj = Member.objects.get(user=request.user)
                project_obj.name = request.POST.get('name')
                import ipdb; ipdb.set_trace()
                project_obj.image = request.FILES.get('image')
                project_obj.summary = request.POST.get('summary')
                project_obj.description = request.POST.get('description')
                project_obj.requirement = request.POST.get('requirement')
                project_obj.target_amount = request.POST.get('target_amount')
                project_obj.status = request.POST.get('status')
                project_obj.start_date = start_date
                project_obj.end_date = end_date
                
                project_obj.project_category = cat_obj
                project_obj.save()
            if request.POST.getlist("beneficiaries", ""):
                project_obj.beneficiaries.clear()
                for i in request.POST.getlist("beneficiaries"):
                    project_obj.beneficiaries.add(i)
            if request.POST.getlist("transactions", ""):   
                project_obj.transactions.clear()
                for i in request.POST.getlist("transactions"):
                    project_obj.transactions.add(i)
            if request.POST.getlist("goals", ""):   
                project_obj.goals.clear()
                for i in request.POST.getlist("goals"):
                    project_obj.goals.add(i)
            
            return render(request, 'projects/add_project.html', {'edit_done': True},
                    context_instance=RequestContext(request))
                
    return render(request, 'projects/add_project.html', locals())


def delete_project(request, pro_id=''):
    #import ipdb;ipdb.set_trace()
    if pro_id =='':
        pro_id = request.GET.get('pro_id')
    proj = Project.objects.get(id=pro_id)
    proj.is_active = False
    proj.save()
    return HttpResponseRedirect('/projects/project-list/')



def project_category(request):
    if request.method == 'POST':
            form = Project_Category_Form(request.POST, request.FILES)
            name = request.POST.get('name')
            if form.is_valid():
                try:
                    check = Project_Category.objects.filter(name__iexact=name,
                            is_active = 2)
                except:
                    check = ''
                if not check:
                    form.save()
                    return render(request, 'projects/add_project_category.html', {'added': True,
                            'next': next},
                            context_instance=RequestContext(request))
                else:
                    error = 'Project Category already exists'
                    form = Project_Category_Form(request.POST, request.FILES)
            else:
                form = Project_Category_Form(request.POST, request.FILES)
    else:
        form = Project_Category_Form()
    return render(request, 'projects/add_project_category.html', locals())



'''
def project_category(request, task = None):
    task = request.GET.get('task')
    next = '/project/category/list/'
    if task == 'add':
        if request.method == 'POST':
            form = Project_Category_Form(request.POST, request.FILES)
            name = request.POST.get('name')
            if form.is_valid():
                try:
                    check = Project_Category.objects.filter(name__iexact=name,
                            is_active = 2)
                except:
                    check = ''
                if not check:
                    form.save()
                    return render(request, 'add_project_category.html', {'added': True,
                            'next': next},
                            context_instance=RequestContext(request))
                else:
                    error = 'Project Category already exists'
                    form = Project_Category_Form(request.POST, request.FILES)
            else:
                form = Project_Category_Form(request.POST, request.FILES)
        else:
            form = Project_Category_Form()
        return render(request, 'add_project_category.html', locals())


    if task == "edit":
        #import ipdb; ipdb.set_trace()
        if pro_cat_id == '':
            pro_cat_id_id = request.POST.get('pro_cat_id_id', '')
            project_category = Project_Category.objects.get(id = pro_cat_id_id)
        if request.method == 'POST':
            form = Project_Category_Form(request.POST, request.FILES, instance = project_category)
            name = request.POST.get('name')
            if form.is_valid():
                if not has_changed(instance=project_category, field='name'):
                    form.save()
                    return render(request, 'add_project_category.html',
                        {'edit_done': True, 'next': next},
                        context_instance=RequestContext(request))
                else:
                    try:
                        check = Project_Category.objects.filter(name__iexact=name,
                            is_active=2)
                    except:
                        check = ''
                    if not check:
                        form.save()
                        return render(request, 'add_project_category.html',
                        {'edit_done': True, 'next': next},
                        context_instance=RequestContext(request))
                    else:
                        error = 'Project Category already exists'
                        form = Project_Category_Form(request.POST, request.FILES)
                        edit = True
            else:
                form = Project_Category_Form(request.POST, request.FILES)
                edit = True
        else:
            form = Project_Category_Form(instance=project_category)
            edit = True
        return render(request, 'add_project_category.html', locals())
'''

def project_details(request):
    pass
    return render(request, 'projects/project_details.html', locals())
