import datetime
import csv
from booking import build_booking_url, get_booking_offers
from azair import build_azair_url, get_flights
from utils import open_browser


def get_offers(from_code, to_code, from_date, to_date):
    # build url for azair.eu with all parameters and get list of flights
    flight_list = []
    oneway = {0: 'oneway', 1: 'return'}
    min_days = 5
    max_days = 8
    min_stopover = datetime.time(0, 45)
    max_stopover = datetime.time(23, 30)
    max_there_flight = datetime.time(10, 0)
    max_back_flight = datetime.time(10, 0)
    number_people = 2
    max_change = 1
    currency = 'PLN'

    rooms = 1
    center_distance = 1
    review = 8
    azair_url = build_azair_url(oneway, from_code, to_code, from_date, to_date, min_days, max_days, min_stopover,
                                max_stopover, max_there_flight, max_back_flight, number_people, max_change, currency)
    get_flights(azair_url, flight_list)
    # loop through flight list and add accomodation offers from booking.com
    offer_list = []
    with open_browser() as driver:
        for flight in flight_list:
            temp_list = []
            booking_url = build_booking_url(datetime.datetime.strptime(flight[1], "%Y-%m-%d").date(), datetime.datetime.strptime(flight[12], "%Y-%m-%d").date(), number_people, rooms, flight[6], center_distance, review)
            get_booking_offers(booking_url, temp_list, driver)
            for offer in temp_list:
                offer_list.append([flight[22]+offer[2]]+flight+offer)
    with open('assets/csv/offers.csv', 'w', newline='', encoding='UTF-8') as fp:
        myFile = csv.writer(fp)
        myFile.writerow(['total_price', 'ft_weekday', 'ft_date', 'ft_from_time', 'ft_from_city_name',
                         'ft_from_city_code', 'ft_to_time', 'ft_to_city_name', 'ft_to_city_code',
                         'ft_duration', 'ft_changes', 'ft_price', 'fb_weekday', 'fb_date', 'fb_from_time',
                         'fb_from_city_name', 'fb_from_city_code', 'fb_to_time', 'fb_to_city_name', 'fb_to_city_code',
                         'fb_duration', 'fb_changes', 'fb_price', 'price', 'number_people', 'stay_days',
                         'f_link', 'hotel_name', 'rank', 'price', 'distance', 'longitiude', 'latitiude', 'b_link', 'pic_link'
                         ])
        myFile.writerows(offer_list)


if __name__ == '__main__':
    from_code = 'WRO'
    to_code = 'XXX'
    oneway = {0: 'oneway', 1: 'return'}
    from_date = datetime.date(2020, 4, 20)
    to_date = datetime.date(2020, 4, 30)
    min_days = 5
    max_days = 8
    min_stopover = datetime.time(0, 45)
    max_stopover = datetime.time(23, 30)
    max_there_flight = datetime.time(10, 0)
    max_back_flight = datetime.time(10, 0)
    number_people = 2
    max_change = 1
    currency = 'PLN'

    rooms = 1
    center_distance = 1
    review = 8
    get_offers(from_code, to_code, from_date, to_date)
