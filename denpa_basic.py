'''denpa_basic.py'''
import json
import requests
from requests.exceptions import Timeout

BASE_URL = 'https://www.tele.soumu.go.jp/musen/'
AGENT_CHROME_MAC = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3864.0 Safari/537.36'
AGENT_CHROME_WIN = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'
AGENT_SAFARI_MAC = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) \
    AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15'


class DenpaSearch():
    ''' denpa_search class '''
    def __init__(self) -> None:
        pass

    @classmethod
    def get_total_amateur_stations(cls):
        ''' get total number of Amateur radio stations '''
        headers = {'Accept': '*/*',
                   'Accept-Encoding': 'gzip, deflate',
                   'User-Agent': AGENT_SAFARI_MAC,
                   }
        params = {'ST': 1, 'OF': 2, 'OW': 'AT'}
        try:
            res = requests.get(url=BASE_URL + 'num',
                               headers=headers,
                               params=params,
                               timeout=(3.0, 7.5),
                               # verify=True,
                               )
        except Timeout:
            print('requests timeout error')

        json_dict = json.loads(res.text)

        return json_dict['musen']['count']

    @classmethod
    def get_list_of_amateur_stations(cls, start_count=1):
        ''' get list of Amateur radio stations '''
        headers = {'Accept': '*/*',
                   'Accept-Encoding': 'gzip, deflate',
                   'User-Agent': AGENT_SAFARI_MAC,
                   }
        params = {'ST': 1, 'DA': 0, 'SC': start_count,
                  'DC': 1, 'OF': 2, 'OW': 'AT'}
        try:
            res = requests.get(url=BASE_URL + 'list',
                               headers=headers,
                               params=params,
                               timeout=(3.0, 7.5),
                               # verify=True,
                               )
        except Timeout:
            print('requests timeout error')

        # json_dict = json.loads(res.text)

        return res.text

    @classmethod
    def get_station_information_by_callsign(cls, callsign):
        ''' get list of Amateur radio stations '''
        headers = {'Accept': '*/*',
                   'Accept-Encoding': 'gzip, deflate',
                   'User-Agent': AGENT_SAFARI_MAC,
                   }
        params = {'ST': 1, 'DA': 0, 'SC': 1,
                  'DC': 1, 'OF': 2, 'OW': 'AT', 'MA': callsign}
        try:
            res = requests.get(url=BASE_URL + 'list',
                               headers=headers,
                               params=params,
                               timeout=(3.0, 7.5),
                               # verify=True,
                               )
        except Timeout:
            print('requests timeout error')

        json_dict = json.loads(res.text)

        return json_dict


def main():
    ''' main func for test '''
    # ds = DenpaSearch()
    # result = DenpaSearch.get_total_amateur_stations()
    # print(result)

    # result = DenpaSearch.get_list_of_amateur_stations()
    # print(result)

    result = DenpaSearch.get_station_information_by_callsign('JS2IIU')
    print(result)


if __name__ == '__main__':
    main()
