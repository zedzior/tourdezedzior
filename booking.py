import csv
import bs4
import re
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from utils import take_out_number
import datetime


# create url query on booking.com
checkin = datetime.date(2019, 12, 29)
checkout = datetime.date(2020, 1, 3)
people = 4
rooms = 1
city = 'ATH'
center_distance = 1
review = 8


booking_url = f'https://www.booking.com/searchresults.pl.html?tmpl=searchresults&checkin_month={checkin.month}&' \
      f'checkin_monthday={checkin.day}&checkin_year={checkin.year}&checkout_month={checkout.month}&' \
      f'checkout_monthday={checkout.day}&checkout_year={checkout.year}&group_adults={str(people)}&' \
      f'no_rooms={str(rooms)}&sb_price_type=total&ss={city}&nflt=distance={str(center_distance)}000;' \
      f'review_score={review}0;order=price'

print(booking_url)


def get_offers(url):
    with get_chrome_driver() as driver:
        driver.get(url)
        source_code = driver.page_source
        soup = bs4.BeautifulSoup(source_code, 'html.parser')
        container = soup.findAll('div', {'class': re.compile('sr_item_content sr_item_content_slider_wrapper')})
        for offer in container:
            try:
                hotel_name = offer.find('span', {'class': 'sr-hotel__name'}).text.strip()
                link = 'https://www.booking.com' + offer.find('a', {'class': 'hotel_name_link url'}).get('href').strip().split('\n')[0]
                longitiude = float(offer.find('a', {'class': 'bui-link'}).get('data-coords').split(',')[0])
                latitiude = float(offer.find('a', {'class': 'bui-link'}).get('data-coords').split(',')[1])
                distance = get_distance(offer)
                rank = float(offer.find('div', {'class': 'bui-review-score__badge'}).text.replace(',', '.'))
                price = take_out_number(offer.find('div', {'class': 'bui-price-display__value prco-inline-block-maker-helper'}).text)
                record = [hotel_name, rank, price, distance, longitiude, latitiude, link]
                print(record)
                database.append(record)
            except:
                pass


def get_distance(soup):
    m = 0
    x = soup.find('div', {'class': 'sr_card_address_line'}).text.split('\n')
    for i in x:
        if 'centrum' in i:
            z = i.split()
            m = float(z[0].replace(',', '.'))
            meassure = z[1]
            if meassure == 'km':
                m = m * 1000
    return m


def get_chrome_driver():
    driver_path = f'geckodriver.exe'
    opts = Options()
    # opts.headless = True
    driver = webdriver.Firefox(executable_path=driver_path, options=opts)
    return driver


if __name__ == '__main__':
    database = []
    get_offers(booking_url)
    with open('assets/csv/booking.csv', 'w', newline='', encoding='UTF-8') as fp:
        myFile = csv.writer(fp)
        myFile.writerows(database)