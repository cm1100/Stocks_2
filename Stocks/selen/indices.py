import selenium
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.support.select import Select
import datetime
import calendar
from selenium.webdriver.common.keys import Keys
from db_structure.models import Indices


def add_indices():
    driver = webdriver.Chrome(ChromeDriverManager().install())


    url = 'https://www.moneycontrol.com/stocks/histstock.php'

    index_str = "//a[@id='wutabs2']"

    driver.get(url)
    element = driver.find_element_by_xpath(index_str)
    element.click()
    drop_str = "//select[@id='indian_indices']"
    e = driver.find_element_by_xpath(drop_str)
    elements =e.text.split('\n')



    for e in elements[1:]:
        m = e.split()
        m = " ".join(m)
        if Indices.objects.filter(name = m).count()==0:
            obj = Indices(name=m)
            obj.save()
    time.sleep(10)
    driver.quit()

