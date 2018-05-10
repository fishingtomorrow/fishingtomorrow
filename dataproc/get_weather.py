import requests
from bs4 import BeautifulSoup


class weather_parser():
    
    def __init__(self, city, year_month):
        self.__city = city
        self.__year_month = year_month
        
    def value(self):
        
        url = 'http://tianqi.2345.com/t/wea_history/js/201804/%s_%s.js'%(self.__city, self.__year_month)
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")
        return soup.string


class city_paser():
    
    def __init__(self, city):
        self.__city = city
    
    def value(self):
            return '56294'
        
if __name__ == '__main__':
    
    print weather_parser(city_paser('').value(), '201804').value()