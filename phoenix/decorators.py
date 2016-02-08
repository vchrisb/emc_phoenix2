from django.contrib.auth.decorators import login_required
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.shortcuts import render
from django.db.models import Q

from allauth.account.models import EmailAddress
from allauth.account.utils import send_email_confirmation

from functools import reduce

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
            if not EmailAddress.objects.filter(Q(user=request.user), reduce(lambda x, y: (x | y), [Q(email__iendswith=('@' + domain)) for domain in domains])).exists():
                return render(request, 'account/email_required_domain.html', context)
            elif not EmailAddress.objects.filter(Q(user=request.user, verified=True), reduce(lambda x, y: (x | y), [Q(email__iendswith=('@' + domain)) for domain in domains])).exists():
                #send_email_confirmation(request, request.user)
                return render(request, 'account/verified_email_required_domain.html', context)
            return view_func(request, *args, **kwargs)
        return _wrapped_view

    if function:
        return decorator(function)
    return decorator
