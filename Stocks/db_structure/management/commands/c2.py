from django.core.management.base import BaseCommand, CommandError
from selen.details import get_data
from db_structure.models import Stock

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    #def add_arguments(self, parser):
        #parser.add_argument('poll_ids', nargs='+', type=int)


    def handle(self, *args, **options):

        stocks = Stock.objects.all()
        for s in stocks:
            driver=get_data(s.name)


        driver.quit()


