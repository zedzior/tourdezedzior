import requests
import csv
import bs4
from utils import take_out_time, convert_time, take_out_number

from_code = 'WRO'
to_code = 'XXX'
oneway = {0: 'oneway', 1: 'return'}
from_date = '2019-12-02'
to_date = '2019-12-31'
min_days = 5
max_days = 8
min_stopover = '0:45'
max_stopover = '23:30'
max_there_flight = '10:00'
max_back_flight = '10:00'
number_people = 2
max_change = 1
currency = 'PLN'


def get_flights():
    # get source code of search results on azair.eu
    source_code = requests.get(url)
    soup = bs4.BeautifulSoup(source_code.text, 'lxml')
    # loop through all found flights
    flights = soup.findAll('div', {'class': 'result'})
    for flight in flights:
        # get data of flight there
        flight_there = flight.div.findAll('p', recursive=False)[0]
        ft_weekday = flight_there.find('span', {'class': 'date'}).text.split(' ')[0]
        ft_date = flight_there.find('span', {'class': 'date'}).text.split(' ')[1]
        ft_from_time = flight_there.find('span', {'class': 'from'}).text.split(' ')[0]
        ft_from_city_name = flight_there.find('span', {'class': 'from'}).text.split(' ')[1]
        ft_from_city_code = flight_there.find('span', {'class': 'from'}).text.split(' ')[2][:3]
        ft_to_time = flight_there.find('span', {'class': 'to'}).text.split(' ')[0]
        ft_to_city_name = flight_there.find('span', {'class': 'to'}).text.split(' ')[1]
        ft_to_city_code = flight_there.find('span', {'class': 'to'}).text.split(' ')[2][:3]
        ft_duration = take_out_time(flight_there.find('span', {'class': 'durcha'}).text.split('/')[0])
        ft_changes = flight_there.find('span', {'class': 'durcha'}).text.split('/')[1].strip()
        ft_price = take_out_number(flight_there.find('span', {'class': 'subPrice'}).text)

        # get data of flight back
        flight_back = flight.div.findAll('p', recursive=False)[1]
        fb_weekday = flight_back.find('span', {'class': 'date'}).text.split(' ')[0]
        fb_date = flight_back.find('span', {'class': 'date'}).text.split(' ')[1]
        fb_from_time = flight_back.find('span', {'class': 'from'}).text.split(' ')[0]
        fb_from_city_name = flight_back.find('span', {'class': 'from'}).text.split(' ')[1]
        fb_from_city_code = flight_back.find('span', {'class': 'from'}).text.split(' ')[2][:3]
        fb_to_time = flight_back.find('span', {'class': 'to'}).text.split(' ')[0]
        fb_to_city_name = flight_back.find('span', {'class': 'to'}).text.split(' ')[1]
        fb_to_city_code = flight_back.find('span', {'class': 'to'}).text.split(' ')[2][:3]
        fb_duration = take_out_time(flight_back.find('span', {'class': 'durcha'}).text.split('/')[0])
        fb_changes = flight_back.find('span', {'class': 'durcha'}).text.split('/')[1].strip()
        fb_price = take_out_number(flight_back.find('span', {'class': 'subPrice'}).text)

        price = take_out_number(flight.find('span', {'class': 'tp'}).text)
        stay_days = take_out_number(flight.find('span', {'class': 'lengthOfStay'}).text)
        link = 'http://www.azair.eu/' + flight.find('div', {'class': 'bookmark'}).a.get('href')

        result = [ft_weekday, ft_date, ft_from_time, ft_from_city_name, ft_from_city_code, ft_to_time, ft_to_city_name,
                  ft_to_city_code, ft_duration, ft_changes, ft_price, fb_weekday, fb_date, fb_from_time,
                  fb_from_city_name, fb_from_city_code, fb_to_time, fb_to_city_name, fb_to_city_code, fb_duration,
                  fb_changes, fb_price, price, stay_days, link]
        print(result)
        database.append(result)


# create url query on azair.eu
url = f'http://www.azair.eu/azfin.php?searchtype=flexi&tp=0&isOneway={oneway[1]}&srcAirport=%5B{from_code}%5D&' \
      f'dstAirport=%5B{to_code}%5D&depdate={from_date}&&arrdate={to_date}&minDaysStay={str(min_days)}&maxDaysStay={str(max_days)}&' \
      f'dep0=true&dep1=true&dep2=true&dep3=true&dep4=true&dep5=true&dep6=true&arr0=true&arr1=true&arr2=true&arr3=true&arr4=true&arr5=true&arr6=true&' \
      f'samedep=true&samearr=true&minHourStay={convert_time(min_stopover)}&maxHourStay={convert_time(max_stopover)}&maxHourOutbound={convert_time(max_there_flight)}&' \
      f'maxHourInbound={convert_time(max_back_flight)}&autoprice=true&adults={str(number_people)}&maxChng={str(max_change)}&' \
      f'currency={currency}&indexSubmit=Search'
print(url)

if __name__ == '__main__':
    database = []
    get_flights()
    with open('test.csv', 'w', newline='', encoding='UTF-8') as fp:
        myFile = csv.writer(fp)
        myFile.writerows(database)
