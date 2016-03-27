# load settings file
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

#cache
from django.views.decorators.cache import cache_page
from django.views.decorators.cache import cache_control

import os
from django.core.mail import send_mail
from phoenix.decorators import specific_verified_email_required, cache_on_auth
from .forms import ContactForm, ContactFormSignedIn
from .models import Featurette, FAQ
import json

# Create your views here.
@cache_on_auth(60 * 15)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):

    featurette_list = Featurette.objects.filter(publish=True).order_by('position')
    context = {
        "featurettes": featurette_list,
    }

    return render(request, "home.html", context)

@cache_on_auth(60 * 15)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def faq(request):

    faq_list = FAQ.objects.filter(publish=True).order_by('position')
    context = {
        "faqs": faq_list,
    }

    return render(request, "faq.html", context)

@cache_page(60 * 15)
@specific_verified_email_required(domains=settings.ALLOWED_DOMAINS)
def accommodation(request):

    context = {
    }

    return render(request, "accommodation.html", context)

@cache_page(60 * 15)
@specific_verified_email_required(domains=settings.ALLOWED_DOMAINS)
def shuttle(request):

    context = {
    }

    return render(request, "shuttle.html", context)

@cache_page(60 * 5)
@specific_verified_email_required(domains=settings.ALLOWED_DOMAINS)
def gallery(request):

    context = {
    }

    return render(request, "gallery.html", context)

@cache_on_auth(60 * 15)
def contact(request):
    title = "Contact:"
    if request.user.is_authenticated():
        form = ContactFormSignedIn(request.POST or None)
    else:
        form = ContactForm(request.POST or None)

    context = {
        "contact": 'active',
        "title": title,
        "form": form,
    }
    if form.is_valid():
        form_email = form.cleaned_data.get("email")
        form_message = form.cleaned_data.get("message")
        form_full_name = form.cleaned_data.get("full_name")


        subject = 'Site contact form'
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [settings.DEFAULT_TO_EMAIL]
        contact_message = "%s: %s via %s" %(form_full_name, form_message, form_email)
        some_html_message = """
        <h1>This message was send to you from %s via %s:</h1>
        %s
        """ %(form_full_name, form_email, form_message)
        # send asynchronous
        send_mail(subject,
                    contact_message,
                    from_email,
                    to_email,
                    html_message = some_html_message,
                    fail_silently = False)
        context = {
            "contact": 'active',
            "title": "Thank You!",
        }

    return render(request, "contact.html", context)

from .tasks import prime_number
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def primes(request):

    if request.method == 'GET':
        searchrange = 3
        tasks = 1
        if 'range' in request.GET:
            try:
                searchrange = int(request.GET.get('range'))
            except ValueError:
                searchrange = 3
        if 'tasks' in request.GET:
            try:
                tasks = int(request.GET.get('tasks'))
            except ValueError:
                tasks = 1
        if tasks < 1:
            tasks = 1
        if searchrange < 3:
            searchrange = 3

        if searchrange > 500000:
            searchrange = 500000

        if (searchrange/tasks) > 100000:
            searchrange = 100000
            tasks = 5

        window = int(searchrange / tasks)
        low = 0
        high = window

        for n in range(0, tasks):
            if high > searchrange:
                high = searchrange
            prime_number.delay(low,high)
            low += window
            high += window

    context = {
        "title": "Primes:",
        "range": searchrange,
        "tasks": tasks,
    }
    return render(request, "primes.html", context)
