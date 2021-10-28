import selenium
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.support.select import Select
import datetime
import calendar
from selenium.webdriver.common.keys import Keys
from selen.helpers import save_data
from db_structure.models import Indices,OHCLI

def attack12(indice):
    driver = webdriver.Chrome(ChromeDriverManager().install())


    driver.get("https://www.moneycontrol.com/stocks/histstock.php?indian_indices=1")
    idice =indice

    drop_str = "//select[@id='indian_indices']"
    drops = Select(driver.find_element_by_xpath(drop_str))

    drops.select_by_visible_text(idice)
    drop_str = "//select[@name='frm_yr']"

    drop = Select(driver.find_element_by_xpath(drop_str))
    drop.select_by_visible_text("2011")

    go_str = "//form[@name='frm_dly']//input[@type='image']"

    button = driver.find_element_by_xpath(go_str)

    button.click()
    body_str='/html/body/div/div/div/div/div/table/tbody/tr'

    elements = driver.find_elements_by_xpath(body_str)


    obj = Indices.objects.filter(name=idice)[0]
    print(obj)

    save_data(elements,obj,OHCLI)

    current = driver.current_url
    for i in range(2,6):
        url = current+f"&pno={i}&hdn=daily&fdt=2011-01-01&todt=2021-01-01"
        driver.get(url)
        data = driver.find_elements_by_xpath(body_str)
        save_data(data,obj,OHCLI)






    time.sleep(10)

    return driver