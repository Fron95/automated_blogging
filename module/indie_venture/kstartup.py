import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import httpx
import re
import html

def html_to_text(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text(separator="\n")
    return text

def kstartup_single_page(page):
    headers = {
        'accept': '*/*',
    }
    params = {
        'serviceKey': os.getenv("KSTARTUP_API_KEY"),
        'returnType': 'json',
        'page': page
        # "cond[biz_yr::EQ]": "2024"
    }

    parsed_data = []
    with httpx.Client(verify=False) as client:
        response = client.get(
            'https://apis.data.go.kr/B552735/kisedKstartupService/getAnnouncementInformation',
            params=params,
            headers=headers,
        )
        try :
            items = response.json()['data']
        except :
            return 
        for item in items:
            cols = {
                'title': html.unescape(item.get('intg_pbanc_biz_nm', '')),
                'description': html_to_text(item.get('pbanc_ctnt', '')),
                'organization': item.get('pbanc_ntrp_nm', ''),
                'category': item.get('supt_biz_clsfc', ''),
                'url': item.get('detl_pg_url', ''),
                'provider': 'K-스타트업',
                'region': item.get('supt_regin', ''),  # 이 정보는 제공되지 않음
                'startDate': item.get('pbanc_rcpt_bgng_dt', ''),
                'endDate': item.get('pbanc_rcpt_end_dt', ''),
                'registerDate': None
            }

            parsed_data.append(cols)
    return pd.DataFrame(parsed_data)

def kstartup_multi_page(start=1, end=999):
    isContinue = True
    results = pd.DataFrame()
    page = start
    while isContinue and page < end + 1:
        print(f'[SYSTEM] KSTARTUP {page}/{end} 조회 중')
        result = kstartup_single_page(page=page)
        if result.empty:
            isContinue = False
        else:
            results = pd.concat([results, result], ignore_index=True)
        page += 1
    return pd.DataFrame(results)

