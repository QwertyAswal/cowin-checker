import requests
from datetime import date
import time
import os
import math

end_line = '-' * os.get_terminal_size().columns

today = date.today()
today = today.strftime('%d-%m-%y')

url = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin'


print('\nALLOWED REQUESTS ARE 100 per 300 seconds. Therefore the program will fetch once every 3 seconds\n')

pin_code = input('Enter Pin Code:')
age = int(input('Enter Age:'))

print(end_line)

params = {
    'pincode': pin_code,
    'date': today
}

headers = {
    'User-Agent': 'Chrome/56.0.2924.76',
    "Accept": "*/*",
    "Accept-Language": "en-US"
}




try:
    while True:
        start_time = int(round(time.time() * 1000))
        response = requests.get(url=url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()['centers']
            ctr = 0
            for i in data:
                address = i['address']
                for j in i['sessions']:
                    if j['min_age_limit'] <= age and j['available_capacity'] > 0:
                        string_to_add = 'available ' + str(j['available_capacity'])+' seats of ' + str(
                            j['vaccine'])+' at: ' + address + ', on '+j['date']
                        print(string_to_add)
                        ctr += 1
            if ctr == 0:
                print('NO SEATS AVAILABLE')
            print(end_line)
        else:
            print(response.status_code)
            break
        end_time = int(round(time.time() * 1000))
        sleep_time = max((3 - (end_time-start_time)/1000), 0)
        time.sleep(sleep_time)
except KeyboardInterrupt:
    print('PROCESS ENDED')
