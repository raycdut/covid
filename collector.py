
from Mongo_Client import Mongo_Client
import requests
import json
from bs4 import BeautifulSoup
import re
import datetime
import os
import time
from country import country
from country import country_trend
from datetime import date

class CovCollector():
    def __init__(self):
        self.db_client = Mongo_Client()
        self.countrycollection = self.db_client.db["CountryInfo"]
        self.country = self.db_client.db['Country']
        self.countryTrend = self.db_client.db['CountryTrend']
        pass

    def request_page(self):
        url = 'https://ncov.dxy.cn/ncovh5/view/pneumonia'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
        r = requests.get(url, headers=headers)
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup

    def requets_trend(self, json_url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
        r = requests.get(json_url, headers=headers)
        return r

    def collect_world(self):
        print("start to collect world info...")

        page = self.request_page()

        countryData_raw = page.find_all('script', attrs={'id': 'getListByCountryTypeService2true'})
        if countryData_raw:
            data = countryData_raw[0].string
            RE = re.compile('\[.*\]')
            data_clear = re.findall(RE, data)
            data_json = json.loads(data_clear[0])
            #self.countrycollection.insert_many(data_json)
            
            for item in data_json:
                if item['countryShortCode'] != 'CHN':
                    id = item['id']
                else:
                    id = 100000000

                if item.get('statisticsData') != None:
                    cn = country(id, item['continents'], item['provinceName'],
                             item['countryFullName'], item['countryShortCode'], item['statisticsData'])
                else:
                    cn = country(id, item['continents'], item['provinceName'],
                             item['countryFullName'], item['countryShortCode'], None)
                
                if cn.statisticData != None:
                    trendRaw = self.requets_trend(cn.statisticData)
                    trend_json = json.loads(trendRaw.text)

                

                    trend = country_trend(
                        cn.id, item['confirmedCount'], 0, item['curedCount'], 0, item['currentConfirmedCount'], 0, datetime.date.today().strftime("%Y-%m-%d"), item['deadCount'], 0)
                    #clean data in mongodb
                    self.country.delete_many({'id': cn.id})
                    self.countryTrend.delete_many({'id': cn.id})

                    self.countryTrend.insert_one(trend.__dict__)

                    for titem in trend_json['data']:
                        trend = country_trend(
                            cn.id, titem['confirmedCount'], titem['confirmedIncr'], titem['curedCount'], titem['curedIncr'], titem['currentConfirmedCount'], titem['currentConfirmedIncr'], titem['dateId'], titem['deadCount'], titem['deadIncr'])
                        
                        self.countryTrend.insert_one(trend.__dict__)
                   
                self.country.insert_one(cn.__dict__)
                
                

if __name__ == "__main__":
    collector = CovCollector()
    collector.collect_world()
    pass
