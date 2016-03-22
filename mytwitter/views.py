from django.shortcuts import get_object_or_404, render
from django.db import transaction
from django.http import HttpResponseRedirect
from django.conf import settings
# Create your views here.
from .forms import TweetForm
from .models import Tweet, TweetPic
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from phoenix.decorators import specific_verified_email_required

from django.views.decorators.cache import cache_page

from .tasks import process_image
from PIL import Image

@cache_page(60 * 2)
@transaction.atomic
@specific_verified_email_required(domains=settings.ALLOWED_DOMAINS)
def tweet(request):
    title = "Tweet:"
    tweet_list = Tweet.objects.all().order_by('-created_at')
    paginator = Paginator(tweet_list, 10) # Show 10 tweets per page
    page = request.GET.get('page')

    try:
        tweets = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        tweets = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        tweets = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            for picture in form.cleaned_data['picture']:
                image = process_image(Image.open(picture))
                image_name = "tmp.jpg" # will be renamed by "upload_to" function
                newpic = TweetPic()
                newpic.tweet = instance
                newpic.picture.save(image_name, image, save=False)
                newpic.save()

            return HttpResponseRedirect(reverse('tweet'))
    else:
        form = TweetForm()

    context = {
        "tweet": 'active',
        "title": title,
        "form": form,
        "tweets": tweets,
    }
    return render(request, "tweet.html", context)

@cache_page(60 * 15)
@specific_verified_email_required(domains=settings.ALLOWED_DOMAINS)
def tweetgallery(request):
    tweetpic_list = TweetPic.objects.all().prefetch_related('tweet').order_by('-tweet__created_at')
    paginator = Paginator(tweetpic_list, 25) # Show 25 tweets per page
    page = request.GET.get('page')

    try:
        tweetpics = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        tweetpics = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        tweetpics = paginator.page(paginator.num_pages)

    context = {
        "tweetpics": tweetpics,
    }
    return render(request, "tweetgallery.html", context)

@specific_verified_email_required(domains=settings.ALLOWED_DOMAINS)
def TweetPicView(request, uuid):
    TweetPicObj = get_object_or_404(TweetPic, pk=uuid)
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
        url = TweetPicObj.picture.url
    elif size == 'large':
        url = TweetPicObj.pic_large.url
    elif size == 'medium':
        url = TweetPicObj.pic_medium.url
    elif size == 'small':
        url = TweetPicObj.pic_small.url
    elif size == 'thumb':
        url = TweetPicObj.pic_thumb.url
    else:
        url = TweetPicObj.pic_large.url

    return HttpResponseRedirect(url)
