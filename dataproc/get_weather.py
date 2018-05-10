# -*- coding: utf-8 -*-

import set_sys_utf8
import requests
from bs4 import BeautifulSoup
import re
import json
from logging import codecs
import demjson
import datetime

def alg_indexof(lst, key, keyof):
    
    length = len(lst)
    
    if length <= 1:
        return 0
    
    fli = lambda l: [0, l / 2] if l % 2 == 0 else [0 , l / 2 + 1]
    fri = lambda l: [l / 2 , l] if l % 2 == 0 else [l / 2 + 1 , l]
    
    left = lst[fli(length)[0] : fli(length)[1]]
    right = lst[fri(length)[0] : fri(length)[1]]
    
    if key < keyof(right[0]):
        return alg_indexof(left, key, keyof)
    else:
        return alg_indexof(right, key, keyof) + fli(length)[1]

class weather_parser():
    
    ##style:2015-04-29
    def __init__(self, city, start, end):
        
        self.__city = city
        self.__start = start
        self.__end = end
        self.__future = []
        self.__future.append('http://tianqi.2345.com/today-%s.htm')
        self.__future.append('http://tianqi.2345.com/tomorrow-%s.htm')
        self.__future.append('http://tianqi.2345.com/third-%s.htm')
        self.__future.append('http://tianqi.2345.com/fourth-%s.htm')
        self.__future.append('http://tianqi.2345.com/fifth-%s.htm')
        self.__future.append('http://tianqi.2345.com/sixth-%s.htm')
        self.__future.append('http://tianqi.2345.com/seventh-%s.htm')
    
    def __month_value(self, month):
        
        url = 'http://tianqi.2345.com/t/wea_history/js/%s/%s_%s.js'%(month, self.__city, month)
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")
        return demjson.decode(re.split('[=;]', soup.string)[1])['tqInfo']
    
    def __subweatherlist(self, wlist):
        
        keyof = lambda x: datetime.datetime.strptime(x['ymd'], '%Y-%m-%d')
        s = datetime.datetime.strptime(self.__start, '%Y-%m-%d')
        e = datetime.datetime.strptime(self.__end, '%Y-%m-%d')     
        retlist = wlist[alg_indexof(wlist, s, keyof)  : alg_indexof(wlist, e, keyof) + 1]
        return retlist
    
    def value(self):
        
        retlist = []
        starts = self.__start.split('-')
        retlist = [ x for x in self.__month_value(starts[0] + starts[1]) if x != {} ]
        if self.__end != self.__start:
            ends = self.__end.split('-')
            retlist = retlist + [ x for x in self.__month_value(ends[0] + ends[1]) if x != {} ]
        print self.__subweatherlist(retlist)
        
class city_paser():
    
    def __init__(self, city):
        self.__city = city
        self.__load_formated_citydata()
        
    def __load_formated_citydata(self):
        
        with open('../res/2345_city_json.txt') as f:
            self.__cityjs = json.loads(f.read())
        
    def __format_citydata(self):
        
        outjs = {}
        
        with open('../res/2345_city.txt')  as f:
            
            lines = f.read().split('\n')
            provqx = [ x for x in lines if 'provqx' in x and 'var' not in x ]
            
            for item in provqx:
                
                item1 = item.split('=')[1]
                item1 = item1[1:-1]
                citys = re.split('[,]', item1)
                citys = [ x[1:-1] for x in citys ]
                
                for citys1 in citys:
                    for citem in citys1.split('|'):
                        citemsplits = re.split('[ -]', citem)
                        outjs[citemsplits[2]] = citemsplits[0]
        
        with codecs.open('../res/2345_city_json.txt', 'w', encoding='utf-8') as f:
            f.write(json.dumps(outjs, indent=4, ensure_ascii=False))
            
    def value(self):
            return self.__cityjs[self.__city.decode('utf-8')]
        
if __name__ == '__main__':
    
    print weather_parser(city_paser('金堂').value(), '2018-04-30', '2018-05-15').value()