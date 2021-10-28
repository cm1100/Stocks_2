from django.core.management.base import BaseCommand, CommandError


import selenium
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager
from selen.indices_data import attack12,Indices







class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    #def add_arguments(self, parser):
        #parser.add_argument('poll_ids', nargs='+', type=int)


    def handle(self, *args, **options):
        objects = Indices.objects.all()
        for o in objects:
            driver =attack12(o.name)
            break
        driver.quit()