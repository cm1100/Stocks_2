# https://www.moneycontrol.com/stocks/company_info/stock_news.php?sc_id=UTI10&scat=&pageno=2&next=0&durationType=Y&Year=2021&duration=1&news_type=

import selenium
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.support.select import Select
import datetime
import calendar
from selenium.webdriver.common.keys import Keys

from db_structure.models import Stock,News




month_dict= {month: index for index, month in enumerate(calendar.month_abbr) if month}

print(month_dict)
def get_news(company):
    driver = webdriver.Chrome(ChromeDriverManager().install())

    for year in reversed(range(20,22)):



        urls=[f'https://www.moneycontrol.com/stocks/company_info/stock_news.php?sc_id={company.mc_id}&scat=&pageno={i}&next=0&durationType=Y&Year=20{year}&duration=1&news_type=' for i in range(1,6)]


        for url in urls:
            driver.get(url)


            descript_str="/html/body/div/div/div/div/div/div/div/div/div/div/div"




            descr= driver.find_elements_by_xpath(descript_str)

            for d in descr:
                if len(d.text.split('\n'))==3:
                    compo=d.text.split('\n')
                    headline =compo[0]
                    time1=compo[1].split('|')[0].split()
                    real_time = time1[0].split('.')
                    real_time=[int(r) for r in real_time]
                    if time1[1]=='pm':
                        real_time[0]=(real_time[0]+12)%24


                    date = compo[1].split('|')[1].split()
                    date.reverse()


                    date=datetime.datetime(int(date[0]),month_dict[date[1]],int((date[2])),real_time[0],real_time[1])
                    desc = compo[2]

                    if News.objects.filter(headline=headline).count()==0:
                        obj = News(stock = company,headline=headline,date_time= date,description=desc)
                        obj.save()
                        print("saved")

                    print(headline)
                    print(date)
                    print(desc)


    driver.quit()












