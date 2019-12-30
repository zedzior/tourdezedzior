import pandas as pd


def get_results():
    df = pd.read_csv('assets/csv/offers.csv')
    df = df.sort_values('total_price')[['total_price', 'ft_to_city_name', 'stay_days', 'number_people']].head(30)
    df['price per head'] = df.total_price / df.number_people
    return df.values.tolist()

if __name__ == '__main__':
    print(get_results())