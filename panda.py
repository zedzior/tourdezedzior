import pandas as pd


def get_results():
    df = pd.read_csv('assets/csv/offers.csv')
    df['price_per_head'] = df.total_price / df.number_people
    df = df.sort_values('total_price')[['price_per_head', 'ft_to_city_name', 'stay_days']]
    cities = df.ft_to_city_name.unique()
    result = []
    for city in cities:
        x = df[df.ft_to_city_name == city].head(1).values.tolist()[0]
        result.append(x)
    return result


if __name__ == '__main__':
    print(get_results())