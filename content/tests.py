from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress


# Create your tests here.
class SimpleViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@emc.com', 'johnpassword')
        # EmailAddress.objects.create(user=self.user,
        #                                 email='lennon@emc.com',
        #                                 primary=True,
        #                                 verified=True)

    def test_home_view_(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_faq_view_(self):
        response = self.client.get(reverse('faq'))
        self.assertEqual(response.status_code, 200)

    def test_agenda_view_(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('agenda'))
        self.assertEqual(response.status_code, 200)
        #print(response.content)
