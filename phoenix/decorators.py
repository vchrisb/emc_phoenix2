from django.contrib.auth.decorators import login_required
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.shortcuts import render
from django.db.models import Q

from allauth.account.models import EmailAddress
from allauth.account.utils import send_email_confirmation

from functools import reduce
from django.core.cache import cache

def specific_verified_email_required(function=None,
                            login_url=None,
                            redirect_field_name=REDIRECT_FIELD_NAME,
                            domains=None):
    """
    Even when email verification is not mandatory during signup, there
    may be circumstances during which you really want to prevent
    unverified users to proceed. This decorator ensures the user is
    authenticated and has a verified email address. If the former is
    not the case then the behavior is identical to that of the
    standard `login_required` decorator. If the latter does not hold,
    email verification mails are automatically resend and the user is
    presented with a page informing them they needs to verify their email
    address.
    """
    def decorator(view_func):
        @login_required(redirect_field_name=redirect_field_name, login_url=login_url)
        def _wrapped_view(request, *args, **kwargs):
            context ={
                'domains': domains
            }
            #look in cache if email is verified
            email_verified_key = str(request.user.id) + "_email_verified"
            email_verified = cache.get(email_verified_key)

            if not request.user.is_superuser and not email_verified:
                if not EmailAddress.objects.filter(Q(user=request.user), reduce(lambda x, y: (x | y), [Q(email__iendswith=('@' + domain)) for domain in domains])).exists():
                    return render(request, 'account/email_required_domain.html', context)
                elif not EmailAddress.objects.filter(Q(user=request.user, verified=True), reduce(lambda x, y: (x | y), [Q(email__iendswith=('@' + domain)) for domain in domains])).exists():
                    #send_email_confirmation(request, request.user)
                    return render(request, 'account/verified_email_required_domain.html', context)

            #put key in cache that email is verified
            if not email_verified:
                cache.set(email_verified_key, 'True', 3600)
            return view_func(request, *args, **kwargs)
        return _wrapped_view

    if function:
        return decorator(function)
    return decorator


from django.views.decorators.cache import cache_page
from functools import wraps
from django.utils.decorators import available_attrs

def cache_on_auth(timeout):
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            return cache_page(timeout, key_prefix="_auth_%s_" % request.user.is_authenticated())(view_func)(request, *args, **kwargs)
        return _wrapped_view
    return decorator
