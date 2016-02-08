from django import forms

from captcha.fields import CaptchaField

class ContactForm(forms.Form):
    full_name = forms.CharField()
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea, max_length=370)
    captcha = CaptchaField()

class ContactFormSignedIn(forms.Form):
    full_name = forms.CharField(required = False)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea, max_length=370)
