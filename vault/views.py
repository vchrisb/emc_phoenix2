from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.conf import settings
from django.views.decorators.cache import cache_page
from .models import DocumentGroup, Document
from phoenix.decorators import specific_verified_email_required

# Create your views here.
@cache_page(60 * 15)
@specific_verified_email_required(domains=settings.ALLOWED_DOMAINS)
def documents(request):
    documentgroup_list = DocumentGroup.objects.all().order_by('title')
    context = {
        "entries": documentgroup_list
    }
    return render(request, "documents.html", context)

@specific_verified_email_required(domains=settings.ALLOWED_DOMAINS)
def document(request, uuid):
    document_obj = get_object_or_404(Document, pk=uuid)
    document_obj.downloads += 1
    document_obj.save()
    return HttpResponseRedirect(document_obj.filename.url)
