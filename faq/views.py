from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import *
from django.contrib.auth import authenticate, login, logout
from django.template import Context, loader,RequestContext
from django.http import HttpResponseRedirect,HttpResponse,Http404
from django.template.defaultfilters import slugify
from datetime import *
from django.db.models import Q
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMessage, BadHeaderError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import password_reset
from faq.models import *

def faq(request):
    faq_cat = FAQ_Category.objects.filter(is_active=True)
    return render_to_response('faq/faq.html',locals(),context_instance=RequestContext(request))
