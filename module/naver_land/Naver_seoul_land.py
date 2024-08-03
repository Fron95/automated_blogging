import requests
import copy
import time
import json
import pandas as pd
import ast
import os
import re

class Naver_seoul_land() :
    def __doc__(self) : 
        print("""
네이버부동산 크롤링 클래스입니다.
사용방법은 다음과 같습니다.

1. 
              """)
        
    def __init__(self) :
        self.base_dir = '부동산'
        if not os.path.exists(self.base_dir):
            os.mkdir(self.base_dir)

        self.total_apts_dir = os.path.join(self.base_dir, '전국.csv')        
        self.total_apts = pd.read_csv(self.total_apts_dir, encoding='cp949')
        self.apts = self.total_apts.copy()

        self.cols_article = ['articleNo', 'articleName', 'realEstateTypeName', 'tradeTypeName', 'floorInfo', 'isPriceModification', 'dealOrWarrantPrc', 'areaName', 'area1', 'area2', 'direction', 'articleConfirmYmd', 'articleFeatureDesc', 'tagList', 'buildingName', 'sameAddrCnt', 'sameAddrMaxPrc', 'sameAddrMinPrc', 'pyeongs']
        self.cols_trade = ['tradeType', 'floor' ,'formattedPrice', 'formattedTradeYearMonth']
        self.cols_info = ['complexTypeName', 'complexName', 'totalHouseHoldCount', 'totalDongCount', 'useApproveYmd', 'minArea', 'maxArea']
        self.cols_pyeongs = ['pyeongs']

    def config_district(self, name_district) :
        """지역설정"""
        self.district_dir = os.path.join(self.base_dir, name_district)
        if not os.path.exists(self.district_dir):
            os.mkdir(self.district_dir)
        self.apts_dir = os.path.join(self.district_dir, f'{name_district}.csv')
        self.article_dir = os.path.join(self.district_dir, f'{name_district}_매물.csv')
        self.trade_dir = os.path.join(self.district_dir, f'{name_district}_실거래.csv')
        self.info_dir = os.path.join(self.district_dir, f'{name_district}_정보.csv')

        self.apts = self.total_apts[self.total_apts['cortarName_district'] == name_district]
        self.apts.reset_index(drop=True, inplace=True)
        self.apts.to_csv(os.path.join('부동산', name_district, f'{name_district}.csv'), encoding='cp949', index=False)

        self.renew()

    def renew(self) :
        try :
            self.apts_info = self.load('info')
        except :
            pass
        try :
            self.apts_article = self.load('article')
        except :
            pass
        try :
            self.apts_trade = self.load('trade')
        except :
            pass


    def save(self, data, kind) :
        if isinstance(data, dict) and all(isinstance(v, (int, float, str)) for v in data.values()):
            df = pd.DataFrame([data])

        else:
            df = pd.DataFrame(data)

        def convert_price(x):
            if isinstance(x, int):
                return x * 10000 if x <= 100 else x
            if not isinstance(x, str):
                return x
            try:
                if '억' in x:
                    parts = x.split('억')
                    if len(parts) == 2 and parts[1].strip():
                        return int(parts[0].strip()) * 10000 + int(re.sub(r'[^\d]', '', parts[1]))
                    else:
                        return int(parts[0].strip()) * 10000
                else:
                    return int(re.sub(r'[^\d]', '', x))
            except ValueError:
                return x
        
        if kind == 'article' :
            df['floorInfo'] = df['floorInfo'].apply(lambda x : x+'층')
            
            df['dealOrWarrantPrc'] = df['dealOrWarrantPrc'].apply(convert_price)
            df.to_csv(self.article_dir, encoding='cp949', index=False)
        elif kind == 'trade' :
            df['formattedPrice'] = df['formattedPrice'].apply(convert_price)
            # for idx, row in df.iterrows():
            #     area_no = row['areaNo']
            #     pyeongs = land.str2dict(row['pyeongs'])
            #     if str(area_no) in pyeongs:
            #         df.at[idx, 'pyeong'] = pyeongs[str(area_no)]
            df.to_csv(self.trade_dir, encoding='cp949', index=False)
        elif kind == 'info' :
            df.to_csv(self.info_dir, encoding='cp949', index=False)
        else :
            print("kind에 article, trade, info 중 하나를 넣으세요.")
        return df
    
    def load(self, kind) :
        
        if kind == 'article' :
            df = pd.read_csv(self.article_dir, encoding='cp949', )
        elif kind == 'trade' :
            df =pd.read_csv(self.trade_dir, encoding='cp949', )
        elif kind == 'info' :
            df =pd.read_csv(self.info_dir, encoding='cp949', )
        else :
            print("kind에 article, trade, info 중 하나를 넣으세요.")
        return df
        
    
    def get_dong(self, cortarNo ="1120000000") :
        """구 이하 동이름 가져오기"""
        url = "https://new.land.naver.com/api/regions/list"
        headers = {
            "Cookie": "NNB=FCKCGABYXJBGM; ASID=de6c8eec0000018fe0e3f4d60000005d; NAC=r45BBMwegqUeB; NACT=1; nhn.realestate.article.rlet_type_cd=A01; nhn.realestate.article.trade_type_cd=; nhn.realestate.article.ipaddress_city=1100000000; _fwb=61LHhDmgSVSDTIn6beSYcT.1719020991264; landHomeFlashUseYn=Y; page_uid=iFhWwdqVOsCssiyk1dGsssssskR-268088; _fwb=61LHhDmgSVSDTIn6beSYcT.1719020991264; REALESTATE=Sat%20Jun%2022%202024%2011%3A04%3A44%20GMT%2B0900%20(KST); wcs_bt=4f99b5681ce60:1719021885; BUC=fZZA8_pWVcDwPBsokKy-ABqKINLnOafN4vdJCZoIdxs=",
            "Referer": "https://new.land.naver.com/complexes?ms=37.554416,127.0195285,17&a=APT:ABYG:JGC:PRE&e=RETAIL",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        }

        params = {
            "cortarNo": cortarNo
        }

        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        cortar_list = [( region['cortarNo'], region['cortarName'],) for region in data['regionList']]
        return cortar_list
    
    # 아파트 목록가져오기
    def get_apts(self, cortarNo = "1120011000") :
        """동 이하 아파트 이름 가져오기"""

        url = "https://new.land.naver.com/api/regions/complexes"
        headers = {
            "Cookie": "NNB=FCKCGABYXJBGM; ASID=de6c8eec0000018fe0e3f4d60000005d; NAC=r45BBMwegqUeB; NACT=1; nhn.realestate.article.rlet_type_cd=A01; nhn.realestate.article.trade_type_cd=; nhn.realestate.article.ipaddress_city=1100000000; _fwb=61LHhDmgSVSDTIn6beSYcT.1719020991264; landHomeFlashUseYn=Y; page_uid=iFhWwdqVOsCssiyk1dGsssssskR-268088; _fwb=61LHhDmgSVSDTIn6beSYcT.1719020991264; REALESTATE=Sat%20Jun%2022%202024%2011%3A04%3A44%20GMT%2B0900%20(KST); wcs_bt=4f99b5681ce60:1719021885; BUC=fZZA8_pWVcDwPBsokKy-ABqKINLnOafN4vdJCZoIdxs=",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        }

        params = {
            "cortarNo": cortarNo,
            "realEstateType": "APT:PRE",
            "order": ""
        }

        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        cortar_list = [( region['complexNo'], region['complexName'],) for region in data['complexList']]
        return cortar_list

    def get_apts_mult(self, districts) : 
        """구 이하 아파트 이름 가져오기"""
        results = []

        for district in districts :
            no_district, name_district = district[0], district[1]
            
            dongs = self.get_dong(no_district)

            for dong in dongs : 
                no_dong, name_dong = dong[0], dong[1]

                apts = self.get_apts(no_dong)

                for apt in apts :
                    no_apt, name_apt = apt[0], apt[1]
                    results.append((no_district,name_district,no_dong,name_dong,no_apt,name_apt))
        df = pd.DataFrame(results)
        df.columns = ['cortarNo_district','cortarName_district','cortarName_dong','name_dong','complexNo','complexName']

        return df
    
    # 매물조회
    def apt_items(self, 
                  complexNo = 1147, 
                  tradeType = "A1:B1", 
                  areaNos = '',
                  page = 1, 
                  rentPriceMin= 0,
                  rentPriceMax= 900000000,
                  priceMin= 0,
                  priceMax= 900000000,
                  areaMin= 0,
                  areaMax= 900000000,
                  oldBuildYears= "",
                  recentlyBuildYears= "",
                  minHouseHoldCount= "",
                  maxHouseHoldCount= "",
                  ) :
        """단일 물건에 대한 매물정보 (호가정보) 가져오기.
        complexNo : 물건id
        tradeType : A1(매매) | B1(전세)
        areaNos : 미기재 시 전체 평수에 대해. 복수 선택은 :으로 이어붙임. (예시. 1:2)
        page : scroll 에 따라 추가정보 호출."""

        url = f"https://new.land.naver.com/api/articles/complex/{complexNo}"
        headers = {
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IlJFQUxFU1RBVEUiLCJpYXQiOjE3MTkwMjQ2MTEsImV4cCI6MTcxOTAzNTQxMX0.x3jYojHGWB6R2BHcODH8LI4CaxaxyHdcHFucBFCIS0Y",
            "Cookie": "NNB=FCKCGABYXJBGM; ASID=de6c8eec0000018fe0e3f4d60000005d; NAC=r45BBMwegqUeB; NACT=1; nhn.realestate.article.rlet_type_cd=A01; nhn.realestate.article.trade_type_cd=; nhn.realestate.article.ipaddress_city=1100000000; _fwb=61LHhDmgSVSDTIn6beSYcT.1719020991264; landHomeFlashUseYn=Y; page_uid=iFhWwdqVOsCssiyk1dGsssssskR-268088; _fwb=61LHhDmgSVSDTIn6beSYcT.1719020991264; REALESTATE=Sat%20Jun%2022%202024%2011%3A50%3A11%20GMT%2B0900%20(KST); wcs_bt=4f99b5681ce60:1719024611; BUC=Dwr5Ph9_Z0h12xcrVOHR5Bz1D2_7_i3ypl51m0vlbfk=",
            "Referer": "https://new.land.naver.com/complexes/1147?ms=37.544731,126.9391515,17&a=APT:PRE&b=A1&e=RETAIL",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        }

        params = {
            "realEstateType": "APT:PRE",
            "tradeType": tradeType,
            "tag": "::::::::",
            "rentPriceMin": rentPriceMin,
            "rentPriceMax": rentPriceMax,
            "priceMin": priceMin,
            "priceMax": priceMax,
            "areaMin": areaMin,
            "areaMax": areaMax,
            "oldBuildYears": oldBuildYears,
            "recentlyBuildYears": recentlyBuildYears,
            "minHouseHoldCount": minHouseHoldCount,
            "maxHouseHoldCount": maxHouseHoldCount,
            "showArticle": "false",
            "sameAddressGroup": "true",
            "minMaintenanceCost": "",
            "maxMaintenanceCost": "",
            "priceType": "RETAIL",
            "directions": "",
            "page": page,
            "complexNo": complexNo,
            "buildingNos": "",
            "areaNos": areaNos,
            "type": "list",
            "order": "rank"
        }

        response = requests.get(url, headers=headers, params=params)
        result = response.json()

        return result
    
    def apt_items_mult(self, 
                  complexNo = 1147, 
                  tradeType = "A1:B1", 
                  areaNos = '',
                  page = 1, 
                  rentPriceMin= 0,
                  rentPriceMax= 900000000,
                  priceMin= 0,
                  priceMax= 900000000,
                  areaMin= 0,
                  areaMax= 900000000,
                  oldBuildYears= "",
                  recentlyBuildYears= "",
                  minHouseHoldCount= "",
                  maxHouseHoldCount= "",
                  sleep = 1,
                merge = 'apts') :
        
        results = []
        is_more_data = True
        while is_more_data :
            try:
                raw_data = self.apt_items(
                    complexNo = complexNo,
                    tradeType = tradeType,
                    areaNos = areaNos,
                    page = page,
                    rentPriceMin = rentPriceMin,
                    rentPriceMax = rentPriceMax,
                    priceMin = priceMin,
                    priceMax = priceMax,
                    areaMin = areaMin,
                    areaMax = areaMax,
                    oldBuildYears = oldBuildYears,
                    recentlyBuildYears = recentlyBuildYears,
                    minHouseHoldCount = minHouseHoldCount,
                    maxHouseHoldCount = maxHouseHoldCount,
                )

                if merge == 'apts_info' :
                    result = self.apts_info[self.apts['complexNo'] == complexNo].to_dict()  # 기존 row의 데이터 포함
                elif merge == 'apts' : 
                    result = self.apts[self.apts['complexNo'] == complexNo].to_dict()  # 기존 row의 데이터 포함
                else :
                    result = pd.DataFrame()

                is_more_data = raw_data['isMoreData']
                for article in raw_data['articleList'] :
                    for col in self.cols_article :
                        if col in article :
                            result.loc[:,col] = article[col]
                    
                    results.append(copy.deepcopy(result))

            except Exception as e:
                print(f"Error fetching data for complexNo {complexNo} and areaNo {areaNos}: {e}")
                is_more_data = False
            
            page += 1 
            time.sleep(sleep)
        return results


    # 단지정보
    def apt_info(self, complexNo = 1147, merge = True) :
        """단지정보 조회"""
        url = f"https://new.land.naver.com/api/complexes/overview/{complexNo}"
        headers = {
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IlJFQUxFU1RBVEUiLCJpYXQiOjE3MTkwMjUyNDAsImV4cCI6MTcxOTAzNjA0MH0.ld0GtF1d0IZK-kDSqcmFarUz00qPN7g-7i_J5RpgTDY",
            "Cookie": "NNB=FCKCGABYXJBGM; ASID=de6c8eec0000018fe0e3f4d60000005d; NAC=r45BBMwegqUeB; NACT=1; nhn.realestate.article.rlet_type_cd=A01; nhn.realestate.article.trade_type_cd=; nhn.realestate.article.ipaddress_city=1100000000; _fwb=61LHhDmgSVSDTIn6beSYcT.1719020991264; landHomeFlashUseYn=Y; page_uid=iFhWwdqVOsCssiyk1dGsssssskR-268088; _fwb=61LHhDmgSVSDTIn6beSYcT.1719020991264; REALESTATE=Sat%20Jun%2022%202024%2012%3A00%3A40%20GMT%2B0900%20(KST); BUC=RCphcWIuUeinf-MgG0Dke4l0F8fEAWdtIj-xN1lIlTE=; wcs_bt=4f99b5681ce60:1719025241",
            "Priority": "u=1, i",
            "Referer": "https://new.land.naver.com/complexes?ms=37.544731,126.942547,17&a=APT:ABYG:JGC:PRE&b=A1&e=RETAIL",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        }

        params = {
            "complexNo": complexNo
        }

        response = requests.get(url, headers=headers, params=params)
        raw_data = response.json()
        if merge : 
            result = self.apts[self.apts['complexNo'] == complexNo]
        else :
            result = pd.DataFrame()

        for col in self.cols_info :         
            try :
                result.loc[:, col] = raw_data.get(col, '')
            except Exception as e :
                print(f"at complexNo : {complexNo}, error occured with column : {col}")
                continue
        for col in self.cols_pyeongs : 
            pyeong_info = {}
            for pyeong in raw_data[col] :
                pyeong_info[pyeong['pyeongNo']] =  pyeong['exclusiveArea']        
            str_result = json.dumps(pyeong_info)
            result.loc[:,col] = str_result

        return result

    
    # 실거래가
    def real_trade(self, complexNo=1147, areaNo=0, db = 'apts') :
        """아파트 특정 평수 실거래가 조회"""

        url = f"https://new.land.naver.com/api/complexes/{complexNo}/prices/real"
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IlJFQUxFU1RBVEUiLCJpYXQiOjE3MTkwMjYwNzYsImV4cCI6MTcxOTAzNjg3Nn0.-ohhan7oQNVxYwRI3nmwcmE3JeyD3M-HkvPJVShbEu4",
            "Cookie": "NNB=FCKCGABYXJBGM; ASID=de6c8eec0000018fe0e3f4d60000005d; NAC=r45BBMwegqUeB; NACT=1; nhn.realestate.article.rlet_type_cd=A01; nhn.realestate.article.trade_type_cd=; nhn.realestate.article.ipaddress_city=1100000000; _fwb=61LHhDmgSVSDTIn6beSYcT.1719020991264; landHomeFlashUseYn=Y; page_uid=iFhWwdqVOsCssiyk1dGsssssskR-268088; _fwb=61LHhDmgSVSDTIn6beSYcT.1719020991264; REALESTATE=Sat%20Jun%2022%202024%2012%3A14%3A36%20GMT%2B0900%20(KST); wcs_bt=4f99b5681ce60:1719026076; BUC=p18HRKA3Y0XSqzq3tugbJNgv64iu42F1PQpR6QUumsI=",
            "Priority": "u=1, i",
            "Referer": "https://new.land.naver.com/complexes/1147?ms=37.5404435,126.9390494,16&a=APT:ABYG:JGC:PRE&b=A1&e=RETAIL&ad=true",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        }

        params = {
            "complexNo": complexNo,
            "tradeType": "A1",
            "year": 5,
            "priceChartChange": "false",
            "areaNo": areaNo,
            "type": "table"
        }
        response = requests.get(url, headers=headers, params=params)
        raw_data = response.json()['realPriceOnMonthList'] 

        results = []

        try:
            if db == 'apts_info' :
                result = self.apts_info[self.apts['complexNo'] == complexNo].iloc[0, :].to_dict()  # 기존 row의 데이터 포함
            else : 
                result = self.apts[self.apts['complexNo'] == complexNo].iloc[0, :].to_dict()  # 기존 row의 데이터 포함
            result['areaNo'] = areaNo

            for month in raw_data :
                for trade in month['realPriceList'] :
                    for col in self.cols_trade:
                        if col in trade:
                            result.loc[:,col] = trade[col]
                    results.append(result.copy())
        except Exception as e:
            print(f"Error fetching data for complexNo {complexNo} and areaNo {areaNo}: {e}")

        return result
    
    def str2dict(self, data) :
        return ast.literal_eval(data)
    
    def get_pyeongs(self, complexNo) :
        pyeongs = self.apts_info[self.apts_info['complexNo'] == complexNo]['pyeongs'].values[0]
        pyeongs = self.str2dict(pyeongs)
        return pyeongs


         

    def real_trade_mult(self, complexNo, pyeongs,  db = 'apts') : 
        """아파트 단위 실거래가 조사"""
        results = []
        for areaNo, pyeong in pyeongs.items():
            try:
                result = self.real_trade(complexNo=complexNo, areaNo=areaNo, db=db)
                for idx in range(len(result)) :
                    result[idx] = result[idx]['pyeong'] = pyeong
                results.append(result.copy())
            except Exception as e:
                print(f"Error fetching data for complexNo {complexNo} and areaNo {areaNo}: {e}")
        return results
