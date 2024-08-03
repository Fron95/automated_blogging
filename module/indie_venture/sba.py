import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import httpx
import re


def sba_single_page( page):
    url = "https://www.sba.seoul.kr/Pages/ContentsMenu/Company_Support.aspx/GetData"

    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Content-Length": "201",
        "Content-Type": "application/json; charset=UTF-8",
        "Cookie": "_ba_exist=true; _BS_GUUID=UrIaqEVCuHMafaZCxSqwpjAxkztgyQhsiZCJExl9; ASP.NET_SessionId=tk5kyzzwxtygahrqqtoiv1l1; _TRK_CR=https%3A%2F%2Fsearch.naver.com%2Fsearch.naver%3Fsm=tab_hty.top%26where=nexearch%26ssc=tab.nx.all%26query=sba%26oquery=K-%25EC%258A%25A4%25ED%2583%2580%25ED%258A%25B8%25EC%2597%2585%26tqi=iFCsIwqVN8CssO%252FALd4ssssstQZ-156651; _TRK_CQ=%3FC=AFF3B5BF-6677-EC11-80E8-9418827691E2; CK_Load=0; CS_PG=12; CS_PN=1; CS_O=END; CS_K=0; CS_S=; CS_H=; WMONID=ZZVrqCS0hMg; _ba_rand=66; _ba_initial_refer=; _ba_ssid=njVQfy4y; _ba_page_seq=0; _ba_parent_seq=0; _ba_page_ct=2024-06-24T09%3A14%3A27.735Z; _ba_last_url=https%3A%2F%2Fwww.sba.seoul.kr%2FPages%2FContentsMenu%2FCompany_Support.aspx%3FC%3DAFF3B5BF-6677-EC11-80E8-9418827691E2; _ba_initial_refer=; _TRK_UID=604a1e37ec753370d320099906f1399f:4:1.192666976273148:1719220467750; _TRK_SID=e0766440b210600e9b18cee70a651010; CS_C=AFF3B5BF-6677-EC11-80E8-9418827691E2; _TRK_EX=3; _ba_reload_count=2",
        "Host": "www.sba.seoul.kr",
        "Origin": "https://www.sba.seoul.kr",
        "Referer": "https://www.sba.seoul.kr/Pages/ContentsMenu/Company_Support.aspx?C=AFF3B5BF-6677-EC11-80E8-9418827691E2",
        "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Google Chrome\";v=\"126\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }

    data = {
        "param": {
            "P_TYPE": "List",
            "P_PAGING": 12,
            "P_PAGE_NUM": page,
            "P_MENU_ID": "6FA70790-6677-EC11-80E8-9418827691E2",
            "P_CONTACTID": "",
            "P_HASHTAG": "",
            "P_KEYWORD": "0",
            "P_ORDER": "REG",
            "P_RECORDID": "",
            "P_SEARCH": ""
        }
    }

    response = requests.post(url, headers=headers, json=data, verify=False)
    
    contents = response.json()["d"]["contents"]
    if len(contents) < 1 :
        print('[SYSTEM] 마지막 페이지 도달')
        return 

    data_list = []
    for content in contents:
        data = {
            'title': content.get('new_name', ''),
            'description': content.get('new_ntxt_mig_content', ''),
            'organization': content.get('new_txt_mig_org_nm', ''),
            'category': content.get('new_txt_mig_category2_nm', ''),
            'url': f"https://www.sba.seoul.kr/Pages/ContentsMenu/Company_Support_Detail.aspx?RID={content.get('recordId')}",
            'provider': '서울경제진흥원',
            'region': '',  # region 정보가 JSON에 없으므로 빈 문자열로 설정
            'startDate': content.get('new_dt_mig_sdate', ''),
            'endDate': content.get('new_dt_mig_edate', ''),
            'registerDate' : ''
        }
        data_list.append(data)

    return pd.DataFrame(data_list)


def sba_multi_page( start=1, end=999):
    isContinue = True
    results = pd.DataFrame()
    page = start
    while isContinue and page < end + 1 :
        print(f'[SYSTEM] SBA {page}/{end} 조회 중')
        result = sba_single_page(page = page)
        if type(result) == type(None) :
            isContinue = False
        else :
            results = pd.concat([results, result], ignore_index=True)
        page += 1
    return pd.DataFrame(results)