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
import os
import copy
import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime, timedelta
from module.Crawler import Crawler

# css selectors
format_selector = "#editor-mode-layer-btn-open"
html_format_option = "#editor-mode-html"
title_input = "#post-title-inp"
content = "#html-editor-container > div.mce-edit-area > div > div > div.CodeMirror-scroll > div.CodeMirror-sizer > div > div > div > div.CodeMirror-code > div > pre > span"
kakao_login = "#cMain > div > div > div > a.btn_login.link_kakao_id > span.txt_login"
kakao_id = "#loginId--1"
kakao_pw = "#password--2"
idpw_submit_button = "#mainContent > div > div > form > div.confirm_btn > button.btn_g.highlight.submit"
submit_button = '#publish-layer-btn'
public_radio_button = "#open20"
publish_date_on = "dd > button:nth-child(2)"
finish_button = "#publish-btn"
next_month_button = "#editor-root > div:nth-child(42) > div > div > div > form > fieldset > div.layer_body > div > dl:nth-child(4) > dd > div > div.layer_info > div > div > div.info_date > button.btn_arr.btn_next"
hour_css = "#dateHour"
minute_css = "#dateMinute"
date_buttons = "button.btn_day"
calender_button = "button.btn_reserve"


def require_env(var_name):
    value = os.getenv(var_name)
    if value is None:
        raise ValueError(f"환경변수 {var_name}가 설정되어 있지 않습니다.")
    return value

# config
class Uploader(Crawler) :
    def __init__(
        self,
        blogname,         
        id = None,
        password= None,
        new_post_url= None,        
        verbose=False,
        isHeadless=True
        ) :

        super().__init__(verbose, isHeadless)
        self.blogname = blogname
        self.id = id if id is not None else os.getenv(f"{blogname}_ID")
        self.pw = password if password is not None else os.getenv(f"{blogname}_PW")
        self.new_post_url = new_post_url if new_post_url is not None else os.getenv(f"{blogname}_NEW_POST_URL")

        
        
        
    

    def generate_times(self, start_day, start_hour, minute_term, count):
        # 시작 시간 설정, 연도와 월은 여전히 임의로 설정
        start_time = datetime(2023, 1, start_day, start_hour, 0)
        times = []
        
        for _ in range(count):
            # 현재 시간을 (일, 시, 분) 형태로 변환하여 리스트에 추가
            times.append((start_time.day, start_time.hour, start_time.minute))
            # 다음 시간 계산
            start_time += timedelta(minutes=minute_term)

        return times



    # def selenium_send(self, tag_css_selector, content) :
    #     self.is_selenium_turned_on()        
    #     time.sleep(1) # 잠시 대기 (동적 콘텐츠 로딩을 위함)
    #     WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, tag_css_selector)))
    #     target = self.driver.find_element(By.CSS_SELECTOR, tag_css_selector)
    #     self.driver.execute_script("arguments[0].style.display='block';", target)
    #     target.send_keys(content)

    # def selenium_typing(self, tag_css_selector, content) :
    #     self.is_selenium_turned_on()     
    #     WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, tag_css_selector)))
    #     self.selenium_click_action(tag_css_selector)
    #     actions = ActionChains(self.driver)
    #     actions.send_keys(content)
    #     actions.perform()
    
    # def selenium_alert_handling(self, handling='dismiss') :
    #     assert handling in ['accept', 'dismiss'], "handling은 'accept' 또는 'dismiss' 중 하나여야 합니다."
    #     self.is_selenium_turned_on()        
    #     try : # 
    #         alert = self.driver.switch_to.alert             
    #         alert.dismiss() if handling == 'dismiss' else alert.accept()
    #     except Exception as e:
    #         if self.verbose : print('at alert', e)
    #         pass
        


    def tistory_selectDay(self, day) :        
        self.selenium_click_action(calender_button)

        if day == 1 :
            self.selenium_click_action(next_month_button) # 업로드날짜가 다음달인 경우에 활성화
        
        buttons = self.driver.find_elements(By.CSS_SELECTOR, date_buttons)
        for button in buttons:
            if button.text.strip() == str(day):
                button.click()
                break

    def tistory_selectTime(self, hour, minute) :

        hour_input = self.driver.find_elements(By.CSS_SELECTOR, hour_css)[0]  
        minute_input = self.driver.find_elements(By.CSS_SELECTOR, minute_css)[0]  

        hour_input.send_keys(Keys.END)
        hour_input.send_keys(Keys.BACK_SPACE)
        hour_input.send_keys(Keys.BACK_SPACE)

        minute_input.send_keys(Keys.END)
        minute_input.send_keys(Keys.BACK_SPACE)
        minute_input.send_keys(Keys.BACK_SPACE)

        self.selenium_send(hour_css, hour)
        self.selenium_send(minute_css, minute)
    

        
    def tistory_upload(
            self, 
            titles, 
            contents, 
            uploading_day = (datetime.now() + timedelta(days=1)).day, 
            uploading_start_hour = 2, 
            uploading_minute_term = 120) : 
    
        assert len(titles) == len(contents), "등록된 제목의 갯수와 글의 갯수가 불일치합니다."

        num_uploading = len(titles)
        uploading_dates = self.generate_times(uploading_day, uploading_start_hour, uploading_minute_term, num_uploading)
        
        # 업로드 시작
        self.is_selenium_turned_on()  # selenium이 켜져있는지 확인        
        if self.verbose : print('💠페이지 접속')
        self.driver.get(self.new_post_url) # 새 글 작성 페이지로 이동
        # 1. 로그인
        if self.verbose : print('💠카카오로그인 페이지 접속')
        self.selenium_click_action(kakao_login) # 카카오 로그인 버튼 클릭
        if self.verbose : print('💠 아이디입력')
        self.selenium_send(kakao_id, self.id) # 아이디 입력
        if self.verbose : print('💠 비밀번호 입력')
        self.selenium_send(kakao_pw, self.pw) # 비밀번호 입력
        if self.verbose : print('💠 로그인 버튼 클릭')
        self.selenium_click_action(idpw_submit_button) # 로그인 버튼 클릭
        time.sleep(2) # 로그인 대기
        self.selenium_alert_handling('dismiss') # 알림창 닫기
        time.sleep(1)
        self.selenium_alert_handling('dismiss') # 알림창 닫기        
        # 2. 포스팅 
        for idx in range(num_uploading) :

            title = titles[idx]
            html_text = contents[idx]
            uploading_day = uploading_dates[idx][0]
            uploading_hour = uploading_dates[idx][1]
            uploading_minute = uploading_dates[idx][2]

            try :
                self.driver.get(self.new_post_url) # 새 글 작성 페이지로 이동                    
                time.sleep(2) # 페이지 로딩 대기
                self.selenium_alert_handling('dismiss') # 알림창 닫기        
                time.sleep(1)
                self.selenium_alert_handling('dismiss') # 알림창 닫기        
                time.sleep(1)
                if self.verbose : print('💠 html 편집기 전환')
                self.selenium_click_action(format_selector) # html selector 클릭                    
                time.sleep(0.5)
                self.selenium_click_action(html_format_option) # html option 클릭
                self.selenium_alert_handling('accept') # 알림창 닫기        
                time.sleep(0.5)
                if self.verbose : print('💠 제목입력창 선택')
                self.selenium_send(title_input, title) # 제목창 선택 및 입력                    
                time.sleep(0.5)
                if self.verbose : print('💠 내용입력 창 선택')
                self.selenium_click_action(content) # 텍스트 창 선택 및 입력
                self.selenium_typing(content, html_text) # 텍스트 창 선택 및 입력
                # self.selenium_typing(content, "html_text")
                time.sleep(0.5)
                if self.verbose : print('💠 완료버튼 선택')
                self.selenium_click_action(submit_button) # 완료 버튼        
                time.sleep(0.5)
                self.selenium_click_action(public_radio_button) # 공개 버튼
                time.sleep(0.5)
                self.selenium_click_action(publish_date_on) # 예약 버튼
                time.sleep(0.5)                
                self.tistory_selectDay(uploading_day) # 날짜 선택
                time.sleep(0.5)
                self.tistory_selectTime(uploading_hour, uploading_minute) # 시간 선택
                if self.verbose : print('💠 최종제출')
                time.sleep(0.5) # 최종 제출
                self.selenium_click_action(finish_button)
                if self.verbose : print("글생성완료",title)                    
            except Exception as e:
                print(e)

