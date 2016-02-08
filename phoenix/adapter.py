from allauth.account.adapter import DefaultAccountAdapter
from django import forms
from django.conf import settings

class AccountAdapter(DefaultAccountAdapter):
    def clean_email(self, email):
        print(email)
        email_base, provider = email.split("@")
        domain, extension = provider.split('.')
        if not provider in settings.ALLOWED_DOMAINS:
            error_text = "Please use a valid %s email address" %(', '.join(settings.ALLOWED_DOMAINS))
            raise forms.ValidationError(error_text)
        return email
