import selenium
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.support.select import Select
from db_structure.models import LookupStock,Stock,OHCL
from pprint import pprint
import datetime




def save_data(data,stock):
    dict1 = {}
    i=0
    for d in data:
        if i == 1:
            for m in d.text.split()[:-3]:
                dict1[m] = []

        elif i > 2:
            keys = list(dict1)
            dim = d.text.split()

            [dict1[keys[k]].append(dim[k]) for k in range(6)]
            date = dim[0].split('-')

            date.reverse()

            date = datetime.date(int(date[0]), int(date[1]), int(date[2]))

            if OHCL.objects.filter(stock=stock,date=date).count() == 0:

                obj = OHCL(stock=stock, date=date, open_p=float(dim[1]), high_p=float(dim[2]), low_p=float(dim[3]),
                           close_p=float(dim[4]), volume=float(dim[5]))
                obj.save()
                print("saved")


        i += 1


def get_details(company,driver):
    stock=Stock.objects.filter(name=company)[0]
    print(stock)
    look = LookupStock.objects.filter(stock = stock)[0]
    driver.get(look.url)

    drop_str = "//select[@name='frm_yr']"

    drop = Select(driver.find_element_by_xpath(drop_str))
    drop.select_by_visible_text("2011")

    go_str = "//form[@name='frm_dly']//input[@type='image']"

    button = driver.find_element_by_xpath(go_str)

    button.click()

    time.sleep(5)

    bse_str = "/html[1]/body[1]/div[6]/div[2]/div[1]/div[4]/div[2]/div[1]/span[2]/strong[1]"
    bse = driver.find_element_by_xpath(bse_str)
    bse=bse.text.split()[1]

    nse_str = '//span[(((count(preceding-sibling::*) + 1) = 3) and parent::*)]//strong'
    nse = driver.find_element_by_xpath(nse_str)
    nse = nse.text.split()[1]

    isin_str = '//span[(((count(preceding-sibling::*) + 1) = 4) and parent::*)]//strong'
    isin = driver.find_element_by_xpath(isin_str)
    isin = isin.text.split()[1]

    id_n = driver.current_url.split('&')[1].split('=')[1]
    print(id_n)

    if Stock.objects.filter(name=company,bse__isnull=False,mc_id__isnull=False).count()==0:
        print("came in")
        Stock.objects.filter(name=company).update(bse=bse,nse=nse,isin_num=isin,mc_id=id_n)


    # https://www.moneycontrol.com/stocks/hist_stock_result.php?sc_id=RI&pno=2&hdn=daily&fdt=20111-01-01&todt=2021-01-01
    body_str='/html/body/div/div/div/div/div/table/tbody/tr'

    data=driver.find_elements_by_xpath(body_str)
    save_data(data,stock=stock)
    u = driver.current_url.split('&')
    for i in range(2,5):
        print(i)
        u1=u
        u1+=[f'pno={i}','hdn=daily','fdt=2011-01-01&todt=2021-01-01']
        u1 = '&'.join(u1)
        driver.get(u1)
        data=driver.find_elements_by_xpath(body_str)
        save_data(data,stock=stock)



    time.sleep(10)











    return driver






