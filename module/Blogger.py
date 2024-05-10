# ✅todo : 1. colab 용으로 requirements.txt을 하나 더 만든다.
# ✅ todo : 1. turnonselenium 내용을 colab용으로 추가한다.
# ✅todo : 1. blogger를 모듈화해서 사용하기 쉽게 만든다.
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
from datetime import datetime, timedelta
import copy


class Blogger() :
    def __init__(self, blogname, verbose = False, isHeadless = True) :         
        self.blogname = blogname # 블로그 이름
        self.verbose = verbose # 로그 출력 여부
        """ 반드시 파일매니저부터 호출해야 합니다. 파일매니저 인스턴스 생성과 함께 모든 폴더구조가 생성되기 때문입니다."""
        # 클래스 호출        
        self.file_manager = File_manager(blogname = blogname, verbose=verbose) # 파일 매니저
        self.crawler = Crawler(verbose=verbose, isHeadless=isHeadless) # 크롤러
        self.posting_ai = AIAgent(index="my_contents", blogname=blogname, parent_path=self.file_manager.parent_path, verbose=verbose) # 포스팅 AI
        self.keyword_ai = AIAgent(index = "my_keywords", blogname=blogname, parent_path=self.file_manager.parent_path, verbose=verbose) # 키워드 AI
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
    
    # # 코랩전용 함수
    # def whereami(self) :
    #   path = os.getcwd()
    #   print(path)
    
    # # 코랩전용 함수
    # def save(self, filenames = None) :
    #   from google.colab import drive
    #   import os
    #   import shutil
    #   drive.mount('/content/drive')
    #   # 원본 디렉토리 설정
    #   source_dir = '/content'
    #   # 대상 디렉토리 설정
    #   target_dir = '/content/drive/MyDrive/blogging'
    #   if filenames is None :
    #     filenames = os.listdir(source_dir)
    #   try :
    #     filenames.remove('sample_data')
    #     filenames.remove('drive')
    #     filenames.remove('gdrive')
    #   except :
    #     pass
    #   try :
    #     filenames.remove('.config')
    #   except :
    #     pass
    #   try :
    #     filenames.remove('.git')
    #   except :
    #     pass


    #   # '/content/' 디렉토리의 파일과 폴더 나열
    #   for item in filenames:
    #       print('now : ', item)
    #       source_path = os.path.join(source_dir, item)
    #       target_path = os.path.join(target_dir, item)

    #       # 파일 또는 폴더를 Google 드라이브로 복사
    #       if os.path.isfile(source_path):  # 파일인 경우
    #           if os.path.exists(target_path):  # 대상 경로에 파일이 이미 있으면 덮어쓰기
    #               os.remove(target_path)
    #           shutil.copy(source_path, target_path)
    #       elif os.path.isdir(source_path):  # 디렉토리인 경우
    #           if os.path.exists(target_path):  # 대상 경로에 폴더가 이미 있으면 삭제 후 복사
    #               shutil.rmtree(target_path)
    #           shutil.copytree(source_path, target_path)

    #   print("모든 파일이 Google 드라이브로 복사되었습니다.")
    # # 코랩전용 함수
    # def load(self, filenames = None) :
    #   from google.colab import drive
    #   import os
    #   import shutil
    #   drive.mount('/content/drive')
    #   # 대상 디렉토리 설정 (이제 Colab의 로컬 디렉토리)
    #   target_dir = '/content'
    #   # 원본 디렉토리 설정 (Google 드라이브 내의 백업 폴더)
    #   source_dir = '/content/drive/MyDrive/blogging'


    #   # Google 드라이브의 파일과 폴더 나열
    #   if filenames is None :
    #     filenames = os.listdir(source_dir)
    #   for item in filenames:
    #       print('now : ', item)
    #       source_path = os.path.join(source_dir, item)
    #       target_path = os.path.join(target_dir, item)

    #       # 파일 또는 폴더를 Colab 로컬로 복사
    #       if os.path.isfile(source_path):  # 파일인 경우
    #           if os.path.exists(target_path):  # 대상 경로에 파일이 이미 있으면 덮어쓰기
    #               os.remove(target_path)
    #           shutil.copy(source_path, target_path)
    #       elif os.path.isdir(source_path):  # 디렉토리인 경우
    #           if os.path.exists(target_path):  # 대상 경로에 폴더가 이미 있으면 삭제 후 복사
    #               shutil.rmtree(target_path)
    #           shutil.copytree(source_path, target_path)

    #       print("모든 파일이 Google 드라이브에서 복원되었습니다.")
        


    def collect_keywords(self, subjects_n_words, depth, save=True, collected_keywords_save = True, screened_keywords_save = True, suitable_keywords_save = True, vectorstore_save=True) :
        self.crawler.is_selenium_turned_on() # 셀레니움이 켜져있는지 확인합니다.
        try :
            # 키워드 수집에는 crawler 클래스 내에서 미리 정의되어 있는 반복문을 사용합니다.
            # self.crawler.iterate_keyword_crawling_w_multiple_subjects(depth = depth, subjects_n_words=subjects_n_words, save=save) 
            assert type(subjects_n_words) == dict, 'subjects_n_words must be dictionary (key : subject(str), value : list[words])'        
            for subject, words in subjects_n_words.items() :
                assert type(words) == list, 'words must be list'
                assert len(words) > 0, 'words is required'
                assert type(subject) == str, 'subject must be string'
                self.crawler.iterate_keyword_crawling_w_single_subject(depth, words, subject, save)

                if collected_keywords_save : self.file_manager.save_keywords('collected_keywords', self.crawler.results) # 수집한 전체키워드 정보 저장
                if screened_keywords_save : self.file_manager.save_keywords('screened_keywords',  self.crawler.results ) # 선별한 키워드 정보 저장

        except Exception as e :
            print(e)
        finally : # 중단하더라도 현재진행시점까지가 로컬에 저장됩니다.
            
            # 수집한 전체키워드 정보 중에서 정보가 수집되지 않은 키워드는 제외하고 저장한다.
            # 그런데 이 기능은 여기에 들어갈 것이 아니라 기본적인 Cralwer의 iteration 함수에 들어가야 한다.
            self.crawler.results =  self.crawler.load_results().dropna(
                subset = ['num_ads', 'tistory_rank_at_google']).T.to_dict() 
            print('after interuption : good')

            # collected_keywords
            if collected_keywords_save :
                collected_keywords_info = self.crawler.load_results() # 수집한 전체키워드 정보
                collected_keywords = self.crawler.get_keywords() # 수집한 전체키워드 리스트
                self.file_manager.save_keywords('collected_keywords', self.crawler.results) # 수집한 전체키워드 정보 저장
                print('after interuption : collected_keywords = good')


            # 키워드 선별
            if screened_keywords_save :
                screened_keywords_info = self.crawler.load_processed_results() # 선별한 키워드 정보
                screened_keywords = list(screened_keywords_info.index) # 선별한 키워드 리스트
                self.file_manager.save_keywords('screened_keywords',  self.crawler.results ) # 선별한 키워드 정보 저장
                print('after interuption : screened_keywords = good')

            # 키워드 적정성 검사
            if suitable_keywords_save :                
                subjects = screened_keywords_info.loc[:,'subject'].to_list() # 키워드 적정성 검사를 위한 주제 리스트            
                suitable_keywords = []

                # for screened_word, subject in zip(screened_keywords, subjects) :
                #     self.crawler.
                #     suitable_keywords += self.keyword_ai.suitability_checker(subjects, screened_keywords)


                suitable_keywords = self.keyword_ai.suitability_checker(subjects, screened_keywords) # 적정성 검사
                suitable_keywords_info = screened_keywords_info.loc[suitable_keywords] # 적정성 검사 결과
                # 수집한 전체 키워드 로컬환경에 csv파일로 저장            
                self.file_manager.save_keywords('suitable_keywords', suitable_keywords_info.T.to_dict() ) # 적정한 키워드 정보 저장
                print('after interuption : suitable_keywords = good')
                
            # # 클래스 내부 변수로 저장
            # self.collected_keywords_info = collected_keywords_info # 수집한 전체키워드 정보
            # self.collected_keywords = collected_keywords # 수집한 전체키워드 리스트
            # self.screened_keywords_info = screened_keywords_info # 선별한 키워드 정보
            # self.screened_keywords = screened_keywords# 선별한 키워드 리스트
            # self.suitable_keywords_info = suitable_keywords_info # 적정한 키워드 정보
            # self.suitable_keywords = suitable_keywords # 적정한 키워드 리스트
            # print('after interuption : good4')
            
            
            # 키워드 벡터스토어 저장 (keyword_ai)            
            if vectorstore_save :
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
            if self.verbose : print(f"🌐 글을 작성할 키워드를 가지고 오는 중... ")
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
                if self.verbose : print(f"🌐 글 관련 자료 수집 중 ... ")
                for topic in self.posting_ai.results['topics'] :
                    hrefs, documents = self.crawler.ddgsearch_reducing(topic)    
                    # documents, hrefs = self.crawler.ddgsearch_reducing(topic)    
                    self.posting_ai.results['documents_urls'].append(hrefs)
                    self.posting_ai.results['documents'].append(documents)

                # 긁어들인 글들을 벡터스토어에 저장하기                
                collected_documents = []
                for document in self.posting_ai.results['documents'] :
                    collected_documents.extend(document)
                self.posting_ai.vectorstore_recursive_save_texts(collected_documents)


                

                # 글 작성
                if self.verbose : print(f"🌐 글 작성 중 ... ")
                self.posting_ai.create_content(
                    topics = self.posting_ai.results['topics'], 
                    language=contents_lan, 
                    score_threshold=documents_score_threshold,  
                    k=documents_retriever_k,  
                    save=True)

                # 이미지 수집하기    
                if self.verbose : print(f"🌐 이미지 수집 중 ... ")
                topics = self.posting_ai.results['topics']
                for topic in topics : 
                    images = self.crawler.ddgsearch_get_images(topic, max_results = num_images)
                    self.posting_ai.results['images'].append(images)    

                # 글 포맷팅하기
                if self.verbose : print(f"🌐 글 형식화 중 ... ")
                self.posting_ai.create_HTML_formmater(save=True)

                # 결과저장하기
                if self.verbose : print(f"🌐 글 저장 중 ... ")
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
                self.posting_ai.vectorstore_clear()
            except Exception as e :
                print(e)
                continue
            finally :
                if num_contents_creation is not None :
                    if iteration >= num_contents_creation :
                        break

    def upload_contents(self, num_contents_upload = 15, uploading_day = (datetime.now() + timedelta(days=1)).day, uploading_start_hour = 2, uploading_minute_term =  120) :

        assert len(os.getenv(f'{self.blogname}_ID')) > 0, '블로그 아이디를 환경변수에 등록하세요.'
        assert len(os.getenv(f'{self.blogname}_PW')) > 0, '블로그 비밀번호를 환경변수에 등록하세요.'
        assert len(os.getenv(f'{self.blogname}_NEW_POST_URL')) > 0, '블로그 포스팅URL를 환경변수에 등록하세요.'

        print(f"""
            🌐🌐🌐🌐🌐🌐🌐🌐🌐🌐🌐🌐🌐🌐🌐🌐🌐🌐🌐
            uploading_day : {uploading_day}
            uploading_start_hour : {uploading_start_hour}
            uploading_minute_term : {uploading_minute_term}
            🌐🌐🌐🌐🌐🌐🌐🌐🌐🌐🌐🌐🌐🌐🌐🌐🌐🌐🌐
            """
        )


        self.uploader.is_selenium_turned_on() # 셀레니움이 켜져있는지 확인합니다.
        # 업로드 할 문서를 불러옵니다.
        filenames = self.file_manager.get_file_names() # 전체 파일 목록을 불러옵니다.

        upload_titles = [] # 업로드할 문서의 제목 컨테이너
        upload_contents = [] # 업로드할 문서의 내용 컨테이너
        
        for filename in filenames[:num_contents_upload] :
            # 파일명에서 제목 추출 (파일제목에 오류가 있을 경우 순서를 건너뜁니다.)
            try :              
              _, _, title, _ = self.file_manager.extract_elements_from_filename(filename) 
            except Exception as e :
              continue
            
            text = self.file_manager.loadText2Text_w_filename(filename, 'for_upload') # 파일 내용 불러오기

            upload_titles.append(title) # 컨테이너에 제목 추가
            upload_contents.append(text)   # 컨테이너에 내용 추가
            self.file_manager.moveComplete(filename) # 제목과 내용 추출이 완료된 완료된 파일은 이동합니다.

        if self.verbose : print(f"업로드 할 문서의 갯수는 {len(upload_contents)}개 입니다.")
        
        try :
            self.uploader.tistory_upload(
                titles = upload_titles, # 업로드할 전체 제목 목록
                contents = upload_contents, # 업로드할 전체 내용 목록
                uploading_day  = uploading_day,
                uploading_start_hour = uploading_start_hour, # 업로드 시작 시간 (기본값 2시)
                uploading_minute_term = uploading_minute_term)  # 업로드 간격 (기본값 120분)
        finally :
            self.uploader.driver.quit() # 리소스 절약을 위한 드라이버 종료