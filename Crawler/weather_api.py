# https://kimdoky.github.io/tip/2018/04/02/tip-reverse_geocoding.html
import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import trans
import time as t
import kFirebase

class WeatherAPI:

    def get_address(self, country, lat, lng, api_key):
        url = "https://maps.googleapis.com/maps/api/geocode/json?language=%s&latlng=%f,%f&key=%s" % (country, lat, lng, api_key)
        r = requests.get(url).json()

        new_full_adr = r['results'][1]['formatted_address']
        old_full_adr = r['results'][0]['formatted_address']
        local = r['results'][0]['address_components'][2]['long_name']
        si = r['results'][0]['address_components'][3]['long_name']
        si = si[:2]

        return new_full_adr, local, si

    def trans_coordinate(self,latitude, longitude):
        # print(latitude, longitude)
        Trans = trans.Trans()
        x, y = Trans.mapToGrid(latitude, longitude)

        return x, y


    def _main(self, second=1.0):
        # global end
        # if end:
        #     return

        Firebase = kFirebase.Firebase()
        # Firebase.firebase_db()

        latitude = Firebase.load('outside/area/latitude')
        longitude = Firebase.load('outside/area/longitude')


        x, y = self.trans_coordinate(latitude,longitude)
        address, local, si = self.get_address('ko', latitude, longitude, "AIzaSyAbqCogJph6aII9fjowm-it_0ADt41q6bo")

        Firebase.update({'now_location': address})
        # Firebase.update_address(address)
        Firebase.update({'local': local})
        # Firebase.update_local(local)
        Firebase.update({'si': si})
        # Firebase.update_si(si)
        # print(address)

        url = "http://newsky2.kma.go.kr/service/SecndSrtpdFrcstInfoService2/ForecastGrib?"
        ServiceKey = "ServiceKey=6FqGEmUPaKfduSBpJEXzaLdX1u6ouTZeCgs%2FlUFVRTa%2BGgsKamPgLw%2Fx9lg4T%2FNfyO73Yy1UkzORcuGRPR%2Bcnw%3D%3D"
        today = t.localtime()

        year = str(today.tm_year)
        day = ''
        mon = ''
        time = str(today.tm_hour)
        if today.tm_mon < 10:
            mon = "0" + str(today.tm_mon)
        else:
            mon = str(today.tm_mon)

        if today.tm_mday < 10:
            day = "0" + str(today.tm_mday)
        else:
            day = str(today.tm_mday)


        base_date = "&base_date=" + str(year) + str(mon) + str(day)
        base_time = "&base_time=" + str(int(time) - 1) + "45"
        nx = "&nx=" + str(x)
        ny = "&ny=" + str(y)
        url = url + ServiceKey + base_date + base_time + nx + ny + "&pageNo=1" + "&numOfRows=10&_type=json"

        print(url)

        response = requests.get(url)

        if response.status_code == 200:
            # print("ok")
            data = response.json()
            # print(data)
            tmp_data = data['response']['body']['items']['item']
            # print(tmp_data)

            temp = 0.0
            humid = 0.0

            if tmp_data[3]["category"] == "T1H":
                print('온도: ', tmp_data[3]['obsrValue'], '℃')
                temp = float(tmp_data[3]['obsrValue'])

            if tmp_data[1]["category"] == "REH":
                print('습도: ', tmp_data[1]['obsrValue'], '%')
                humid = float(tmp_data[1]['obsrValue'])

            Firebase.update({'temp': temp,'humid': humid})
            # Firebase.update_temp(temp, humid)
            pass

        else:
            print("Error code: " + response.status_code)
