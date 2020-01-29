import csv
import bs4
import re
from utils import take_out_number, open_browser
import datetime
import traceback
from itertools import compress


# create url query on booking.com
from_date = datetime.date(2020, 2, 1)
to_date = datetime.date(2020, 2, 20)
number_people = 2
rooms = 1
city = 'Ateny'
center_distance = 1
review = 8
# apartment, hostel, hotel, guest house
room_types = [False, False, False, False]


def build_booking_url(from_date, to_date, number_people, rooms, city, center_distance, review, room_types):
    # apartment, hostel, hotel, guest house
    room_type_filters = ['ht_id%3D201%3B', 'ht_id%3D203%3B', 'ht_id%3D204%3B', 'ht_id%3D216%3B']
    room_type_filter = ''.join(list(compress(room_type_filters, room_types)))
    booking_url = f'https://www.booking.com/searchresults.pl.html?tmpl=searchresults&checkin_month={from_date.month}&' \
                  f'checkin_monthday={from_date.day}&checkin_year={from_date.year}&checkout_month={to_date.month}&' \
                  f'checkout_monthday={to_date.day}&checkout_year={to_date.year}&group_adults={str(number_people)}&' \
                  f'no_rooms={str(rooms)}&sb_price_type=total&ss={city}&nflt={room_type_filter}distance={str(center_distance)}000;' \
                  f'review_score={review}0;order=price'
    print(booking_url)
    return booking_url


def get_booking_offers(url: str, database: list, driver):
    driver.get(url)
    source_code = driver.page_source
    soup = bs4.BeautifulSoup(source_code, 'html.parser')
    container = soup.findAll('div', {'class': re.compile('sr_item_content sr_item_content_slider_wrapper')})
    for offer in container:
        try:
            if not offer.find('div', {'class': re.compile('sold_out_property')}):
                hotel_name = offer.find('span', {'class': 'sr-hotel__name'}).text.strip()
                link = 'https://www.booking.com' + offer.find('a', {'class': 'hotel_name_link url'}).get('href').strip().split('\n')[0]
                longitiude = float(offer.find('a', {'class': 'bui-link'}).get('data-coords').split(',')[0])
                latitiude = float(offer.find('a', {'class': 'bui-link'}).get('data-coords').split(',')[1])
                distance = get_distance(offer)
                rank = float(offer.find('div', {'class': 'bui-review-score__badge'}).text.replace(',', '.'))
                price = take_out_number(offer.find('div', {'class': 'bui-price-display__value prco-inline-block-maker-helper'}).text)
                pic_link = offer.parent.find('img').get('src')
                record = [hotel_name, rank, price, distance, longitiude, latitiude, link, pic_link]
                print(record)
                database.append(record)
        except:
            traceback.print_exc()


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


if __name__ == '__main__':
    booking_database = []
    booking_url = build_booking_url(from_date, to_date, number_people, rooms, city, center_distance, review, room_types)
    # with open_browser() as driver:
    #     get_booking_offers(booking_url, booking_database, driver)
    # with open('assets/csv/booking.csv', 'w', newline='', encoding='UTF-8') as fp:
    #     myFile = csv.writer(fp)
    #     myFile.writerows(booking_database)