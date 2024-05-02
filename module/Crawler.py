# 필요한 외부 라이브러리를 임포트 합니다.
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import copy
import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains
# ddg
from duckduckgo_search import DDGS
# 크롤러라는 클래스를 정의합니다.
class Crawler():
    # 상태를 지정합니다.
    def __init__(self, verbose=False, isHeadless=True) :          
        """Crawler 클래스의 생성자로, 인스턴스 생성 시 초기 설정을 합니다.
        verbose: 부울 값으로, True 설정 시 실행 과정에서 상세 로그를 출력합니다.
        """
        self.driver = self.turn_on_selenium(is_headless=isHeadless)  # 셀레니움 브라우저를 헤드리스 모드 여부를 결정하여 초기화합니다.
        self.verbose = verbose  # 실행 과정에서 로그를 출력할지의 여부를 저장합니다.
        self.base_search_urls = {
            # 각 검색 엔진별 기본 검색 URL을 설정합니다. <your_query>는 검색어로 대체됩니다.
                    "daum" : f'https://search.daum.net/search?nil_suggest=btn&w=tot&DA=SBC&q=<your_query>',
                    "naver" : f'https://search.naver.com/search.naver?ssc=tab.blog.all&sm=tab_jum&query=<your_query>',
                    "google" : f'https://www.google.com/search?q=<your_query>&sca_esv=a19c4e940f5aec6f&rlz=1C1IBEF_koKR958KR958&ei=UjTbZePvLeGP2roPzY2qiAo&udm=&ved=0ahUKEwjj4I7ZwMaEAxXhh1YBHc2GCqEQ4dUDCBA&uact=5&oq=<your_query>&gs_lp=Egxnd3Mtd2l6LXNlcnAiD-yKpO2LsOu4jOyeoeyKpDIFEC4YgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAuGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIFEC4YgAQyFBAuGIAEGJcFGNwEGN4EGN8E2AEBSLoOUIQFWNQLcAN4ApABA5gBjAGgAdkLqgEEMC4xMrgBA8gBAPgBAZgCCKACvgTCAgQQABhHwgIEEAAYA8ICCxAAGIAEGLEDGIMBwgIEEC4YA8ICERAuGIAEGLEDGIMBGMcBGNEDwgIOEC4YgAQYsQMYxwEY0QPCAgoQLhiABBiKBRhDwgIKEAAYgAQYigUYQ8ICGRAuGIAEGIoFGEMYlwUY3AQY3gQY3wTYAQHCAgsQLhiABBixAxiDAcICChAuGEMYgAQYigXCAhkQLhhDGIAEGIoFGJcFGNwEGN4EGN8E2AEBmAMAiAYBkAYKugYGCAEQARgUkgcDNC40&sclient=gws-wiz-serp',
                    "google_image" : f"https://www.google.com/search?q=<your_query>&tbm=isch&ved=2ahUKEwjNvI38r-uEAxX4fvUHHaL9B4EQ2-cCegQIABAA&oq=<your_query>&gs_lp=EgNpbWciCXN0ZXZlam9iczIFEAAYgAQyBBAAGB4yCRAAGIAEGBgYCjIJEAAYgAQYGBgKMgkQABiABBgYGAoyCRAAGIAEGBgYCkiZ1CBQ8gFYkdMgcAF4AJABAJgBeqABgAmqAQM1Lja4AQPIAQD4AQGKAgtnd3Mtd2l6LWltZ6gCAMICBxAAGIAEGBjCAggQABiABBixA8ICBxAAGIAEGBOIBgE&sclient=img&ei=14juZY31Avj91e8PovufiAg&bih=1023&biw=2048"
                }
        self.tag_selectors = {
            # 각 검색 엔진 및 태그에 따른 CSS 선택자를 설정합니다.
            # 키워드
            'daum_open_keywords' :  'a.keyword', # 다음 오픈키워드
            'google_open_keywords' : 'div.s75CSd.u60jwe.r2fjmd.AB4Wff', # 구글 오픈키워드
            'daum_searchinput' : '#q.tf_keyword', # 다음 검색창
            'google_searchinput' : '#searchform textarea.gLFyf', # 구글 검색창
            'daum_suggest_keywords' : "span.txt_query", # 다음 서제스트키워드
            'google_suggest_keywords' : 'div.wM6W7d span', # 구글 서제스트키워드
            # 다음광고
            'daum_AD_normal' : '.list_ad li', #와이드광고, 프리미엄광고
            'daum_AD_special' : '#splinkColl .list_info.mg_cont.clear li', # 스페셜광고                        
            # 구글 컨텐츠 순서
            'google_contents_link' : 'div#rso.dURPMd  div.MjjYud a'# 구글 검색결과 링크 
            
        }
        self.basic_format = {
            # 데이터 수집 시 사용할 기본 데이터 구조를 설정합니다.
            'source' : [],
            'subject' : None,
            'num_ads' : None,            
            "tistory_rank_at_google" : None,
            'all_links' : None,
            "top_tistory_at_google" : None,
            'images':None
        }
        self.results = {} # 수집된 결과를 저장할 딕셔너리입니다.
    

    
    
    def load_results(self) :
        """수집된 결과를 데이터프레임으로 반환합니다."""
        return pd.DataFrame(self.results).T 
    def get_keywords(self) :
        """사용자에게 지금까지 수집한 키워드를 반환합니다."""
        return list(self.results.keys())
    
    def load_processed_results(self, num_ads = 7, tistory_rank_at_google = 10) :
        """수집된 결과를 데이터프레임으로 반환합니다.
          상업성 키워드와 google 에 tistory 노출이 10번째 이상인 키워드는 제거합니다."""
        df = pd.DataFrame(copy.deepcopy(self.results)).T # 새로운 데이터프레임을 깊은 복사를 통해 생성합니다.
        df = df[df['num_ads'] < num_ads] # 상업성 키워드 제거

        def safe_int_convert(x):
            try:
                return int(x)
            except ValueError:
                return None  # 숫자로 변환할 수 없는 경우 None 반환
        
        df["tistory_rank_at_google"] = df["tistory_rank_at_google"].apply(safe_int_convert)
        df = df[df["tistory_rank_at_google"] < tistory_rank_at_google] # google 에 tistory 노출 10번째 이상제거
        df.sort_values(by='tistory_rank_at_google', ascending=True,inplace=True) # 순위별 정렬
        return df
    
    def get_processed_keywords(self, num_ads = 7, tistory_rank_at_gogle = 10) :
        """수집된 결과를 리스트로 반환합니다.
          상업성 키워드와 google 에 tistory 노출이 10번째 이상인 키워드는 제거합니다."""
        df = self.load_processed_results(num_ads = num_ads, tistory_rank_at_gogle = tistory_rank_at_gogle)
        return list(df.index)
     
    
    
    def clear(self) :
        """수집된 결과를 초기화합니다."""
        self.results = {}

    def createURL(self, word, engine) :        
        """공백은 +로 바꾸어서 각 검색엔진의 검색창에 해당하는 URL을 반환합니다."""
        word = word.replace(" ", "+") # 공백을 +로 바꾸어줍니다.
        base_url = self.base_search_urls.get(engine) # 해당 검색 엔진의 기본 URL을 가져옵니다.
        if base_url:
            return base_url.replace("<your_query>", word) # <your_query>를 word로 바꾸어서 반환합니다.
        else: # 지원하지 않는 엔진이면 지원하지 않는다고 말해줍니다.
            print("지원되지 않는 엔진입니다.")
            return
    
    # 셀레니움 켜기
    def turn_on_selenium(self, is_headless=True):
        """셀레니움 드라이버를 초기화하고 크롬 인스턴스를 반환합니다.
        is_headless: 부울 값으로, True일 경우 헤드리스 모드로 크롬을 실행합니다.
        인스턴스 생성 시 자동 호출됩니다."""
        chrome_options = Options() # 크롬 옵션을 설정합니다.         
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        # 사용자 에이전트 설정
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        chrome_options.add_argument(f"user-agent={user_agent}")
        if is_headless: # headless : 헤드리스 모드로 설정합니다. (눈에 보이는 크롬화면을 표시하지 않음으로써 리소스를 아낍니다.)
            chrome_options.add_argument("--headless")         
        driver = webdriver.Chrome(options=chrome_options)  # 크롬을 실행시킵니다.               
        return driver # 크롬을 반환합니다.

    # 셀레니움 켜져있는지 확인
    def is_selenium_turned_on(self):
        """셀레니움이 켜져있지 않으면 켜고, 켜져있으면 아무것도 하지 않습니다."""
        if self.driver is None : 
            self.driver = self.turn_on_selenium() # 위에서 정의한 셀레니움 실행함수를 호출합니다.
        return

    def search(self, word, engine) :
        """셀레니움을 조작하여 해당 엔진의 검색창에 word를 검색한 상태의 페이지를 반환합니다."""
        self.is_selenium_turned_on() # 셀레니움이 켜져있는지 확인   
        self.driver.get(self.createURL(word, engine)) # 해당 엔진의 검색창에 word를 검색한 페이지로 이동합니다.

    # 셀레니움 클릭이벤트 일으키기
    def selenium_click_action(self, tag_css_selector):
        """셀레니움을 사용하여 CSS 쿼리 선택자에 따른 클릭 작업을 수행합니다."""
        self.is_selenium_turned_on() # 셀레니움이 켜져있는지 확인        
        # if self.verbose : print(f"💬 클릭")
        # 이제 driver를 사용하여 CSS 쿼리 선택자에 따른 클릭 작업 수행
        # 클릭하려는 태그가 화면에 표시되기를 기다립니다.
        WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, tag_css_selector)))
        element = self.driver.find_element(By.CSS_SELECTOR, tag_css_selector) # 클릭하려는 태그를 선택합니다.
        element.click() # 클릭합니다.
        # if self.verbose : print(f"✅ 클릭")
    
    def selenium_crawling(self, tag_css_selector, get_attribute = None) :
        """셀레니움을 사용하여 CSS 쿼리 선택자에 따른 텍스트를 수집합니다."""
        self.is_selenium_turned_on() # 셀레니움이 켜져있는지 확인        
        # if self.verbose : print(f"💬 스크래핑")
        elements = self.driver.find_elements(By.CSS_SELECTOR, tag_css_selector)   # 클릭하려는 태그를 선택합니다.
        if get_attribute != None : # 텍스트 외 다른 속성값을 수집하고 싶다면
            result = [element.get_attribute(get_attribute) for element in elements if element.text != '']        
        else : # 텍스트를 수집하고 싶은 경우
            result = [element.text for element in elements if element.text != '']        
        # if self.verbose : print('✅ 스크래핑', len(result))
        return result
    
    def add_new_keyword(self, keywords, source, subject = None) :
        """수집되지 않았던 새로운 키워드를 수집한 경우 self.results에 해당 단어의 수집공간을 생성합니다.
          이미 존재하는 키워드라면 아무것도 하지 않습니다."""
        if type(keywords) == str :
            keywords = [keywords] # 키워드가 문자열이면 리스트로 변환합니다.
        
        for keyword in keywords :
            if keyword not in self.results.keys() :
                self.results[keyword] = copy.deepcopy(self.basic_format) # 기본 데이터 형식을 복사하여 새 키워드에 할당합니다.
            self.results[keyword]['source'].append(source) # 데이터 출처 추가
            if subject is not None : self.results[keyword]['subject'] = subject # 데이터 출처 추가
    
    def save_results(self, word, key, data) :
        """수집된 데이터를 self.results에 저장합니다. 
        이미 존재하는 키워드라면 해당 키워드의 데이터를 업데이트합니다.                
        """
        if word not in self.results.keys() :
            self.results[word] = copy.deepcopy(self.basic_format)
        self.results[word][key] = data

    def crawl_suggest_keywords(self, word, engine, subject=None, save=False) :
        """주어진 단어에 대해 주어진 엔진에서 서제스트 키워드를 수집합니다."""
        if self.verbose : print(f'{word}💬 {engine}에서 suggest keyword 확인')                        
        self.is_selenium_turned_on() # 셀레니움이 켜져있는지 확인        
        self.search(word, engine)  # 주어진 검색어로 검색을 수행합니다.
        self.selenium_click_action(self.tag_selectors.get(f'{engine}_searchinput')) # 클릭
        suggest_keywords =  self.selenium_crawling(self.tag_selectors.get(f'{engine}_suggest_keywords'))   # 내용 스크래핑
        if save : self.add_new_keyword(suggest_keywords, f"{engine}_suggest", subject)  # 수집된 제안 키워드를 저장합니다.
        if self.verbose : print(f'{word}✅ {engine}에서 suggest keyword 확인')  # 디버깅합니다.
        return  suggest_keywords   
    
    def crawl_open_keywords(self, word, engine, subject = None, save=False) :
        """주어진 단어에 대해 지정된 검색 엔진에서 오픈 키워드를 수집합니다.
            word: 검색어
            engine: 사용할 검색 엔진
            save: 수집된 데이터를 저장할지 여부를 결정하는 플래그
            """
        if self.verbose : print(f'{word}💬 {engine}에서 open keyword 확인')                        
        self.is_selenium_turned_on() # 셀레니움이 켜져있는지 확인        
        self.search(word, engine) # 주소이동
        open_keywords =  self.selenium_crawling(self.tag_selectors.get(f'{engine}_open_keywords'))   # 내용 스크래핑
        if save : self.add_new_keyword(open_keywords, f"{engine}_open", subject) # save=True 설정한 경우 수집된 키워드를 저장합니다.
        if self.verbose : print(f'{word}✅ {engine}에서 open keyword 확인') 
        return open_keywords
    
    def count_daum_ads(self, words, save=False) :
        """주어진 단어 또는 단어 리스트에 대해 다음 검색 엔진에서 광고 수를 수집합니다.
        words: 단어 또는 단어의 리스트
        save: 수집된 데이터를 저장할지 여부
        """
        self.is_selenium_turned_on() # 셀레니움이 켜져있는지 확인 
        if type(words) == str : # 단일 단어를 리스트로 변환 (리스트도 인자로 받을 수 있기 위해서!)
            words = [words]
        for word in words :
            time.sleep(1) # 서버에 부하를 주지 않기 위해 각 요청 사이에 휴식 시간을 둡니다.
            self.search(word, 'daum') # 다음 검색 엔진에서 검색을 수행합니다.
            if self.verbose : print(f'{word}💬  다음 광고확인')
            num_advertisement = 0 # 광고 수를 초기화합니다.
            tags = [self.tag_selectors.get('daum_AD_normal'), self.tag_selectors.get('daum_AD_special')] # 광고섹션 태그들을 불러옵니다.
            for tag in tags : 
                try :        
                    ads = self.selenium_crawling(tag)  # 광고 태그에 해당하는 요소를 크롤링합니다.
                    number_of_ads = len(ads)  # 크롤링한 광고의 수를 계산합니다.
                except Exception as e:
                    number_of_ads = 0
                num_advertisement += number_of_ads  # 총 광고 수에 더합니다.
            if self.verbose : print(F'{word}✅ 다음 광고확인 ({num_advertisement})')
            if save : self.save_results(word, 'num_ads', num_advertisement) # 결과를 저장합니다.
        
    
    def get_top_tistory_rank_n_link_at_google(self, words, save=False) :
        """구글 검색 결과에서 주어진 단어에 대해 티스토리 블로그의 순위와 링크를 수집합니다.
        words: 단어 또는 단어의 리스트
        save: 수집된 데이터를 저장할지 여부
        """
        self.is_selenium_turned_on() # 셀레니움이 켜져있는지 확인                      
        if type(words) == str :
            words = [words] # 단일 단어를 리스트로 변환 (리스트도 인자로 받을 수 있기 위해서!)

        for word in words :
            if self.verbose : print(f'{word}💬 구글에서 티스토리 순위 확인')
            time.sleep(1)# 너무 빠른 크롤링은 포털 사이트로부터 의심을 사서 제재를 받을 수 있습니다. 매 크롤링 사이에 1초 쉬어줍니다.
            self.search(word, 'google')
            # 구글 첫번째 화면에 표시되는 링크들을 수집합니다.
            links = self.selenium_crawling(self.tag_selectors.get('google_contents_link'), get_attribute = 'href')
            rank, href, found = 1, '', False  # 티스토리 블로그의 순위, 링크, 발견 여부를 초기화합니다. 순번은 1부터 시작합니다.
            try :            
                for link in links :                    
                    if 'tistory.com' in link : # 수집한 링크에 tistory라는 이름이 포함되어 있는지 확인합니다.
                        href = link
                        found = True # 티스토리가 있으면 현재  순번을 반환합니다.
                        break# 티스토리 블로그 링크가 발견되면 순위를 기록하고 반복을 중단합니다.
                    else :
                        rank += 1 # 티스토리가 없으면 순번을 +1합니다.
                if not found :
                    rank = '노출없음'# 첫번째 화면에 티스토리가 없으면 '노출없음'을 반환합니다.
                    href = '노출없음'
                if self.verbose : print(f'{word}✅ 구글에서 티스토리 순위 확인 ({rank})')
            except Exception as e :
                if self.verbose : print(f'{word}🚫 구글에서 티스토리 순위 확인 :',e)
                rank = '노출없음'# 첫번째 화면에 티스토리가 없으면 '노출없음'을 반환합니다.
                href = '노출없음'
            finally :                
                if save : # 결과를 저장합니다.
                    self.save_results(word, 'tistory_rank_at_google', rank)  # 티스토리 순위를 저장합니다.
                    self.save_results(word, 'top_tistory_at_google', href)  # 티스토리 링크를 저장합니다.
                    self.save_results(word, 'all_links', links)  # 모든 링크를 저장합니다.

        
    
    
    
    

    def iterate_keyword_crawling_w_single_subject(self, depth, words, subject=None, save=True):
        if not save: 
            temp = copy.deepcopy(self.load_results())
            self.results = {}

        assert depth > 0, 'depth must be greater than 0'
        assert len(words) > 0, 'words is required'

        if type(words) == str:
            words = [words]  # 단일 단어를 리스트로 변환

        # 현재까지 수집된 키워드를 초기화합니다.
        processed_keywords = set(copy.deepcopy(self.get_keywords()))
        new_keywords = set(words)  # 시작할 새 키워드들을 설정합니다.

        for current_depth in range(depth):
            print(f'💛 Now  : Subject : ({subject}) Depth ({current_depth}) collected_keywords : ({len(self.get_keywords())})')  # 디버깅용 출력 (현재 depth)
                        

            # 다음 깊이에서 처리할 새 키워드를 저장할 임시 집합
            next_new_keywords = set()

            while new_keywords:
                new_keyword = new_keywords.pop()
                for engine in ['daum', 'google']:
                    try:
                        self.crawl_suggest_keywords(new_keyword, engine, subject, save)
                        self.crawl_open_keywords(new_keyword, engine, subject, save)
                    except Exception as e:
                        print(f'Error occurred while crawling {new_keyword} on {engine}: {e}')
                        continue  # 실패한 키워드는 다시 시도하거나 로깅할 수 있습니다.

                # 다음 깊이에 사용할 새 키워드들을 추가합니다.
                current_keywords = set(self.get_keywords())  # 현재까지 수집된 모든 키워드
                new_discovered_keywords = current_keywords - processed_keywords
                next_new_keywords.update(new_discovered_keywords)
                

                # 광고 수와 티스토리 순위를 수집합니다.
                try:
                    self.count_daum_ads(new_discovered_keywords, save)
                    self.get_top_tistory_rank_n_link_at_google(new_discovered_keywords, save)
                except Exception as e:
                    print(f'Error occurred while collecting info for {new_keyword}: {e}')
                
                processed_keywords.update(new_discovered_keywords)
                

            # 다음 깊이를 위해 새 키워드 세트를 업데이트합니다.
            new_keywords = next_new_keywords
            

        if not save:
            this_result = copy.deepcopy(self.load_results())
            self.results = temp
            return this_result
        

    def iterate_keyword_crawling_w_multiple_subjects(self, depth, subjects_n_words, subject = None, save=True) :
        assert type(subjects_n_words) == dict, 'subjects_n_words must be dictionary (key : subject(str), value : list[words])'
        
        for subject, words in subjects_n_words.items() :
            assert type(words) == list, 'words must be list'
            assert len(words) > 0, 'words is required'
            assert type(subject) == str, 'subject must be string'
            self.iterate_keyword_crawling_w_single_subject(depth, words, subject, save)



    def clean_blog_content(self, text):
        """블로그 컨텐츠를 정제합니다."""
        cleaned_text = '\n'.join(filter(None, text.split('\n'))) # 빈 줄을 제거합니다.
        cleaned_text = '\t'.join(filter(None, cleaned_text.split('\t'))) # 빈 탭을 제거합니다.
        return cleaned_text
    
    def get_naver_blog_contents_from_urls(self, urls, driver):
        """네이버 블로그의 본문을 수집합니다.
        네이버 블로그의 경우 본문 안에 별도의 프레임이 있어서 별도의 처리가 필요합니다.
        """
        body_contents = [] # 네이버 본문을 담을 컨테이너입니다.
        for link in urls:
            try:
                driver.get(link) # 해당 링크로 이동합니다.
                WebDriverWait(driver, 10).until(
                    EC.frame_to_be_available_and_switch_to_it((By.ID, 'mainFrame'))) # 블로그의 본문이 있는 프레임으로 이동합니다.
                body_text = driver.find_element(By.TAG_NAME, 'body').text
                driver.switch_to.default_content() # html 내부의 frame을 벗어나기 위해 사용합니다.
                body_contents.append(body_text) # 본문을 컨테이너에 담습니다.
            except Exception as e:
                continue
        return body_contents
    
    def get_text_from_webpage(self, url, driver=None):
        """웹페이지에서 텍스트를 수집합니다."""
        try:
            response = requests.get(url)
            response.encoding = 'utf-8'

            if response.status_code == 200: # 정상적으로 응답이 왔을 때
                soup = BeautifulSoup(response.text, 'html.parser') # html을 파싱합니다.
                text = soup.get_text() # 텍스트를 수집합니다.
                return text
            elif 'blog.naver' in url: # 네이버 블로그인 경우
                return self.get_naver_blog_contents_from_urls([url], driver)[0] # 네이버 블로그의 본문을 수집합니다.
        except Exception as e:
            if 'blog.naver' in url:
                return self.get_naver_blog_contents_from_urls([url], driver)[0]
        return None

    

    def ddgsearch_reducing(self, keyword, how_many_retrieve=5):
        """웹브라우저 덕덕고로부터 키워드와 관련된 링크를 수집합니다.
        그 다음 해당 링크들로부터 본문을 수집합니다. 수집한 자료는 이후에 RAG에 활용합니다."""
        urls, contents = [], [] # 사이트 주소와 내용을 담을 컨테이너를 준비합니다.
        try:
            results = DDGS().text(keyword, max_results=20) # 덕덕고에서 키워드와 관련된 링크를 수집합니다.
            urls = [a['href'] for a in results if 'html' not in a['href'] and a['href'] != '']
        except Exception as e:
            print(f'{e} with {keyword}')

        
        try:
            idx, clear = 0, 0 # 텍스트 수집에 성공한 갯수를 담을 컨테이너 입니다.
            while clear < how_many_retrieve and idx < len(urls):
                url = urls[idx]
                content = self.get_text_from_webpage(url, self.driver) # 해당 링크로부터 본문을 수집합니다.
                if content:
                    contents.append(self.clean_blog_content(content)) # 수집한 본문을 정제합니다.
                    clear += 1
                idx += 1
        except Exception as e:
            print(e)
        return urls[:how_many_retrieve], contents

    def ddgsearch_get_images(self, word, query_lan = 'en', region = 'wt-wt', license_image='public', max_results = 1,save = False) : 
        """웹브라우저 덕덕고로부터 키워드와 관련된 이미지를 수집합니다."""
        if self.verbose : print(f'{word}💬 이미지수집')
        word = DDGS().translate(keywords= word, to=query_lan)[0]['translated'] # 키워드를 영어로 번역합니다.
        images = DDGS().images(keywords = word, region = region, license_image = license_image) # 이미지를 수집합니다.
        image_container = []
            
        for image in images :
            if 'https' in image['image'] :
                image_container.append(image)
            if len(image_container) == max_results :
                break
        
        if self.verbose : 
            if len(image_container) == max_results :
                print(f'{word}✅ 이미지수집 ({len(image_container)})')
            else :
                print(f'{word}❌ 이미지수집 실패({len(image_container)})')
        
        if save : self.save_results(word, 'images', image_container)

        return image_container
    

