import pandas as pd


class Offer:
    def __init__(self, total_price, ft_weekday, ft_date, ft_from_time, ft_from_city_name, ft_from_city_code, ft_to_time,
                 ft_to_city_name, ft_to_city_code, ft_duration, ft_changes, ft_price, fb_weekday, fb_date, fb_from_time,
                 fb_from_city_name, fb_from_city_code, fb_to_time, fb_to_city_name, fb_to_city_code, fb_duration,
                 fb_changes, fb_price, flight_price, number_people, stay_days, f_link, hotel_name, rank, book_price,
                 distance, longitiude, latitiude, b_link, pic_link):
        self.total_price = total_price
        self.ft_weekday = ft_weekday
        self.ft_date = ft_date
        self.ft_from_time = ft_from_time
        self.ft_from_city_name = ft_from_city_name
        self.ft_from_city_code = ft_from_city_code
        self.ft_to_time = ft_to_time
        self.ft_to_city_name = ft_to_city_name
        self.ft_to_city_code = ft_to_city_code
        self.ft_duration = ft_duration
        self.ft_changes = int(ft_changes)
        self.ft_price = ft_price
        self.fb_weekday = fb_weekday
        self.fb_date = fb_date
        self.fb_from_time = fb_from_time
        self.fb_from_city_name = fb_from_city_name
        self.fb_from_city_code = fb_from_city_code
        self.fb_to_time = fb_to_time
        self.fb_to_city_name = fb_to_city_name
        self.fb_to_city_code = fb_to_city_code
        self.fb_duration = fb_duration
        self.fb_changes = int(fb_changes)
        self.fb_price = fb_price
        self.flight_price = flight_price
        self.number_people = number_people
        self.stay_days = int(stay_days)
        self.f_link = f_link
        self.hotel_name = hotel_name
        self.rank = rank
        self.book_price = book_price
        self.distance = int(distance)
        self.longitiude = longitiude
        self.latitiude = latitiude
        self.b_link = b_link
        self.pic_link = pic_link
        self.price_per_head = int(self.total_price / self.number_people)
        self.price_per_head_per_day = int(self.total_price / self.number_people / self.stay_days)


def get_results():
    df = pd.read_csv('assets/csv/offers.csv')
    df = df.sort_values('total_price')
    cities = df.ft_to_city_name.unique()
    result = []
    for city in cities:
        x = df[df.ft_to_city_name == city].head(1).values.tolist()[0]
        offer = Offer(*x)
        result.append(offer)
    return result


def get_results_for_city(city):
    df = pd.read_csv('assets/csv/offers.csv')
    df = df[df.ft_to_city_name == city]
    x = df.values.tolist()
    result = []
    for row in x:
        offer = Offer(*row)
        result.append(offer)
    return result


if __name__ == '__main__':
    k = get_results_for_city('Krakow')
    print(k[0].price_per_head)