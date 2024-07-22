from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from decouple import config


class Command(BaseCommand):
    help = 'Sets the domain and name for the Site model'

    def handle(self, *args, **options):
        domain = config('SITE_DOMAIN', default='localhost:8000')
        name = config('SITE_NAME', default='My Site')

        site = Site.objects.get_current()
        site.domain = domain
        site.name = name
        site.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully set site domain to {domain} and name to {name}'))
