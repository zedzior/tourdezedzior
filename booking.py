import datetime
import csv
import requests
import bs4
import re
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


checkin = datetime.datetime(2019, 12, 10)
checkout = datetime.date(2019, 12, 15)
people = 4
rooms = 1
city = 'Krakow'
center_distance = 1
review = 8


url = f'https://www.booking.com/searchresults.pl.html?tmpl=searchresults&checkin_month={checkin.month}&' \
      f'checkin_monthday={checkin.day}&checkin_year={checkin.year}&checkout_month={checkout.month}&' \
      f'checkout_monthday={checkout.day}&checkout_year={checkout.year}&group_adults={str(people)}&' \
      f'no_rooms={str(rooms)}&sb_price_type=total&ss={city}&nflt=distance={str(center_distance)}000;' \
      f'review_score={review}0;order=price'

print(url)


def get_offers():
    driver = get_chrome_driver()
    driver.get(url)
    source_code = driver.page_source
    driver.close()
    soup = bs4.BeautifulSoup(source_code, 'html.parser')
    container = soup.findAll('div', {'class': re.compile('sr_item_content sr_item_content_slider_wrapper')})
    print(len(container))


def get_chrome_driver():
    driver_path = f'geckodriver.exe'
    opts = Options()
    # opts.headless = True
    driver = webdriver.Firefox(executable_path=driver_path, options=opts)
    return driver


if __name__ == '__main__':
    database = []
    get_offers()
    with open('booking.csv', 'w', newline='', encoding='UTF-8') as fp:
        myFile = csv.writer(fp)
        myFile.writerows(database)