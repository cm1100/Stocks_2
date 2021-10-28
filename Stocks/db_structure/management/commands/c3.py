from django.core.management.base import BaseCommand, CommandError
from selen.get_details import get_details
from db_structure.models import Stock
import selenium
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager







class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    #def add_arguments(self, parser):
        #parser.add_argument('poll_ids', nargs='+', type=int)


    def handle(self, *args, **options):
        companies = Stock.objects.all()
        driver = webdriver.Chrome(ChromeDriverManager().install())
        for c in companies:
            driver=get_details(c.name,driver)
        driver.quit()
