from django.core.management.base import BaseCommand, CommandError
from selen.indices import add_indices

import selenium
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager







class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    #def add_arguments(self, parser):
        #parser.add_argument('poll_ids', nargs='+', type=int)


    def handle(self, *args, **options):
        add_indices()