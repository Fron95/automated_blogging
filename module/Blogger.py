import os
# 정의한 클래스들을 호출합니다.
from module.Crawler import Crawler
from module.AIAgent import AIAgent
from module.File_manager import File_manager
from module.Uploader import Uploader
import copy

class Blogger() :
    def __init__(self, blogname, verbose = False) :         
        self.blogname = blogname # 블로그 이름
        self.verbose = verbose # 로그 출력 여부
        """ 반드시 파일매니저부터 호출해야 합니다. 파일매니저 인스턴스 생성과 함께 모든 폴더구조가 생성되기 때문입니다."""
        # 클래스 호출        
        self.file_manager = File_manager(blogname = blogname, verbose=verbose) # 파일 매니저
        self.crawler = Crawler(verbose=verbose) # 크롤러
        self.posting_ai = AIAgent(index="my_contents", blogname=blogname  ,verbose=verbose) # 포스팅 AI
        self.keyword_ai = AIAgent(index = "my_keywords", blogname=blogname, verbose=verbose) # 키워드 AI
        self.uploader = Uploader(
            blogname=blogname, # 아이디와 비밀번호, 포스팅URL을 지정하지 않으면 환경변수에서 가져옵니다.        
            verbose=verbose)
        
        # 기존에 수집하여서 저장해두었던 키워드들이 있으면은 불러와서 crawler.results에 저장합니다.
        # 그렇게 함으로써 키워드를 수집하는 과정에서 중복되는 키워드를 제거할 수 있을 뿐만 아니라 새롭게 수집된 키워드가 기존 키워드에 덮어씌워지지 않도록 합니다.
        collected_keywords_info = self.file_manager.get_keywords(what_keywords='collected_keywords') # 수집한 전체키워드 정보
        self.crawler.results = copy.deepcopy(collected_keywords_info) # 수집한 전체키워드 정보를 crawler.results에 저장합니다.



    def collect_keywords(self, subjects_n_words, depth, save=True) :
        self.crawler.is_selenium_turned_on() # 셀레니움이 켜져있는지 확인합니다.
        try :
            # 키워드 수집에는 crawler 클래스 내에서 미리 정의되어 있는 반복문을 사용합니다.
            self.crawler.iterate_keyword_crawling_w_multiple_subjects(depth = depth, subjects_n_words=subjects_n_words, save=save) 
        finally : # 중단하더라도 현재진행시점까지가 로컬에 저장됩니다.
            # 결과물
            collected_keywords_info = self.crawler.load_results() # 수집한 전체키워드 정보
            collected_keywords = self.crawler.get_keywords() # 수집한 전체키워드 리스트
            screened_keywords_info = self.crawler.load_processed_results() # 선별한 키워드 정보
            screened_keywords = list(screened_keywords_info.index) # 선별한 키워드 리스트
            
            # 키워드 적정성 검사
            subjects = screened_keywords_info.loc[:,'subject'].to_list() # 키워드 적정성 검사를 위한 주제 리스트
            
            suitable_keywords = self.keyword_ai.suitability_checker(subjects, screened_keywords) # 적정성 검사
            suitable_keywords_info = screened_keywords_info.loc[suitable_keywords] # 적정성 검사 결과
            
            # 클래스 내부 변수로 저장
            self.collected_keywords_info = collected_keywords_info # 수집한 전체키워드 정보
            self.collected_keywords = collected_keywords # 수집한 전체키워드 리스트
            self.screened_keywords_info = screened_keywords_info # 선별한 키워드 정보
            self.screened_keywords = screened_keywords# 선별한 키워드 리스트
            self.suitable_keywords_info = suitable_keywords_info # 적정한 키워드 정보
            self.suitable_keywords = suitable_keywords # 적정한 키워드 리스트
            
            # 수집한 전체 키워드 로컬환경에 csv파일로 저장
            self.file_manager.save_keywords('collected_keywords', collected_keywords_info.to_dict() ) # 수집한 전체키워드 정보 저장
            self.file_manager.save_keywords('screened_keywords', screened_keywords_info.to_dict() ) # 선별한 키워드 정보 저장
            self.file_manager.save_keywords('suitable_keywords', suitable_keywords_info.to_dict() ) # 적정한 키워드 정보 저장
            
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
                break
            try : 
                my_keyword = self.keyword_ai.vectorstore.similarity_search('')[0].page_content # 글을 쓸 첫번째 키워드를 가져옵니다.    
                my_keywords = self.keyword_ai.vectorstore_extract(
                    my_keyword, 
                    score_threshold=keyword_score_threshold,
                    k = kewyord_retriever_k
                    )     # 관련 키워드 추출 및 벡터스토어 내에서 삭제 (extract)

                self.posting_ai.create_subject('파스타', my_keywords, num_topic=num_topic, save=True)     # 소제목 3개 생성
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
                if (iteration != None) and (iteration >= num_contents_creation) :
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