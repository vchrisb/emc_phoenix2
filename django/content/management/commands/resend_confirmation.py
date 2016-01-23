from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from allauth.account.models import EmailAddress
from allauth.account.adapter import get_adapter
from django.contrib import messages

class Command(BaseCommand):

    help = 'Starts the twitter watcher'

    def add_arguments(self, parser):
        parser.add_argument('--email',dest='email_address_list', nargs='+', type=str, required=False)
        parser.add_argument('--all_not_verified', dest='all_not_verified', action='store_true', required=False, default=False)

    def handle(self, *args, **options):
        if not options['email_address_list'] and not options['all_not_verified']:
            raise ValueError("Specify either --email <email> or --all_not_verified")

        request = None
        if options['all_not_verified']:
            email_address_list = EmailAddress.objects.filter(verified=False)
            for email_address in email_address_list:
                print (email_address.email)
                email_address.send_confirmation(request)

        if options['email_address_list']:
            for email in options['email_address_list']:
                try:
                    email_address = EmailAddress.objects.get(email=email)
                    print (email_address.email)
                    email_address.send_confirmation(request)
                except EmailAddress.DoesNotExist:
                    raise CommandError('email address "%s" does not exist' % email)
