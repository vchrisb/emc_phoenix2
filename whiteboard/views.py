from django.shortcuts import get_object_or_404,render
from django.http import HttpResponseRedirect
from django.conf import settings
from django.views.decorators.cache import cache_page

# Create your views here.
from .forms import WhiteboardForm
from .models import Whiteboard
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from phoenix.decorators import specific_verified_email_required

# Create your views here.
@specific_verified_email_required(domains=settings.ALLOWED_DOMAINS)
def whiteboard(request):
    whiteboard_list = Whiteboard.objects.all().order_by('-created_at')
    paginator = Paginator(whiteboard_list, 25) # Show 10 tweets per page
    page = request.GET.get('page')

    try:
        whiteboards = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        whiteboards = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        whiteboards = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        form = WhiteboardForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return HttpResponseRedirect(reverse('whiteboard'))
    else:
        form = WhiteboardForm()

    context = {
        "form": form,
        "whiteboards": whiteboards,
    }
    return render(request, "whiteboard.html", context)

@specific_verified_email_required(domains=settings.ALLOWED_DOMAINS)
def WhiteboardImgView(request, uuid):
    ImgObj = get_object_or_404(Whiteboard, pk=uuid)
    size = ''
    if request.method == 'GET':
        if 'size' in request.GET:
            try:
                size = str(request.GET.get('size'))
            except ValueError:
                pass

    if not size in ['full', 'large', 'medium', 'small', 'thumb']:
        size = ''

    if size == 'full':
        url = ImgObj.image.url
    elif size == 'large':
        url = ImgObj.img_large.url
    elif size == 'medium':
        url = ImgObj.img_medium.url
    elif size == 'small':
        url = ImgObj.img_small.url
    elif size == 'thumb':
        url = ImgObj.img_thumb.url
    else:
        url = ImgObj.img_large.url

    return HttpResponseRedirect(url)
