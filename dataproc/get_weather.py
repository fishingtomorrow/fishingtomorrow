# -*- coding: utf-8 -*-

import set_sys_utf8
import requests
from bs4 import BeautifulSoup
import re
import json
from logging import codecs
import demjson
import datetime
import time
import re

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
        retinfo = demjson.decode(re.split('[=;]', soup.string)[1])['tqInfo']
        retinfo = [ x for x in retinfo if x != {} ]
        ##fix future weather info.
        y, m, d = retinfo[-1]['ymd'].split('-')
        if datetime.date.today() >= datetime.date(int(y), int(m), int(d)):
            for i in range(int(self.__end.split('-')[2]) - int(str(datetime.date.today()).split('-')[2]) + 1):
                
                weainfo = {'ymd':str(datetime.date.today() + datetime.timedelta(days=i))}
                
                allinfo = BeautifulSoup(requests.get(self.__future[i]%(self.__city)).content, "html.parser")
                timeinfo = allinfo.find('div', 'time-main')
                timeinfo2 = allinfo.find('div', 'filter')
                
                night = timeinfo.find('dl', 'night')
                temperature = night.find('span', 'temperature')
                weainfo['yWendu'] = re.search('\d+', temperature.get_text()).group()
                phrase0 = night.find('span', 'phrase').get_text()
                
                day = timeinfo.find('dl', 'day')
                temperature = day.find('span', 'temperature')
                weainfo['bWendu'] = re.search('\d+', temperature.get_text()).group()
                phrase1 = day.find('span', 'phrase').get_text()
                
                weainfo['tianqi'] = '%s~%s'%(phrase0, phrase1) if phrase0 != phrase1 else phrase0
                
                timeinfo2 = [x.get_text() for x in timeinfo2.find_all('li')]
                try: weainfo['fengxiang'] = [x for x in timeinfo2 if '风向：' in x][0].split('：')[1]
                except: weainfo['fengxiang'] = 'N/A'
                try: weainfo['fengli'] = [x for x in timeinfo2 if '风力：' in x][0].split('：')[1]
                except: weainfo['fengli'] = 'N/A'
                
                retinfo.append(weainfo)
    
        return retinfo
    
    def __subweatherlist(self, wlist):
        
        keyof = lambda x: datetime.datetime.strptime(x['ymd'], '%Y-%m-%d')
        s = datetime.datetime.strptime(self.__start, '%Y-%m-%d')
        e = datetime.datetime.strptime(self.__end, '%Y-%m-%d')     
        retlist = wlist[alg_indexof(wlist, s, keyof)  : alg_indexof(wlist, e, keyof) + 1]
        return retlist
    
    def value(self):
        
        retlist = []
        starts = self.__start.split('-')
        ends = self.__end.split('-')
        retlist = [ x for x in self.__month_value(starts[0] + starts[1]) if x != {} ]
        if starts[1] != ends[1]:
            ends = self.__end.split('-')
            retlist = retlist + [ x for x in self.__month_value(ends[0] + ends[1]) if x != {} ]
        return self.__subweatherlist(retlist)
        
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
    weather_parser(city_paser('游仙').value(), '2018-05-20', '2018-05-31').value()
    #print json.dumps(weather_parser(city_paser('游仙').value(), '2018-05-20', '2018-05-30').value(), ensure_ascii=False, indent=4)