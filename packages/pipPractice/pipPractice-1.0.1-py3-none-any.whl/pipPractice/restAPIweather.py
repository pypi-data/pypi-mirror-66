from time import sleep

import pandas as pd
import requests
import urllib3


def call_weather_api(start_date, end_date):
    api_key = '5CpJ21rSTnOqjDSRlI9V2WHkJJuJ3WudZO9H/9va4ygSmn3bE/Yo1Rk7omHjjaE9'
    url_format = 'https://data.kma.go.kr/apiData/getData?type=json&dataCd=ASOS&dateCd=HR&startDt={' \
                 'date}&startHh=00&endDt={date}&endHh=23&stnIds={snt_id}&schListCnt=100&pageIndex=1&apiKey={api_key} '

    headers = {'content-type': 'application/json;charset=utf-8'}
    urllib3.disable_warnings()  # ssl 에러방지

    for date in pd.date_range(start_date, end_date).strftime("%Y%m%d"):
        print("%s Weather" % date)
        url = url_format.format(api_key=api_key, date=date, snt_id="108")
        response = requests.get(url, headers=headers, verify=False)

        # 200 (정상)의 경우에만 파일 생성
        print(response.status_code)
        if response.status_code == 200:
            result = pd.DataFrame(response.json()[-1]["info"])
            print(result.head())
            result = result.fillna(0)
            print("Nan값 처리 후")
            print(result.head())
            result.to_csv("./raw_data/weather_%s.csv" % date, index=False, encoding="utf-8")
        # API 부하 관리를 위해 0.5초 정도 쉬어 줍시다 (찡긋)
        sleep(0.5)



