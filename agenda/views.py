from django.shortcuts import render
from django.conf import settings
from .models import Entry
from phoenix.decorators import specific_verified_email_required
from django.views.decorators.cache import cache_page

# Create your views here.
@cache_page(60 * 15)
@specific_verified_email_required(domains=settings.ALLOWED_DOMAINS)
def agenda(request):
    entry_list = Entry.objects.filter(publish=True).order_by('start')
    context = {
        "entries": entry_list
    }
    return render(request, "agenda.html", context)
