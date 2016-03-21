from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from .routers import router

import content.views
import mytwitter.views
import agenda.views
import vault.views
import whiteboard.views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    # Examples:
    url(r'^api/', include(router.urls)),
    url(r'^$', content.views.home, name='home'),
    url(r'^contact/$', content.views.contact, name='contact'),
    url(r'^faq/$', content.views.faq, name='faq'),
    url(r'^sme/$', content.views.sme, name='sme'),
    # url(r'^accommodation/$', content.views.accommodation, name='accommodation'),
    # url(r'^shuttle/$', content.views.shuttle, name='shuttle'),
    # url(r'^gallery/$', content.views.gallery, name='gallery'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # Url Entries for allauth
    url(r'^accounts/', include('allauth.urls')),
    #url(r'^rest-auth/', include('rest_auth.urls')),

    url(r'^captcha/', include('captcha.urls')),
    url(r'^primes$', content.views.primes, name='primes'),
    url(r'^tweets$', mytwitter.views.tweet, name='tweet'),
    url(r'^tweets/picture/(?P<uuid>[0-9a-z-]+)$', mytwitter.views.TweetPicView, name='tweetpic'),
    url(r'^tweetgallery$', mytwitter.views.tweetgallery, name='tweetgallery'),
    url(r'^agenda$', agenda.views.agenda, name='agenda'),
    url(r'^documents$', vault.views.documents, name='documents'),
    url(r'^documents/(?P<uuid>[0-9a-z-]+)$', vault.views.document, name='document'),
    url(r'^whiteboards$', whiteboard.views.whiteboard, name='whiteboard'),
    url(r'^whiteboards/image/(?P<uuid>[0-9a-z-]+)$', whiteboard.views.WhiteboardImgView, name='whiteboardimg'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # serving MEDIA in development
