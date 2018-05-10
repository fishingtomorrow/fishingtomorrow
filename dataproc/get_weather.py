import requests
from bs4 import BeautifulSoup

def get_city_weather(city, date):
    
    url = 'http://tianqi.2345.com/t/wea_history/js/201804/%s_%s.js'%(city, date)
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    return soup.string

if __name__ == '__main__':
    
    print get_city_weather('56294', '201804')