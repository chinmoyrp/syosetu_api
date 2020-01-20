from dateutil.tz import tzoffset
import datetime
import requests
import json
import os

# This script is written with the assumption that since launch of syosetu, <=2000 novels were published each day till today 

days = [30, 31, 30, 31, 31, 30, 31, 30, 31, 31, 28, 31]
months = [4, 5, 6, 7, 8, 9, 10, 11, 12, 1, 2, 3]
main_counter = 0
aux_counter = 0

#def isleap(year):
    #return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def get_datetext(date):
    return '{}_{}_{}'.format(date.year, date.month, date.day)

def timestamp(y, m, d, hh, mm, ss):
    tzinfo = tzoffset(None, 32400)
    return datetime.datetime(y,m,d,hh,mm,ss, tzinfo=tzinfo).timestamp()

def get_ts_range(y, m, d):
    start = timestamp(y,m,d,0,0,0)
    end = timestamp(y,m,d,23,59,59)
    _range = "-".join([str(start), str(end)])
    return _range
        
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)        


if __name__ == '__main__':
    start_date = datetime.date(2004, 4, 19) #launch of syosetu
    end_date = datetime.date(2020, 1, 20) #today i.e 2020-01-20
    for date in daterange(start_date, end_date):
        ts_range = get_ts_range(date.year, date.month, date.day) # will return something like "1301583600.0-1304175599.0"
        print("Processing for", date, ts_range)
        url = 'https://api.syosetu.com/novelapi/api/?of=t-n&lim=500&st=1&firstup={}&order=old&out=json'.format(ts_range)
        response = requests.get(url)
        result = response.json()
        allcount = result[0]['allcount']
        if allcount == 0:
            print("Skipping", date)
            continue
        
        with open('{}.json'.format(get_datetext(date)), 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=1)
        
        main_counter += allcount
        aux_counter += len(result)-1
        print("**\tallcount={} main_counter={} aux_counter={}".format(allcount, main_counter, aux_counter))
        
        if allcount > 500:
            for st in range(501, allcount, 500):              
                url_new = 'https://api.syosetu.com/novelapi/api/?of=t-n&lim=500&st={}&firstup={}&order=old&out=json'.format(str(st), ts_range)
                response_new = requests.get(url_new)
                result_new = response_new.json()                    
                aux_counter += len(result_new) - 1
                print("\tStill processing for", date, "at step", st, "\tallcount={} main_counter={} aux_counter={}".format(allcount, main_counter, aux_counter)) 
                with open('{}.{}.json'.format(get_datetext(day), st), 'w', encoding='utf-8') as f1:
                    json.dump(result_new, f1, ensure_ascii=False, indent=1)
    
    print('Written {}({}) records'.format(main_counter, aux_counter))
            
