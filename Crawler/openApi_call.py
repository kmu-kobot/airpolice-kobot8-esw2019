import requests
import kFirebase

class MiseAPI:
    def mise_url(self, sidoName, pageNo):
        ServiceKey = "6FqGEmUPaKfduSBpJEXzaLdX1u6ouTZeCgs%2FlUFVRTa%2BGgsKamPgLw%2Fx9lg4T%2FNfyO73Yy1UkzORcuGRPR%2Bcnw%3D%3D"
        url = "http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnMesureSidoLIst?"
        url = url + "sidoName=" + sidoName + "&searchCondition=HOUR" + "&pageNo=" + str(
            pageNo) + "&numOfRows=10" + "&ServiceKey=" + ServiceKey + "&_returnType=json"

        return url

    def air_info(self, tmp_data):
        coValue = tmp_data['coValue']
        pm10Value = tmp_data['pm10Value']
        pm25Value = tmp_data['pm25Value']

        if coValue == '':
            coValue = '0'
        if pm10Value == '':
            pm10Value = '0'
        if pm25Value == '':
            pm25Value = '0'

        dataList = {
            'coValue': coValue,
            'pm10Value': pm10Value,
            'pm25Value': pm25Value
        }
        return dataList

    def _main(self):
        Firebase = kFirebase.Firebase()

        # Firebase.firebase_db()

        si = Firebase.load('outside/info/si')
        # si = Firebase.load_si()
        # local = Firebase.load_local()
        local = Firebase.load('outside/info/local')
        print(local)
        pageNo = 0

        for i in range(5):
            pageNo += 1

            url = self.mise_url(si, pageNo)
            print(url)
            response = requests.get(url)

            if (response.status_code == 200):
                # print('ok')
                data = response.json()
                for i in range(len(data['list'])):
                    tmp_data = data['list'][i]
                    if tmp_data['cityName'] == local:
                        # self.print_air_info(tmp_data)
                        dataList = self.air_info(tmp_data)
                        Firebase.update(dataList)
            else:
                print("Error code: " + response.status_code)

