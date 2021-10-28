import selenium

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.support.select import Select

driver = webdriver.Chrome(ChromeDriverManager().install())
from selenium.webdriver.common.keys import Keys


def get_data(company):

    url ='https://www.moneycontrol.com/stocks/histstock.php'

    driver.get(url)
    enter_str ='//*[(@id = "mycomp")]'
    enter=driver.find_element_by_xpath(enter_str)
    enter.send_keys(company)
    enter.send_keys(Keys.ENTER)
    time.sleep(2)

    elements_str = '//*[(@id = "suggest")]'
    elements = driver.find_elements_by_xpath(elements_str)

    for e in elements:


        e.click()
        break

    drop_str = '//*[contains(concat( " ", @class, " " ), concat( " ", "PT4", " " )) and (((count(preceding-sibling::*) + 1) = 2) and parent::*)]//select~//select+//select'
    drop_str = "//select[@name='frm_yr']"

    drop = Select(driver.find_element_by_xpath(drop_str))
    drop.select_by_visible_text("2011")

    go_str = "//form[@name='frm_dly']//input[@type='image']"

    button= driver.find_element_by_xpath(go_str)

    button.click()

    time.sleep(10)
    return driver


get_data("reliance industries")

driver.quit()