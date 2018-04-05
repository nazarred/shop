from django.core.management.base import BaseCommand, CommandError
from django.contrib.sessions.models import Session
from django.utils import timezone


class Command(BaseCommand):
    help = 'Видаляє сесії в яких закінчився термін дії'

    def handle(self, *args, **options):
        session = Session.objects.filter(expire_date__lt=timezone.now())
        if not session:
            raise CommandError('Немає сесій які потребують видалення')
        session.delete()
