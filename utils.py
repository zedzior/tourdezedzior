def convert_time(str):
    return str.replace(':', '%3A')


def take_out_time(input: str):
    # get 24h time from string
    return ''.join((filter(lambda x: x in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', ':'], input)))


def take_out_letters(input: str):
    # get rid of any chracters not belonging to letters
    return ''.join((filter(str.isalpha, input)))


def take_out_number(input: str):
    return float(''.join((filter(lambda x: x in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.'], input))))

