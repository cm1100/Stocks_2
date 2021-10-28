from django.core.management.base import BaseCommand, CommandError
from selen.add_stock import add_s
class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    #def add_arguments(self, parser):
        #parser.add_argument('poll_ids', nargs='+', type=int)


    def handle(self, *args, **options):
        add_s()