from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import datetime
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


def connect_to_db():
    dburl = 'postgres://tbmkkepntuendy:b2308880d750d3f39146471663cec29e85c6cde87ee8a89efc1028a9ffc102b9@ec2-54-246-105-238.eu-west-1.compute.amazonaws.com:5432/d84f7m3fcdukso'
    engine = create_engine(dburl)
    db = scoped_session(sessionmaker(bind=engine))
    return db


def open_browser():
    driver_path = f'geckodriver.exe'
    opts = Options()
    opts.headless = True
    driver = webdriver.Firefox(executable_path=driver_path, options=opts)
    return driver


def convert_date(str):
    return datetime.datetime.strptime(str, "%d/%m/%y").strftime('%Y-%m-%d')


def convert_time(str):
    return str.replace(':', '%3A')


def take_out_time(input: str):
    # get 24h time from string
    return ''.join((filter(lambda x: x in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', ':'], input)))


def take_out_letters(input: str):
    # get rid of any chracters not belonging to letters
    return ''.join((filter(str.isalpha, input)))


def take_out_number(input: str):
    s = ''.join((filter(lambda x: x in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.'], input)))
    return 0 if len(s) == 0 else float(s)


