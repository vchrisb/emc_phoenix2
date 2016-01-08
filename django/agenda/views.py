from django.shortcuts import render

from .models import Entry
from phoenix.decorators import specific_verified_email_required

# Create your views here.
@specific_verified_email_required(domains=['emc.com','vmware.com'])
def agenda(request):
    entry_list = Entry.objects.filter(publish=True).order_by('start')
    context = {
        "entries": entry_list
    }
    return render(request, "agenda.html", context)
