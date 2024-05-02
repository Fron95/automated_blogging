# ✅todo : 1. colab 용으로 requirements.txt을 하나 더 만든다.
# ✅ todo : 1. turnonselenium 내용을 colab용으로 추가한다.
# todo : 1. blogger를 모듈화해서 사용하기 쉽게 만든다.
# ✅todo : 1. 쓰레딩 시키는 것도 함수화한다.
# ✅todo : 1. 코랩은 쓰레딩 몇개를 시키는게 적당한지를 확인한다 = 2개 (2코어라서)
# ✅todo : 1. 코랩크롤링 시에, user-agent 사용하도록 한다.
# duckduckgo 대체품 찾기



import os
# 정의한 클래스들을 호출합니다.
from module.Crawler import Crawler
from module.AIAgent import AIAgent
from module.File_manager import File_manager
from module.Uploader import Uploader
import copy

class Blogger() :
    def __init__(self, blogname, verbose = False, isHeadless = True) :         
        self.blogname = blogname # 블로그 이름
        self.verbose = verbose # 로그 출력 여부
        """ 반드시 파일매니저부터 호출해야 합니다. 파일매니저 인스턴스 생성과 함께 모든 폴더구조가 생성되기 때문입니다."""
        # 클래스 호출        
        self.file_manager = File_manager(blogname = blogname, verbose=verbose) # 파일 매니저
        self.crawler = Crawler(verbose=verbose, isHeadless=isHeadless) # 크롤러
        self.posting_ai = AIAgent(index="my_contents", blogname=blogname  ,verbose=verbose) # 포스팅 AI
        self.keyword_ai = AIAgent(index = "my_keywords", blogname=blogname, verbose=verbose) # 키워드 AI
        self.uploader = Uploader(
            blogname=blogname, # 아이디와 비밀번호, 포스팅URL을 지정하지 않으면 환경변수에서 가져옵니다.        
            verbose=verbose,
            isHeadless = isHeadless
            )
        
        # 기존에 수집하여서 저장해두었던 키워드들이 있으면은 불러와서 crawler.results에 저장합니다.
        # 그렇게 함으로써 키워드를 수집하는 과정에서 중복되는 키워드를 제거할 수 있을 뿐만 아니라 새롭게 수집된 키워드가 기존 키워드에 덮어씌워지지 않도록 합니다.

        collected_keywords_info = self.file_manager.get_keywords(what_keywords='collected_keywords') # 수집한 전체키워드 정보            
        if collected_keywords_info is not None : # 수집한 전체키워드 정보가 있으면
            self.crawler.results = copy.deepcopy(collected_keywords_info.T.to_dict()) # 수집한 전체키워드 정보를 crawler.results에 저장합니다.
        else :            
            print('해당 블로그는 수집한 키워드 정보가 없습니다.')        
        
        # self.collected_keywords_info = self.file_manager.get_keywords(what_keywords='collected_keywords')
        # self.collected_keywords = self.collected_keywords_info.keys().to_list()
        # self.screened_keywords_info = self.file_manager.get_keywords(what_keywords='collected_keywords')
        # self.screened_keywords = self.screened_keywords_info.keys().to_list()
        # self.suitable_keywords_info = self.file_manager.get_keywords(what_keywords='collected_keywords')
        # self.suitable_keywords = self.suitable_keywords_info.keys().to_list()

        


    def collect_keywords(self, subjects_n_words, depth, save=True) :
        self.crawler.is_selenium_turned_on() # 셀레니움이 켜져있는지 확인합니다.
        try :
            # 키워드 수집에는 crawler 클래스 내에서 미리 정의되어 있는 반복문을 사용합니다.
            self.crawler.iterate_keyword_crawling_w_multiple_subjects(depth = depth, subjects_n_words=subjects_n_words, save=save) 
        except Exception as e :
            print(e)
        finally : # 중단하더라도 현재진행시점까지가 로컬에 저장됩니다.
            
            # 수집한 전체키워드 정보 중에서 정보가 수집되지 않은 키워드는 제외하고 저장한다.
            # 그런데 이 기능은 여기에 들어갈 것이 아니라 기본적인 Cralwer의 iteration 함수에 들어가야 한다.
            self.crawler.results =  self.crawler.load_results().dropna(
                subset = ['num_ads', 'tistory_rank_at_google']).T.to_dict() 
            print('after interuption : good')

            # collected_keywords
            collected_keywords_info = self.crawler.load_results() # 수집한 전체키워드 정보
            collected_keywords = self.crawler.get_keywords() # 수집한 전체키워드 리스트
            self.file_manager.save_keywords('collected_keywords', self.crawler.results) # 수집한 전체키워드 정보 저장
            print('after interuption : collected_keywords = good')


            # 키워드 선별
            screened_keywords_info = self.crawler.load_processed_results() # 선별한 키워드 정보
            screened_keywords = list(screened_keywords_info.index) # 선별한 키워드 리스트
            self.file_manager.save_keywords('screened_keywords',  self.crawler.results ) # 선별한 키워드 정보 저장
            print('after interuption : screened_keywords = good')

            # 키워드 적정성 검사
            subjects = screened_keywords_info.loc[:,'subject'].to_list() # 키워드 적정성 검사를 위한 주제 리스트            
            suitable_keywords = self.keyword_ai.suitability_checker(subjects, screened_keywords) # 적정성 검사
            suitable_keywords_info = screened_keywords_info.loc[suitable_keywords] # 적정성 검사 결과
            print('after interuption : good3')
            
            # 클래스 내부 변수로 저장
            self.collected_keywords_info = collected_keywords_info # 수집한 전체키워드 정보
            self.collected_keywords = collected_keywords # 수집한 전체키워드 리스트
            self.screened_keywords_info = screened_keywords_info # 선별한 키워드 정보
            self.screened_keywords = screened_keywords# 선별한 키워드 리스트
            self.suitable_keywords_info = suitable_keywords_info # 적정한 키워드 정보
            self.suitable_keywords = suitable_keywords # 적정한 키워드 리스트
            print('after interuption : good4')
            
            # 수집한 전체 키워드 로컬환경에 csv파일로 저장            
            
            self.file_manager.save_keywords('suitable_keywords', suitable_keywords_info.T.to_dict() ) # 적정한 키워드 정보 저장
            
            
            # 키워드 벡터스토어 저장 (keyword_ai)            
            self.keyword_ai.vectorstore_save_texts(suitable_keywords)

    def create_contents(self, 
                        num_contents_creation = None, 
                        keyword_score_threshold=0.55,
                        kewyord_retriever_k = 16,
                        num_topic = 3,
                        contents_lan = 'English',
                        num_images = 1,
                        documents_score_threshold=0.25,
                        documents_retriever_k = 10) :        

        iteration = 0 # 반복횟수
        # 무한반복 (반복횟수 미지정 시 벡터스토어 내에 키워드가 남지 않을 때까지 무한반복한다. 반복횟수 지정 시 해당 횟수만큼 반복하고 종료한다.)
        while True : 
            iteration += 1 # 반복횟수 1증가
            random_keywords = self.keyword_ai.vectorstore.similarity_search('')
            if len(random_keywords) == 0 : # 벡터스토어 내에 키워드가 남지 않으면 종료
                print('🟡 벡터스토어 내에 저장된 모든 키워드를 소진하였습니다. 고생하셨습니다.')
                break
            try : 
                my_keyword = self.keyword_ai.vectorstore.similarity_search('')[0].page_content # 글을 쓸 첫번째 키워드를 가져옵니다.    
                my_keywords = self.keyword_ai.vectorstore_extract(
                    my_keyword, 
                    score_threshold=keyword_score_threshold,
                    k = kewyord_retriever_k
                    )     # 관련 키워드 추출 및 벡터스토어 내에서 삭제 (extract)
            
            
            
            
            
                self.posting_ai.create_topics(my_keywords, num_topic=num_topic, save=True)     # 소제목 3개 생성
                self.posting_ai.create_prologue(self.posting_ai.results['topics'], self.posting_ai.results['keywords'], save=True)     # 프롤로그 생성
                self.posting_ai.create_title(self.posting_ai.results['topics'], self.posting_ai.results['keywords'], save=True)     # 제목 생성
                # 자료수집
                for topic in self.posting_ai.results['topics'] :
                    documents, hrefs = self.crawler.ddgsearch_reducing(topic)    
                    self.posting_ai.results['documents_urls'].append(documents)
                    self.posting_ai.results['documents'].append(hrefs)

                # 긁어들인 글들을 벡터스토어에 저장하기
                collected_documents = []
                for document in self.posting_ai.results['documents'] :
                    collected_documents.extend(document)
                self.posting_ai.vectorstore_recursive_save_texts(collected_documents)


                

                # 글 작성
                self.posting_ai.create_content(
                    topics = self.posting_ai.results['topics'], 
                    language=contents_lan, 
                    score_threshold=documents_score_threshold,  
                    k=documents_retriever_k,  
                    save=True)

                # 이미지 수집하기    
                topics = self.posting_ai.results['topics']
                for topic in topics : 
                    images = self.crawler.ddgsearch_get_images(topic, max_results = num_images)
                    self.posting_ai.results['images'].append(images)    

                # 글 포맷팅하기
                self.posting_ai.create_HTML_formmater(save=True)

                # 결과저장하기

                # 수집 및 생성한 모든 자료를 json으로 저장합니다.
                self.file_manager.saveGeneratedDict2Json(
                    data = self.posting_ai.results,
                    subject = self.blogname,
                    language = 'ko',
                    contents = self.posting_ai.results['title'],
                    folder_category='storage'
                )
                # 포스팅할 문서를 txt로 저장합니다.
                self.file_manager.saveGeneratedText2Text(
                    data = self.posting_ai.results['html_for_upload'],
                    subject = self.blogname,
                    language = 'ko',
                    contents = self.posting_ai.results['title'],
                    folder_category='for_upload'
            )
                # 저장 후 self.posting_ai의 results 초기화.
                self.posting_ai.clear()
            except Exception as e :
                print(e)
                continue
            finally :
                if num_contents_creation is not None :
                    if iteration >= num_contents_creation :
                        break


    def upload_contents(self, num_contents_upload = 15) :

        assert len(os.getenv(f'{self.blogname}_ID')) > 0, '블로그 아이디를 환경변수에 등록하세요.'
        assert len(os.getenv(f'{self.blogname}_PW')) > 0, '블로그 비밀번호를 환경변수에 등록하세요.'
        assert len(os.getenv(f'{self.blogname}_NEW_POST_URL')) > 0, '블로그 포스팅URL를 환경변수에 등록하세요.'

        self.uploader.is_selenium_turned_on() # 셀레니움이 켜져있는지 확인합니다.
        # 업로드 할 문서를 불러옵니다.
        filenames = self.file_manager.get_file_names() # 전체 파일 목록을 불러옵니다.

        upload_titles = [] # 업로드할 문서의 제목 컨테이너
        upload_contents = [] # 업로드할 문서의 내용 컨테이너
        
        for filename in filenames[:num_contents_upload] :
            _, _, title, _ = self.file_manager.extract_elements_from_filename(filename) # 파일명에서 제목 추출
            text = self.file_manager.loadText2Text_w_filename(filename, 'for_upload') # 파일 내용 불러오기

            upload_titles.append(title) # 컨테이너에 제목 추가
            upload_contents.append(text)   # 컨테이너에 내용 추가
            self.file_manager.moveComplete(filename) # 제목과 내용 추출이 완료된 완료된 파일은 이동합니다.

        if self.verbose : print(f"업로드 할 문서의 갯수는 {len(upload_contents)}개 입니다.")
        
        try :
            self.uploader.tistory_upload(
                titles = upload_titles, # 업로드할 전체 제목 목록
                contents = upload_contents, # 업로드할 전체 내용 목록
                # uploading_day 미 지정 시 내일 날짜 기준으로 업로드 ,
                uploading_start_hour = 2, # 업로드 시작 시간 (기본값 2시)
                uploading_minute_term = 120)  # 업로드 간격 (기본값 120분)
        finally :
            self.uploader.driver.quit() # 리소스 절약을 위한 드라이버 종료
            # 경고를 무시합니다.
import warnings
warnings.filterwarnings("ignore")

# 환경변수 저장 (.env) 확인
from dotenv import load_dotenv
import os


load_dotenv() 



# blogger 클래스를 호출합니다.
from module.Blogger import Blogger

# 기본적인 환경설정을 합니다.
isHeadless = True
verbose = True

# blogname = input('블로그 이름을 입력하세요 ')
print('💛')
statifi = Blogger(blogname = 'statifi', verbose = verbose, isHeadless = isHeadless)
print('💛')
kindmom = Blogger(blogname = 'kindmom', verbose = verbose, isHeadless = isHeadless)
print('💛')
sweetkiwi = Blogger(blogname = 'sweetkiwi', verbose = verbose, isHeadless = isHeadless)
print('💛')
takuz = Blogger(blogname = 'takuz', verbose = verbose, isHeadless = isHeadless)
print('💛')
morningbbobbo = Blogger(blogname = 'morningbbobbo', verbose = verbose, isHeadless = isHeadless)

bloggers ={
    "statifi" :statifi,
    "kindmom" :kindmom,
    "sweetkiwi" :sweetkiwi,
    "takuz" :takuz,
    "morningbbobbo" :morningbbobbo,
}



recommended = {
    "건강과 웰빙": ["요가", "마인드풀니스", "웰니스 리트릿", "건강한 간식", "명상", "필라테스", "건강한 식단", "건강 추세", "힐링", "건강 검진"],
    "기업과 기업가": ["기업가 정신", "크라우드펀딩", "비즈니스 모델 혁신", "기술 벤처", "벤처 투자", "스타트업 생태계"],
    "재택 근무 및 자기 계발 블로그": ["재택 근무 팁", "자기계발 책 추천", "온라인 학습 플랫폼", "시간 관리 기술", "생산성 향상", "사이드 허슬", "재택 근무 환경", "프리랜서 가이드", "자기 관리", "모티베이션 증진"],
    "건강 및 웰니스 블로그": ["건강한 식단", "정신 건강", "스트레스 관리", "홈 피트니스", "명상 기법", "웰니스 라이프스타일", "영양 정보", "건강 검진 가이드", "체중 관리", "건강한 습관"],
    
}



# 가정 관리 및 DIY 프로젝트 블로그
subjects_n_words_for_statifi = {"가정 관리 및 DIY 프로젝트 블로그": ["홈 데코 아이디어", "자동차 관리", "정원 가꾸기", "DIY 프로젝트", "가정 유지보수", "가구 제작", "집안 정리 팁", "에너지 효율 가이드", "안전한 집 만들기", "유아 교육 활동"] }
# 음식 요리 
subjects_n_words_for_kindmom = {"음식과 요리": ['미쉐린', '미슐랭', '블루리본', '100년가게', "베지테리언 레시피", "음식 트렌드", "음식 시장", "로컬 식당 탐방", "디톡스 요리", "수퍼푸드", "향토 음식", "음식 블로그", "쿠킹 클래스", "푸드 투어"], }
# 여행
subjects_n_words_for_sweetkiwi = {"디지털 노마드와 여행 블로그": ["디지털 노마드 팁", "글로벌 여행 가이드", "작업 효율성", "여행용 앱", "여행 예산 관리", "비자 가이드", "여행자 보험", "작업 공간 찾기", "문화 적응 팁", "소셜 미디어 마케팅"],  }
# 인공지능, 
subjects_n_words_for_takuz = {"인공지능": ["인공지능 응용", "머신 러닝", "데이터 분석", "딥 러닝 알고리즘", "핀테크", "에코테크", "소프트웨어 개발", "테크 리뷰"]}
# 웰니스
subjects_n_words_for_morningbbobbo = {"지속 가능한 생활 블로그": ["제로 웨이스트 팁", "지속 가능한 제품", "친환경 생활", "에코 라이프스타일", "환경 보호", "플라스틱 프리", "재사용 가능 제품", "친환경 홈 메이크오버", "지속 가능한 패션", "에너지 절약 팁"], }



depth = 3
save = True


import threading

def collect_keywords_for_blogger(blogger, subjects_n_words, depth, save):
    print(f"Collecting keywords for {blogger.blogname}...")
    blogger.collect_keywords(subjects_n_words=subjects_n_words, depth=depth, save=save)
    print(f"Finished collecting keywords for {blogger.blogname}.")

# 각 블로거의 주제 및 키워드 데이터
bloggers = {
    'statifi': statifi,
    'kindmom': kindmom,
    'sweetkiwi': sweetkiwi,
    'takuz': takuz,
    'morningbbobbo': morningbbobbo
}

subjects_n_words = {
    'statifi': subjects_n_words_for_statifi,
    'kindmom': subjects_n_words_for_kindmom,
    'sweetkiwi': subjects_n_words_for_sweetkiwi,
    'takuz': subjects_n_words_for_takuz,
    'morningbbobbo': subjects_n_words_for_morningbbobbo
}

# 스레드 목록 생성
threads = []

# 각 블로거에 대해 스레드 생성 및 실행
for blogger_name, blogger in bloggers.items():
    thread = threading.Thread(target=collect_keywords_for_blogger, args=(blogger, subjects_n_words[blogger_name], depth, save))
    threads.append(thread)
    thread.start()

# 모든 스레드의 완료를 기다림
for thread in threads:
    thread.join()

print("All keyword collection tasks completed.")
