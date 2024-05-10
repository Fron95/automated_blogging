import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions
import copy

from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
# pypi packages
import os
# langchain
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.embeddings import CacheBackedEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda
from langchain_text_splitters import RecursiveCharacterTextSplitter
# info
# import pandas as pd
from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain.prompts import PromptTemplate
# duckduckgo
from duckduckgo_search import DDGS
import time
# translation
import copy
# formatting
import markdown2

from module.Crawler import Crawler
class Marketer(Crawler) :
    def __init__(self, isHeadless=False, verbose=True) -> None:
        super().__init__(isHeadless = isHeadless, verbose = verbose)
        self.basic_format = {
            'link' :  None,           
            'review' : [],
        }
        self.result = copy.deepcopy(self.basic_format)

        self.llm = ChatOpenAI(model="gpt-3.5-turbo-0125",) # LLM model (openai 에서 이용가능한 모델 중 가장 저렴한 gpt3.5-turbo모델을 사용합니다.)
        self.embeddings = OpenAIEmbeddings(model='text-embedding-3-small')  # embedding model 또한 openai의 임베딩 모델 중 저렴한 모델을 사용합니다.



    # def timelimit(self, seconds, func) :
    #     start = time.time()
        

    #     end = time.time()
    #     if end - start > seconds :
    #         return False
    #     return True
    
    def wait_until_element_loaded(self, CSS_SELECTOR, duration=10):
        ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)
        elements = WebDriverWait(self.driver, duration, ignored_exceptions=ignored_exceptions) \
            .until(expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, CSS_SELECTOR)))
        return elements
    
    def show_interaction_with_scroll(self, func, max_attempts=10, **kwargs):
        attempts = 0
        while attempts < max_attempts:
            attempts += 1 
            try:
                func(**kwargs)
                break
            except:
                self.selenium_scroll_action('down')
                attempts += 1

    def set_timelimit(self, func, timeout = 30, **kwargs):
        start_time = time.time()
        while time.time() - start_time < timeout:
            func(**kwargs)
            break




    def naver_smartstore_review_crawling(self, link, max_page = 10, max_attempts=10) :
        """네이버스마트스토어 상품페이지에서 리뷰를 크롤링해옵니다."""
        naver_selector_review_cat = "#content > div > div.z7cS6-TO7X > div._27jmWaPaKy > ul > li:nth-child(2)"
        naver_selector_next_page = "a.fAUKm1ewwo._2Ar8-aEUTq._nlog_click"
        selector_review ="li.BnwL_cs1av._nlog_click._nlog_impression_element"
        naver_selector_comment = 'span._2L3vDiadT9'
        naver_selector_score = 'em._15NU42F3kT'
        naver_selector_product = "div._2FXNMst_ak"
        
        # 링크저장
        self.result['link'] = link

        self.driver.get(link)
        # 리뷰 페이지 이동 버튼
        # self.show_interaction_with_scroll(func=self.selenium_click_action, max_attempts=max_attempts, CSS_SELECTOR=naver_selector_review_cat)

        # 리뷰 크롤링
        _continue = True
        page = 1

        while _continue and page < max_page :
            

            elements = []
            attempts = 0
            while attempts < max_attempts and len(elements) == 0 :                
                attempts += 1 
                time.sleep(1)
                try :
                    self.selenium_scroll_action('down' , 2)
                    elements = self.wait_until_element_loaded(naver_selector_comment, duration=2)
                    elements = self.wait_until_element_loaded(naver_selector_score, duration=2)
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector_review) 
                    
                except :
                    continue
            assert len(elements) != 0, f"{page}번째 페이지에서 리뷰추출을 실패하였습니다."

            for element in elements :
                try :                
                    product = element.find_elements(By.CSS_SELECTOR, naver_selector_product)
                    comment = element.find_elements(By.CSS_SELECTOR, naver_selector_comment)
                    score = element.find_elements(By.CSS_SELECTOR, naver_selector_score)
                    # 저장
                    review = (product[0].text, comment[0].text, comment[1].text, score[0].text)
                    self.result['review'].append(review)
                except :
                    continue
            

            # 다음 페이지로 
            print(f'{page} 페이지 크롤링 완료')
            page += 1

            if page == max_page :
                return self.result

            
            attempts = 0
            while attempts < max_attempts:
                attempts += 1 
                try :
                    self.selenium_click_action(naver_selector_next_page)                    
                    break
                except :
                    self.selenium_scroll_action('down', 4)
                    self.selenium_scroll_action('up', 3)           
                    if attempts >= max_attempts : 
                        print(f"{page} 페이지에서 중단.")
                        return self.result['review']

    def ohouse_review_crawling(self, link, max_page = 10, max_attempts=10) :


        ohouse_review_article_selector = "article.production-review-item"
        ohouse_score_selector = "span.production-review-item__writer__info__total-star"
        ohouse_comment_selector = "p.production-review-item__description"
        ohouse_product_selector = "p.production-review-item__name__explain__text.hidden-overflow"
        ohouse_date_selector = "span.production-review-item__writer__info__date"
        ohouse_next_page_selector = "ul._2BEHX.production-review__paginator button._2XI47._3I7ex"

        
        self.driver.get(link)
        self.result['link'] = link

        _continue = True
        page = 1
        
        while _continue :

            print(f"🅾{page}페이지 크롤링 중")


            def get_ohouse_score() :
                scores = self.selenium_crawling(ohouse_score_selector, get_attribute='aria-label')
                scores =[float(score.replace('별점 ', '').replace('점', '')) for score in scores]
                return scores
            
            elements = []
            attempts = 0
            while attempts < max_attempts and len(elements) == 0 :                
                attempts += 1 
                time.sleep(1)
                try :
                    self.selenium_scroll_action('down' , 2)
                    elements = self.wait_until_element_loaded(ohouse_review_article_selector, duration=2)                
                    if attempts == max_attempts :
                        assert False, "리뷰 크롤링 실패"
                except :
                    continue
            
            for element in elements :
                try :                
                    product = element.find_element(By.CSS_SELECTOR, ohouse_product_selector).text
                    comment = element.find_element(By.CSS_SELECTOR, ohouse_comment_selector).text
                    score_element = element.find_element(By.CSS_SELECTOR, ohouse_score_selector)
                    score = float(score_element.get_attribute('aria-label').replace('별점 ', '').replace('점', ''))
                    date = element.find_element(By.CSS_SELECTOR, ohouse_date_selector).text
                    
                    # 저장
                    review = (product, date, score, comment)                
                    self.result['review'].append(review)
                except :
                    continue
        
            print(f'✅{page} 페이지 크롤링 완료')        

            # 할당 페이지 수 충족 시 그만
            if page >= max_page + 1 :
                return self.result['review']
            
            # 할당 페이지 수 미충족 시 다음 페이지로
            page += 1
            attempts = 0
            while attempts < max_attempts:
                attempts += 1 
                try :
                    self.selenium_click_action(ohouse_next_page_selector)                    
                    break
                except :
                    self.selenium_scroll_action('down', 4)
                    self.selenium_scroll_action('up', 3)           
                    if attempts >= max_attempts : 
                        print(f"{page} 페이지에서 중단.")
                        return self.result['review']
            

    def ai_product_details(self, product, reviews=None) -> str  :
        
        messages = [
            ('human', """As a digital marketing expert, please provide a comprehensive breakdown
of the key benefits and features in separate lists of {product}. Explain
how these features address customer pain points and what makes this
product stand out from competitors. Additionally, highlight any
testimonials, awards, or certifications associated with the product that
can be leveraged to enhance credibility and trust among potential
customers.
""")
        ]

        if reviews is not None :
            messages.append(('system', f"""reviews about product : 
                             {reviews}"""))
        prompt = ChatPromptTemplate.from_messages(messages)
       
        chain = prompt | self.llm
        response = chain.invoke({'product': product}).content
        return response
    
    def ai_create_persona(self, product, reviews) -> str  :
        messages = [
            ('human', """Act as an expert digital marketer. Please provide a comprehensive target
audience persona for a digital marketer selling {product}. Include the
following information: Demographics, Geographic location,
Psychographics, Professional Background, Pain Points and challenges,
Goals and aspirations, Shopping habits and preferences, Media
consumption, Influencers and decision-makers, Brand perceptions and
preferences. Assume no prior audience data is available, and base the
persona on general market trends and consumer behavior for this type of
product. At the end, give me suggestions for different niches to target to
best sell this product.
""")
        ]
        if reviews is not None :
            messages.append(('system', f"""reviews about product : 
                             {reviews}"""))
        prompt = ChatPromptTemplate.from_messages(messages)
        chain = prompt | self.llm
        response = chain.invoke({'product': product}).content
        return response
    
    def ai_update_persona_w_niche(self, niche, persona, reviews = None)  -> str :
        messages = [
            ('human', """Update the following target audience persona and aim it towards {niche}.
{persona}
""")
        ]
        if reviews is not None :
            messages.append(('system', f"""reviews about product : 
                             {reviews}"""))
        prompt = ChatPromptTemplate.from_messages(messages)
        chain = prompt | self.llm
        response = chain.invoke({'niche': niche, 'persona' : persona}).content
        return response

    def ai_summarize_pros_cons_of_competitos(self, reviews) -> str :
        prompt = ChatPromptTemplate.from_messages([
            ('human', """Summarize the following reviews into lists of pros and cons. At the end
give me suggestions on how I may improve based on this feedback.
{reviews}
""")
        ])
        chain = prompt | self.llm
        response = chain.invoke({'riviews': reviews}).content
        return response
    

    def ai_create_marketing_strategy_from_pros_cons(self, pros_cons) -> str :
        prompt = ChatPromptTemplate.from_messages([
            ('human', """Act as a digital marketing expert. Summarize the following list into
constructive feedback that I can use for a digital marketing strategy.
{pros_cons}
""")
        ])
        chain = prompt | self.llm
        response = chain.invoke({'pros_cons': pros_cons}).content
        return response
    
    def chunknizer(self, texts, max_character_length = 3000) :

        if type(texts) == 'str' :
            texts = [texts]

        result = []        
        chunk = ''
        for text in texts :
            chunk += text
            if len(chunk) >= max_character_length :
                result.append(chunk)
                chunk = ''