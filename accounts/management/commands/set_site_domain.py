from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from django.conf import settings


class Command(BaseCommand):
    help = 'Sets the domain and name for the Site model'

    def handle(self, *args, **options):
        domain = settings.SITE_DOMAIN
        name = settings.SITE_NAME

        site = Site.objects.get_current()
        site.domain = domain
        site.name = name
        site.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully set site domain to {domain} and name to {name}'))
