from bs4 import BeautifulSoup
import re
import os
import json
import pandas as pd
from datetime import datetime
import fnmatch
import time
import requests
from selenium import webdriver
# from seleniumwire import webdriver  # selenium-wire를 사용합니다.
from selenium.webdriver.chrome.options import Options
import warnings
warnings.filterwarnings('ignore')
from IPython.display import clear_output
import copy


class Hogangnono:
    def __doc__(self) :
        print("""
    이 클래스는 호갱노노 웹사이트를 크롤링합니다.

    구조체설명:
              - 기본적으로 apt_id와 areaNo, name를 기반으로 작동합니다.
              - 아무것도 입력하지 않으면 서울 전체 지역에 대해서 작동합니다.
              - id, 동, 구, 시를 입력할 수 있도록 만들어야 합니다.
              - 현재는 id에 대해서 모든 것이 정립된 상황이라 생각하시면 되겠습니다.
              - 이후의 내용에 대해서는 반복문을 통해서 할 수 있습니다.
    
    주요 기능:
    - DB) 지역의 아파트 목록을 가져올 수 있습니다.
    - 메인1) 아파트의 자세한 정보(INFO)를 가져올 수 있습니다.
    - 메인2) 아파트의 실거래가(REAL_TRADE)를 가져올 수 있습니다.
              
    - 서브1) 수집된 데이터를 CSV 파일로 저장합니다.
    - 서브2) 수집된 데이터를 병합하고 통합된 파일을 생성합니다.
    
    - 참고) 날짜 범위를 설정하여 실거래가 데이터를 선형 보간법을 사용해 보정합니다.
              (보간법 -> ffill(미래데이터추정) -> bfill(과거데이터가져오기))

    주요 속성:
    - root_folder: 데이터를 저장할 루트 폴더 경로
    - real_trade_folder: 실거래가 데이터를 저장할 폴더 경로
    
    - apts_path: 아파트 정보를 저장할 CSV 파일 경로
    - info_path: 아파트 상세 정보를 저장할 CSV 파일 경로
    - real_trade_path: 실거래가 데이터를 저장할 CSV 파일 경로
    - interpolated_real_trade_path: 보정된 실거래가 데이터를 저장할 CSV 파일 경로
    - merge_apts_info_path: 아파트 정보와 상세 정보를 병합한 CSV 파일 경로
    - merge_apts_info_real_trade_path: 모든 데이터를 병합한 CSV 파일 경로
    - merge_apts_info_interpolated_real_trade_path: 보간법 적용 실거래가 데이터를 병합한 CSV 파일 경로
              
    - date_list: 데이터 수집 날짜 목록

    주요 메서드:
    - ✅__init__: 클래스 초기화 및 폴더 생성
    - config: 수집할 지역 설정
    - get_all_datas: 모든 데이터 로드
    - get_filenames: 파일 목록 가져오기
    - fetch_real_trade_data_one_time: 특정면적 최초 10개 실거래가 데이터 가져오기
    - fetch_real_trade_data_single_areaNo: 특정 면적의 실거래가 데이터 수집
    - fetch_real_trade_data_single_id: 특정 아파트의 실거래가 데이터 수집
    - get_dates: 날짜 목록 생성
    - open_json_file: JSON 파일 열기
    - formatting_date: 날짜 형식 변환
    - get_apts_info: 아파트 정보 가져오기
    - fill_apts_info: 아파트 정보 채우기
    - fill_trade_data: 실거래가 데이터 보정
    - get_trade_data: 실거래가 데이터 가져오기
    - main: 가격정보를 모아주는 메서드 
    - merge_real_trades: 실거래가 데이터 병합
    - extract_data_from_raw_json: 원본 JSON 데이터에서 정보 추출
    - fetch_apt_info: 아파트 상세 정보 수집
    - merge: 모든 데이터 병합  

              TODO1) 캐싱 | INFO의 경우에는 캐싱해도 된다.
              TODO2) 매물 | 네이버지도에서 가져오면 된다.
              TODO3) GUI  | 만들어서 팔자.
              TODO4) HEADER  | SELENIUM 이용해서 HEADER 갱신이 필요
              TODO5) 갱신 | 아파트가 새로생겨나기도 하고 없어지기도 한다.
              
              """)

    def __init__(self):
        # 폴더경로
        self.root_folder = '호갱노노'
        self.data_folder = os.path.join(self.root_folder, 'data')
        self.info_folder = os.path.join(self.data_folder, 'info')
        self.real_trade_folder = os.path.join(self.data_folder, 'real_trade')

        # 폴더가 없으면 생성
        os.makedirs(self.root_folder, exist_ok=True)
        os.makedirs(self.data_folder, exist_ok=True)
        os.makedirs(self.info_folder, exist_ok=True)
        os.makedirs(self.real_trade_folder, exist_ok=True)

        # 단일파일경로
        self.apts_path = os.path.join(self.data_folder, '호갱노노.csv')
        self.info_path = os.path.join(self.root_folder, '호갱노노_정보.csv') 
        self.real_trade_path = os.path.join(self.root_folder, '호갱노노_실거래가.csv')        
        self.interpolated_real_trade_path = os.path.join(self.root_folder, '호갱노노_실거래가_선형보간.csv')        
        self.interpolated_filled_real_trade_path = os.path.join(self.root_folder, '호갱노노_실거래가_선형보간_채우기.csv')        

        # 합친파일경로        
        self.merge_apts_info_path = os.path.join(self.root_folder, '호갱노노_통합.csv') 
        self.merge_apts_info_real_trade_path = os.path.join(self.root_folder, '호갱노노_완전체.csv') 
        self.merge_apts_info_interpolated_real_trade_path = os.path.join(self.root_folder, '호갱노노_완전체_선형보간.csv') 
        self.merge_apts_info_interpolated_filled_real_trade_path = os.path.join(self.root_folder, '호갱노노_완전체_선형보간_채우기.csv') 
        


        # 필요한 변수들.
        self.date_list = self.get_dates()
        self.get_all_datas()
    
    # def save_all_data(self) ;
    """다 저장하도록 해야함."""

    def config(self, districts='all') :
        if type(districts) == str :
            districts = list(districts)
        elif type(districts) != list :
            print('district를 올바르게 설정하세요')
            return

        
        
    def load_csv(self, file_path):
        if os.path.exists(file_path):
            return pd.read_csv(file_path, encoding='cp949', )
        else:
            return pd.DataFrame()  # Return an empty DataFrame if the file does not exist 
    def save_csv(self, data, file_path, encoding='cp949', errors='replace', index=False) :
        data.to_csv(file_path, encoding=encoding, errors=errors, index=index)

    def get_all_datas(self):
        self.apts = self.load_csv(self.apts_path)
        self.info = self.load_csv(self.info_path)
        self.real_trade = self.load_csv(self.real_trade_path)
        self.interpolated_real_trade = self.load_csv(self.interpolated_real_trade_path)
        self.interpolated_filled_real_trade = self.load_csv(self.interpolated_filled_real_trade_path)
        self.merge_apts_info = self.load_csv(self.merge_apts_info_path)
        self.merge_apts_info_real_trade = self.load_csv(self.merge_apts_info_real_trade_path)
        self.merge_apts_info_interpolated_real_trade = self.load_csv(self.merge_apts_info_interpolated_real_trade_path)
        self.merge_apts_info_interpolated_filled_real_trade = self.load_csv(self.merge_apts_info_interpolated_filled_real_trade_path)



    def get_filenames(self, type='info') :
        if type == 'info' :
            return [name for name in os.listdir(self.root_folder) if '.json' in name]
        if type == 'trade' :
            return [name for name in os.listdir(self.real_trade_folder) if '.json' in name]

    def fetch_real_trade_data_one_time(self, apt_id, areaNo, start):
        cookies = {
            'bat': 'B-VEzEDDnAr6CcP6k_SI0s2QqZ78PHXDpJkw',
            '_gcl_au': '1.1.1543066674.1719753966',
            '_fbp': 'fb.1.1719753965794.820917726471047565',
            '_gid': 'GA1.2.18808630.1719753966',
            '_wp_uid': '1-821aee09be2ee8d0af9029b7e4a8355c-s1711704073.904983|windows_10|chrome-2ui902',
            'connect.sid': 's%3AH3Hg--8KIBQ_kT2unBOECRwPC4bCysN_2Q.ocLMX3yyzVCAzhppmZYPiRkGyZyJYlwNYgUEdBkcEKM',
            '_ga': 'GA1.1.1496764594.1719753966',
            'cto_bundle': 'ypfqWF84WlQwJTJCZTBFYUZ4RlglMkJQdXJhMCUyQjRhTjFERmR0bmo5Rm4yaWgyOFY5JTJCUERHcFpDZ2hEWXdpJTJGcENROFVNJTJGNzRtMiUyRnU2TWxEcElVRThKRTBXS3kzYko4eWowbFB0cEdTJTJCd2lOQ09WRWc3Nkpma2JiNE5LZEMzOGFZZnFXdDJzNXJlNnA5Um1IcURsSzY5V04lMkZBVHRFYXJtOURxZ2hXUEMwdlk2WUVFVURqNGtFbVZYejFtS3pVb3ZLZEtVU1ZKZmZ4UEpBM3hIJTJGNVdTZSUyQjFJdVRtU25SdyUzRCUzRA',
            '_ga_P8RWS72S79': 'GS1.1.1719883930.11.1.1719884250.0.0.0',
            'client.cid': 'JngTZb5cTiCB4vmgIUgcl4OTzYZPexzKtahKl9MjHss',
        }

        headers = {
            'accept': 'application/json',
            'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'priority': 'u=1, i',
            'referer': 'https://hogangnono.com/apt/1VO56/0/2',
            'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'x-hogangnono-api-version': '1.9.18',
            'x-hogangnono-app-name': 'hogangnono',
            'x-hogangnono-at': 'B-VEzEDDnAr6CcP6k_SI0s2QqZ78PHXDpJkw',
            'x-hogangnono-ct': '1719884523578',
            'x-hogangnono-event-duration': '890477',
            'x-hogangnono-event-log': '620f9c27023d936e8feeec11e3efcadd867fed90',
            'x-hogangnono-platform': 'desktop',
            'x-hogangnono-release-version': '1.9.18.14',
        }

        params = {
            'tradeType': '0',
            'areaNo': areaNo,
            'start': start,
        }

        response = requests.get(f'https://hogangnono.com/api/v2/apts/{apt_id}/trade-real', params=params, cookies=cookies, headers=headers)
        return response.json()
    
    def fetch_real_trade_data_single_areaNo(self, apt_id, areaNo=None):
        real_trades = []
        isEnd = False
        start = 0

        while not isEnd:     
            data = self.fetch_real_trade_data_one_time(apt_id, areaNo, start)
            
            if data['data']:
                isEnd = data['data']['isEnd']
                real_trades += data['data']['data']
                print(start, isEnd)
            else:
                return
            
            if not isEnd:
                start += len(data['data']['data'])
                continue
            elif isEnd:
                return real_trades
            
    def fetch_real_trade_data_single_id(self, apt_id, apt_name, save=True):
        """핵심기능1) 실거래가를 조회한다."""
        wrongAreaNo = False
        areaNo = None
        while not wrongAreaNo:
            real_trades = self.fetch_real_trade_data_single_areaNo(apt_id, areaNo)
            if real_trades:
                if areaNo == None :
                    areaNo = 0
                if save :
                    saving_apt_name = apt_name.replace('/', '&')
                    with open(os.path.join(self.real_trade_folder, f'{apt_id}_{saving_apt_name}_{areaNo}.json'), 'w', encoding='utf-8') as json_file:
                        json.dump(real_trades, json_file, ensure_ascii=False, indent=4)
                        print('완료')
                if areaNo :
                    areaNo += 1
                else : areaNo = 1

            

            else:
                wrongAreaNo = True
                if save and areaNo == None :
                    saving_apt_name = apt_name.replace('/', '&')
                    with open(os.path.join(self.real_trade_folder, f'{apt_id}_{saving_apt_name}_{"없음"}.json'), 'w', encoding='utf-8') as json_file:
                        json.dump(real_trades, json_file, ensure_ascii=False, indent=4)
                        print('완료')

    def get_dates(self, start_date="2005-12", end_date="2024-07"):
        date_range = pd.date_range(start=start_date, end=end_date, freq='MS')
        date_list = date_range.strftime('%Y-%m').tolist()
        return date_list

    def open_json_file(self, file_path, encoding='utf-8'):
        with open(file_path, 'r', encoding=encoding) as file:
            data = json.load(file)
        return data

    def formatting_date(self, date_str, format_from='%Y-%m-%dT%H:%M:%S.%fZ', format_to='%Y-%m'):
        formatted_date = datetime.strptime(date_str, format_from).strftime(format_to)
        return formatted_date

    def get_apts_info(self):
        df = pd.read_csv(self.apts_path, encoding='cp949', index_col=0, )
        self.apts_info = df
        return df
    
    def fill_apts_info(self, df):
        def splitting(data) :
            splitted = data.split('_')
            return splitted[0], splitted[1]
        ids = list(df.index)
        results = list(map(splitting, list(ids)))

        ids = []
        areaNo = []
        area = []
        for result in results:
            ids.append( result[0])
            areaNo.append( result[1])

        cols = self.apts_info.columns
        for col in cols:
            datas = []
            for id in ids:
                datas.append(self.apts_info[self.apts_info['id'] == id][col].values[0])
            try:
                df.insert(1, col, datas)
            except:
                continue
        return df
    



    
    def get_trade_data(self, filenames):
        """조회하여 저장해둔 실거래 json 데이터로부터 필요한 데이터들을 추출하여 저장합니다.
        filenames에는 전체 path가 아니라 진짜 파일명칭만 넣으면 됩니다."""
        total = len(filenames)
        now = 0
        df = pd.DataFrame(columns=['areaType'] + self.date_list)
        
        for filename in filenames:
            now += 1
            
            print(f'{now}/{total}')
            # print(filename)
            if now  % 10 == 0 : clear_output()
            name = filename.replace('.json', '')
            data = self.open_json_file(os.path.join(self.real_trade_folder, filename))
            
            if not data :
                continue
            
            max_prices = {}
            for trade in data:
                result = {
                    "floor": trade['floor'],
                    "date": self.formatting_date(trade['date']),
                    "areaType": trade['areaType'],
                    'dong': trade['dong'],
                    'price': trade['price'],
                }
                current_price = max_prices.get(result['date'], 0)
                if result['price'] > current_price:
                    max_prices[result['date']] = result['price']
            for date, price in max_prices.items():
                df.at[name, date] = price
                df.at[name, 'areaType' ]= result['areaType']
                
            # 예시용으로 5개 정도는 진행상황을 표시합니다.
            if now < 5:
                print(data)
                display(df.head())            
            
            # areaType 칼럼을 조정합니다.
            df['areaType'] = df['areaType'].apply(lambda x : x.split('/')[0])
            def extract_number(item):
                return re.split('[^0-9]', item)[0]
            df['areaType'] = df['areaType'].apply(extract_number)
        
        return df
    
        
    def main(self):
        filenames = fnmatch.filter(os.listdir(self.real_trade_folder), '*.json')
        df = self.get_trade_data(filenames)
        df = df.reset_index(drop=True)
        cols = list(df.columns)
        cols[0] = 'id_areaNo'
        df.columns = cols
        # 'id_areaNo' 열의 값을 '_' 기준으로 분리하여 'id'와 'areaNo' 열을 만듭니다.
        df[['id', 'name', 'areaNo']] = df['id_areaNo'].str.split('_', expand=True)
        # 'id' 열을 1번째에, 'areaNo' 열을 2번째에 삽입합니다.
        df = df[['id', 'name','areaNo'] + [col for col in df.columns if col not in ['id', 'areaNo', 'id_areaNo']]]
        # 기본 파일 저장        
        df.to_csv(self.real_trade_path, encoding='cp949', index=False)
        # 채워 넣은 파일 저장 (선형보간법)
        try :
            df[self.date_list] = df[self.date_list].apply(pd.to_numeric, errors='coerce')
            df[self.date_list] = df[self.date_list].interpolate(axis=1, limit_area='inside')
            df.to_csv(self.interpolated_real_trade_path, encoding='cp949', index=False)
        except Exception as e :
            print("at interpolating",e)
        
        try :
            df[self.date_list] = df[self.date_list].ffill(axis=1).bfill(axis=1)    
            df.to_csv(self.interpolated_filled_real_trade_path, encoding='cp949', index=False)
        except Exception as e :
            print("at filling", e)
        return df



    def extract_data_from_raw_json(self, id):
        subwaynames = [
            "1호선", "2호선", "3호선", "4호선", "5호선",
            "6호선", "7호선", "8호선", "9호선", "신분당선",
            "공항철도", "경의중앙선", "우이신설선", "경춘선", "수인분당선",
            "경강선"
        ]

        data = self.open_json_file(os.path.join(self.info_folder, f"{id}.json"))

        if not data:
            print(f"{id} : error (Nonetype)")
            return None

        altState = data.get('altState')
        if altState is None:
            print(f"error at {id}")
            return None

        aptStore = altState.get('AptStore')
        if aptStore is None:
            print(f"error at {id}")
            return None

        detail = aptStore.get('detail')
        if detail is None:
            print(f"error at {id}")
            return None

        baseinfo = detail.get('baseinfo', {})
        convenience = detail.get('convenience', {})
        aptDiffOfPeriod = detail.get('aptDiffOfPeriod', {})
        schoolInfo = detail.get('schoolInfo', {})
        preschool = detail.get('preschool', {})
        commutes = detail.get('commutes', [])

        result = {
            'id': detail.get('id'),
            'name': detail.get('name'),
            'trade_count': detail.get('trade_count'),
            'total_household': detail.get('total_household'),
            'manage_cost': baseinfo.get('manage_cost', {}).get('year'),
            'building_count': baseinfo.get('building_count'),
            'floor_max': baseinfo.get('floor_max'),
            'floor_min': baseinfo.get('floor_min'),
            'slope': baseinfo.get('slope'),
            'approval_date': baseinfo.get('approval_date') or baseinfo.get('permission_date'),
            'parking_rate': baseinfo.get('parking_rate'),
            'earthquake': baseinfo.get('earthquake'),
            'nearby_school_point': detail.get('nearby_school_point'),
            'nearby_subway_station_count': detail.get('nearby_subway_station_count'),
            'total_rental_business_household': detail.get('total_rental_business_household'),
            'areas': [],
            'subways': [],
            'ktxs': [],
            'park_name': None,
            'park_dist': None,
            'mart_name': None,
            'mart_dist': None,
            'hospital_name': None,
            'hospital_dist': None,
            'elementarySchool_name': None,
            'elementarySchool_dist': None,
            'elementarySchool_duration': None,
            'preschool_name': None,
            'preschool_dist': None,
            'commutes': {},
            'diff_3m': aptDiffOfPeriod.get('3m'),
            'diff_6m': aptDiffOfPeriod.get('6m'),
            'diff_1y': aptDiffOfPeriod.get('1y'),
            'diff_3y': aptDiffOfPeriod.get('3y'),
            'lat': detail.get('lat'),
            'lng': detail.get('lng')
        }

        if convenience:
            park = convenience.get('park')
            if park:
                nearby = park.get('nearBy')
                if nearby:
                    result['park_name'] = nearby.get('name')
                    result['park_dist'] = nearby.get('dist')

            mart = convenience.get('mart')
            if mart and len(mart) > 0:
                result['mart_name'] = mart[0].get('name')
                result['mart_dist'] = mart[0].get('dist')

            hospital = convenience.get('hospital')
            if hospital and len(hospital) > 0:
                result['hospital_name'] = hospital[0].get('name')
                result['hospital_dist'] = hospital[0].get('dist')

        areas = detail.get('area', [])
        if areas:
            for area in areas:
                area_info = {
                    'no': area.get('no'),
                    'private_area': area.get('private_area'),
                    'public_area': area.get('public_area'),
                    'real_trade_price': area.get('real_trade_price'),
                    'real_rent_price': area.get('real_rent_price'),
                    'real_rent_ratio': area.get('real_rent_ratio'),
                    'max_real_trade_price': area.get('max_real_trade_price'),
                    'max_real_rent_price': area.get('max_real_rent_price'),
                    'total_household': area.get('total_household'),
                    'type_official_price_data': area.get('type_official_price_data')
                }
                result['areas'].append(area_info)

        for subwayname in subwaynames:
            result[subwayname] = ''

        subway_info = {}
        subways = convenience.get('subway', [])
        if subways:
            for subway in subways:
                line = subway.get('description', '')
                station_dist = subway.get('dist', '')

                if line not in subway_info or station_dist < subway_info[line]:
                    subway_info[line] = station_dist

        for subwayname in subwaynames:
            result[subwayname] = subway_info.get(subwayname, '')

        ktxs = convenience.get('ktx', [])
        if ktxs:
            for ktx in ktxs:
                ktx_info = {
                    'ktx_name': ktx.get('name'),
                    'ktx_dist': ktx.get('dist')
                }
                result['ktxs'].append(ktx_info)

        elementary_schools = schoolInfo.get('elementarySchool', {}).get('schools', [])
        if elementary_schools:
            for school in elementary_schools:
                if school.get('isClosest'):
                    result['elementarySchool_name'] = school.get('name')
                    result['elementarySchool_dist'] = school.get('dist')
                    result['elementarySchool_duration'] = school.get('duration')
                    break

        preschools = preschool.get('childcares', [])
        if preschools:
            for ps in preschools:
                if ps.get('isClosest'):
                    result['preschool_name'] = ps.get('name')
                    result['preschool_dist'] = ps.get('dist')
                    break

        commute_destinations = ['강남', '을지로', '여의도', '판교', '구로', '잠실', '홍대', '명동']
        for destination in commute_destinations:
            result[destination] = None

        if commutes:
            for commute in commutes:
                destination = commute.get('name')
                time = commute.get('time')
                if destination in commute_destinations:
                    result[destination] = time

        return result




    def extract_data_from_raw_json_mult(self, save=True):
        directory = self.info_folder
        filenames = [file for file in os.listdir(directory) if '.json' in file]
        results = []
        

        now = 0
        total = len(filenames)
        for filename in filenames:
            id = filename.split('.')[0]
            now += 1 
            print(f'{now}/{total}')
            if now % 20 == 0 : clear_output()   

            result = self.extract_data_from_raw_json(id)
            results.append(result)
            display(results)
        if save :
            df = pd.DataFrame(results)
            df.to_csv(self.info_path, encoding='cp949', errors='replace', index=False)
        
        return df
    
    def fetch_apt_info(self, id = "1SZ1d", save=True) :
        cookies = {
            # 'bat': 'B-VEzEDDnAr6CcP6k_SI0s2QqZ78PHXDpJkw',
            # '_gcl_au': '1.1.1543066674.1719753966',
            # '_fbp': 'fb.1.1719753965794.820917726471047565',
            # 'connect.sid': 's%3AWDykq4Ufmiq3wD4YVgE34w6twNhgCqtCGQ.xKitUHsxlmX16ciR7EQpy2bSBeKpoSv%2BBOJrHM3Nch0',
            # 'client.cid': 'xKitUHsxlmX16ciR7EQpy2bSBeKpoSv%2BBOJrHM3Nch0',
            # '_gid': 'GA1.2.494390124.1722309366',
            # '_wp_uid': '1-821aee09be2ee8d0af9029b7e4a8355c-s1711704073.904983|android|chrome-8e7669',
            # '_ga_P8RWS72S79': 'GS1.1.1722309366.52.1.1722310192.0.0.0',
            # '_ga': 'GA1.2.1496764594.1719753966',
            # 'cto_bundle': 'HAXCUF84WlQwJTJCZTBFYUZ4RlglMkJQdXJhMCUyQjRhNkZFeiUyQk9Na3k0MFQ1ciUyQk5jZkFSR1NsdEJGMW5idVEwOW1SJTJGZVFRJTJGS28zN3FaUXhrSnI1WGdVb3VoWkVNYThJQjhnOEFBUlpMZ0ZXM1Rwb3dVdFMlMkJpZUkzeUpaZDZiTiUyRkM1YktnZyUyRkdxVEthUkhna0RWdmJXcUdpQnN5TVFXVHN2WExPN005ek1RZDc0TmhCWHZrQVhJaUdhTG5RT2lGVGFhelBNOXFjb3EydVpyJTJCZW9meTlrOWVQYTh4N09iZGJyTEUxb3pFZGpiSCUyRk9KbEtrc3loUmRLNDlyams2YzNMbjluZFlXUFdpa3Vvd3FaSEVDR1N3ejd5dGpsejdOZyUzRCUzRA',
        }

        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            # 'cache-control': 'max-age=0',
            # 'cookie': 'bat=B-VEzEDDnAr6CcP6k_SI0s2QqZ78PHXDpJkw; _gcl_au=1.1.1543066674.1719753966; _fbp=fb.1.1719753965794.820917726471047565; connect.sid=s%3AWDykq4Ufmiq3wD4YVgE34w6twNhgCqtCGQ.xKitUHsxlmX16ciR7EQpy2bSBeKpoSv%2BBOJrHM3Nch0; client.cid=xKitUHsxlmX16ciR7EQpy2bSBeKpoSv%2BBOJrHM3Nch0; _gid=GA1.2.494390124.1722309366; _wp_uid=1-821aee09be2ee8d0af9029b7e4a8355c-s1711704073.904983|android|chrome-8e7669; _ga_P8RWS72S79=GS1.1.1722309366.52.1.1722310192.0.0.0; _ga=GA1.2.1496764594.1719753966; cto_bundle=HAXCUF84WlQwJTJCZTBFYUZ4RlglMkJQdXJhMCUyQjRhNkZFeiUyQk9Na3k0MFQ1ciUyQk5jZkFSR1NsdEJGMW5idVEwOW1SJTJGZVFRJTJGS28zN3FaUXhrSnI1WGdVb3VoWkVNYThJQjhnOEFBUlpMZ0ZXM1Rwb3dVdFMlMkJpZUkzeUpaZDZiTiUyRkM1YktnZyUyRkdxVEthUkhna0RWdmJXcUdpQnN5TVFXVHN2WExPN005ek1RZDc0TmhCWHZrQVhJaUdhTG5RT2lGVGFhelBNOXFjb3EydVpyJTJCZW9meTlrOWVQYTh4N09iZGJyTEUxb3pFZGpiSCUyRk9KbEtrc3loUmRLNDlyams2YzNMbjluZFlXUFdpa3Vvd3FaSEVDR1N3ejd5dGpsejdOZyUzRCUzRA',
            # 'priority': 'u=0, i',
            # 'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            # 'sec-ch-ua-mobile': '?0',
            # 'sec-ch-ua-platform': '"Windows"',
            # 'sec-fetch-dest': 'document',
            # 'sec-fetch-mode': 'navigate',
            # 'sec-fetch-site': 'none',
            # 'sec-fetch-user': '?1',
            # 'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36',
        }

        params = {
            'from': 'map',
        }

        response = requests.get(f'https://hogangnono.com/apt/{id}/0/1', params=params, cookies=cookies, headers=headers)

        try:
            result = response.text
            soup = BeautifulSoup(result, 'html.parser')
            script_tag = soup.find('script', {'id': '__HGNN_DATA__', 'type': 'application/json'})
            
            if script_tag:
                json_data = json.loads(script_tag.string)
                file_path = os.path.join(self.info_folder, f"{id}.json")
                
                if save :
                    with open(file_path, 'w', encoding='utf-8') as file:
                        json.dump(json_data, file, ensure_ascii=False, indent=4)
                return json_data
            else:
                print(f"Script tag with id '__HGNN_DATA__' not found for id: {id}")
                return result
        except Exception as e:
            print(f"Error processing id {id}: {e}")
            return result

    def merge(self, type="merge_apts_info_real_trade", real_trade='original'):
        """수집된 정보들을 통합합니다.
        type : merge_apts_info_real_trade | merge_apts_info"""
        print(
            "df len :", len(self.info),
            "df_apts len :", len(self.apts),
            "df_real_trade len :", len(self.real_trade)
        )
        # 두 데이터프레임을 동일 id를 기준으로 합칩니다.
        merged_df = pd.merge(self.apts, self.info, on='id', suffixes=('', '_drop'))
        merged_df.drop([col for col in merged_df.columns if 'drop' in col], axis=1, inplace=True)
        

        # 지하철관련 정보추가
        for idx, row in merged_df.iterrows() :
            search_range = row['1호선' : '경강선']
            minimum_distance = search_range.min()
            if search_range.sum() :
                line = list(search_range[search_range == minimum_distance].index)[0]
                line_close_distance = list(search_range[search_range.astype(float) < minimum_distance + 150].index)

            merged_df.loc[idx, '가장가까운지하철역'] = line
            merged_df.loc[idx, '가장가까운지하철역의거리'] = minimum_distance
            merged_df.loc[idx, '비슷한거리지하철역(150m 이내차이)'] = str(line_close_distance)    
    
    
        
        if type == "merge_apts_info":
            merged_df.to_csv(self.merge_apts_info_path, encoding='cp949', index=False)
        elif type == "merge_apts_info_real_trade":
            if real_trade == 'original':
                merged_df = pd.merge(merged_df, self.real_trade, on='id', suffixes=('', '_drop'))
                merged_df.drop([col for col in merged_df.columns if 'drop' in col], axis=1, inplace=True)
                merged_df.to_csv(self.merge_apts_info_real_trade_path, encoding='cp949', index=False)
            elif real_trade == 'interpolated':
                merged_df = pd.merge(merged_df, self.interpolated_real_trade, on='id', suffixes=('', '_drop'))
                merged_df.drop([col for col in merged_df.columns if 'drop' in col], axis=1, inplace=True)
                merged_df.to_csv(self.merge_apts_info_interpolated_real_trade_path, encoding='cp949', index=False)
            elif real_trade == 'filled':
                merged_df = pd.merge(merged_df, self.interpolated_filled_real_trade, on='id', suffixes=('', '_drop'))
                merged_df.drop([col for col in merged_df.columns if 'drop' in col], axis=1, inplace=True)
                merged_df.to_csv(self.merge_apts_info_interpolated_filled_real_trade_path, encoding='cp949', index=False)
        
        return merged_df

        # # 합쳐진 데이터프레임을 반환합니다.
        # len(merged_df)


    
        
# 사용 예시
hgnn = Hogangnono()

