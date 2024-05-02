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
import pandas as pd
from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain.prompts import PromptTemplate
# duckduckgo
from duckduckgo_search import DDGS
import time
# translation
import copy
# formatting
import markdown2

class AIAgent() :
    def __init__(
            self,  
            blogname = None, 
            index = 'my_faiss', 
            parent_path = os.getcwd(),    
            verbose=False) : # 벡터스토어의 이름을 index라고 합니다.        
        self.verbose = verbose # 디버깅
        self.blogname = blogname
        self.vectorstore_index = index # 벡터스토어의 이름을 설정합니다.
        self.root_path = os.path.join(parent_path, blogname)
        self.vectorstore_path = os.path.join(self.root_path, self.vectorstore_index)        
        self.llm = ChatOpenAI(model="gpt-3.5-turbo-0125",) # LLM model (openai 에서 이용가능한 모델 중 가장 저렴한 gpt3.5-turbo모델을 사용합니다.)
        self.embeddings = OpenAIEmbeddings(model='text-embedding-3-small')  # embedding model 또한 openai의 임베딩 모델 중 저렴한 모델을 사용합니다.
        
        try :
            self.load_vectorstore_local() # 로컬에 저장된 벡터스토어를 불러옵니다.
        except Exception as e :
            self.create_vectorstore_local()    # 로컬에 저장된 벡터스토어가 없으면 새롭게 생성합니다.
        self.create_vectorstore_list() # 로컬 벡터스토어 리스트를 생성합니다.
        self.basic_result_form = { # 결과물을 저장할 딕셔너리를 생성합니다.
            'title' : None, 
            'prologue' : None, 
            'keywords' : [], 
            'theme' : None, 
            'topics' : [], 
            'contents' : [], 
            'contents_bef_trans' : [], 
            'images' : [],            
            'documents_urls' : [], 
            'documents' : [],             
            'html_for_upload' : None
        }
        self.results = copy.deepcopy(self.basic_result_form)
    

    
    def create_vectorstore_local(self)  :
        """로컬 벡터스토어를 생성합니다."""
        texts = ["FAISS is an important library"] # 임시로 벡터스토어에 넣을 텍스트를 생성합니다.
        self.vectorstore = FAISS.from_texts(texts, embedding=self.embeddings) # 벡터스토어를 생성합니다.
        self.vectorstore.delete([self.vectorstore.index_to_docstore_id[0]])  # 임시로 넣은 텍스트를 삭제합니다.      
        self.save_local_vectorstore() # 로컬 벡터스토어를 저장합니다.
        if self.verbose : print("✅ 새 벡터스토어 로드되었습니다..") # 디버깅용 메시지를 출력합니다.
    
    def create_vectorstore_list(self) :
        """로컬 벡터스토어 리스트를 생성합니다."""
        try :
            self.vectorstore_list = pd.read_csv(os.path.join(self.root_path, self.vectorstore_index, 'vector_list.csv'), encoding='cp949', index_col=0) # 로컬 벡터스토어 리스트를 불러옵니다.
        except FileNotFoundError :
            self.vectorstore_list = pd.DataFrame(columns = ['data', 'id']) # 파일이 없으면 새로운 데이터프레임을 생성합니다.
            self.save_local_vectorstore_list() # 생성된 데이터프레임을 저장합니다.

    def save_local_vectorstore(self) :
        """로컬 벡터스토어를 저장합니다."""
        self.vectorstore.save_local(folder_path=os.path.join(self.root_path, self.vectorstore_index))
            
    
    def save_local_vectorstore_list(self) :
        """로컬 벡터스토어 리스트를 저장합니다."""
        self.vectorstore_list.to_csv(os.path.join(self.root_path, self.vectorstore_index, 'vector_list.csv'), encoding='cp949', errors='ignore') # 벡터스토어 리스트를 저장합니다.
    
    def load_vectorstore_local(self) :
        """로컬 벡터스토어를 로드합니다. 없으면 새로 생성합니다."""
        self.vectorstore = FAISS.load_local(os.path.join(self.root_path, self.vectorstore_index), self.embeddings, allow_dangerous_deserialization=True) # 벡터스토어를 불러옵니다.
        if self.verbose : print("✅ 기존 벡터스토어 로드되었습니다.")

    
    
    def vectorstore_save_texts(self, data) :
        """벡터스토어에 텍스트를 저장합니다."""
        if type(data) == str :
            data = [data] # 텍스트가 문자열이면 리스트로 변환합니다.

        stored_keywords = self.vectorstore_list['data'].to_list()
        new_keywords = list(set(data) - set(stored_keywords))
        
        ids = self.vectorstore.add_texts(new_keywords) # 벡터스토어에 텍스트를 추가합니다.
        self.vectorstore_list = pd.concat([self.vectorstore_list, pd.DataFrame({'data': new_keywords, 'id' : ids})], ignore_index=True) # 벡터스토어 리스트에 추가합니다.
        self.save_local_vectorstore() # 벡터스토어를 저장합니다.
        self.save_local_vectorstore_list()  # 벡터스토어 리스트를 저장합니다.
        if self.verbose : print("✅ 벡토어스토어 내 새 문서 추가 완료")
        return self.vectorstore_list
        
    def vectorstore_save_documents(self, data) :
        """벡터스토어에 문서를 저장합니다."""
        if type(data) == str :
            data = [data] # 텍스트가 문자열이면 리스트로 변환합니다.
        ids = self.vectorstore.add_documents(data) # 벡터스토어에 문서를 추가합니다.
        # 벡터스토어 리스트에 추가합니다.
        self.vectorstore_list = pd.concat([self.vectorstore_list, pd.DataFrame({'data': [d.page_content for d in data], 'id' : ids})], ignore_index=True) 
        self.save_local_vectorstore()
        self.save_local_vectorstore_list()
        if self.verbose : print("✅ 벡토어스토어 내 새 문서 추가 완료")
        return self.vectorstore_list

    def langchain_RecursiveCharacterTextSplitter(self, documents, chunk_size=300, chunk_overlap=30,model_name = "gpt-3.5-turbo-0125"):
        """문서를 재귀적으로 쪼개어 벡터스토어에 저장합니다."""        
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
                    model_name=model_name, # LLM 모델을 지정합니다.
                    chunk_size=chunk_size, # 청크 사이즈를 지정합니다.
                    chunk_overlap=chunk_overlap, # 청크 오버랩(겹치는 부분의 크기)을 지정합니다.
                )
        if type(documents) == str :
            documents = [documents] 
        splitted = []
        for doc in documents :
            split = text_splitter.split_text(doc) # 문서를 쪼개어 리스트로 저장합니다.
            splitted+=split
        return splitted

    def vectorstore_recursive_save_texts(self, data) :
        """벡터스토어에 텍스트를 재귀적으로 저장합니다. 위에서 정의한 langchain_RecursiveCharacterTextSplitter함수를 이용합니다. """
        splitted = self.langchain_RecursiveCharacterTextSplitter(data)
        return self.vectorstore_save_texts(splitted)
    
    def vectorstore_recursive_save_documents(self, data) :
        """벡터스토어에 문서를 재귀적으로 저장합니다. 위에서 정의한 langchain_RecursiveCharacterTextSplitter함수를 이용합니다."""
        splitted = self.langchain_RecursiveCharacterTextSplitter(data)
        return self.vectorstore_save_documents(splitted)
    
    def vectorstore_delete(self, data):
        """벡터스토어에서 데이터를 삭제합니다."""
        if type(data) == str:
            data = [data]
        for d in data:
            _id = self.vectorstore_list[self.vectorstore_list['data'] == d]['id'].to_list()[0]  # 데이터에 해당하는 id를 찾습니다.
            self.vectorstore.delete(ids=[_id])  # 벡터스토어에서 해당 id를 삭제합니다.
            self.vectorstore_list = self.vectorstore_list[self.vectorstore_list['data'] != d]  # 벡터스토어 리스트에서 해당 데이터를 삭제합니다.
        
        # 인덱스를 0부터 다시 재설정합니다.
        self.vectorstore_list.reset_index(drop=True, inplace=True)
        
        self.save_local_vectorstore()
        self.save_local_vectorstore_list()

    
    def vectorstore_clear(self) :
        """벡터스토어를 초기화합니다."""
        data = self.vectorstore_list['data'].to_list() # 모든 저장된 데이터를 불러옵니다.
        self.vectorstore_delete(data)

    def vectorstore_similarity_search(self, query, score_threshold = 0.55, k=16) :
        """벡터스토어에서 유사도 검색을 수행합니다."""
        retriever = self.vectorstore.as_retriever( # 벡터스토어를 리트리버(LLM이 참고할 수 있는 형태)로 변환합니다.
        search_type="similarity_score_threshold", # 유사도 검색을 수행합니다.
        search_kwargs={"score_threshold": score_threshold, # 유사도 임계값을 설정합니다.
                       "k" : k} # k개의 결과를 반환합니다.
        )
        search_result = [doc.page_content for doc in retriever.invoke(query)] # 검색 결과를 저장합니다.
        return search_result
    


    # 유사도검색 결과 삭제
    def vectorstore_extract(self, query,  score_threshold = 0.55, k=16) :
        """벡터스토어에서 검색 결과를 추출합니다. vectorstore_similarity_search과는 달리 검색한 후에는 벡터스토어 내에서 해당 결과를 삭제합니다."""
        search_result = self.vectorstore_similarity_search(query, score_threshold, k) # 유사도 검색 결과를 불러옵니다.
        self.vectorstore_delete(search_result) # 검색 결과를 삭제합니다.
        return search_result
    
    def suitability_checker(self, subjects, keywords):
        """테마와 키워드의 연관성을 파악하여 yes 또는 no를 반환합니다. 키워드의 적정성을 파악하는데 사용합니다."""
        
        assert len(subjects) == len(keywords), "주제와 키워드의 갯수가 일치하지 않습니다."

        if type(subjects) == str: # 주제가 문자열이면 리스트로 변환합니다.
            subjects = [subjects]
        
        if type(keywords) == str: # 키워드가 문자열이면 리스트로 변환합니다.
            keywords = [keywords]
        
        suitable_keywords = []
        for subject, keyword in zip(subjects, keywords):
            if subject is None : 
                continue
            isSuitable = ''  # 각 키워드에 대해 isSuitable 초기화
            attempts = 0  # 반복 횟수를 세기 위한 카운터
            while isSuitable not in ['yes', 'no'] and attempts < 10 : #LLM으로부터 yes 또는 no 대답이 나올 때까지 반복합니다. 최대 10회 반복합니다.
                attempts += 1  # 카운터 증가                
                isSuitable = self.llm.predict(f'{keyword} 가 {subject}에 관한 블로그에 적합한 토픽인가? 맞으면 "yes" 아니면 "no".')
            
            if isSuitable == 'yes':
                suitable_keywords.append(keyword) # 'yes'라는 대답이 나오면은 적합한 키워드로 추가합니다. 
            
            if self.verbose and isSuitable == 'yes':
                print(f'✅ {keyword} 적정성 : {isSuitable}')
            if self.verbose and isSuitable == 'no':
                print(f'❌ {keyword} 적정성 : {isSuitable}')

        return suitable_keywords
    

    
    def create_topics(self, keywords, num_topic = 3, save=False) :
        """주어진 키워드를 활용하여 주제에 맞는 글감을 생성하여 반환합니다."""
        output_parser = CommaSeparatedListOutputParser()    # 결과를 파싱(읽어들이기)하기 위한 파서를 생성합니다.  comma(,)로 구분된 문자열을 리스트로 변환하여 반환합니다.
        format_instructions = output_parser.get_format_instructions() # 결과를 파싱하는데 사용할 지침을 가져옵니다. 랭체인에서 제공합니다.        
        # 글감생성을 지시하는 프롬프트입니다.
        prompt = PromptTemplate(
            template=f"""
            You are an expert in blog posting. 
            Using the specific keywords provided in their original form, 
            list {num_topic} subtopics in Korean 
            that directly utilize these keywords.
            
            keywords: {keywords}
            {format_instructions}
            """,
            input_variables=["keywords", "subject"],
            partial_variables={"format_instructions": format_instructions},
        )
        # 글감을 생성하는 체인입니다.
        chain = prompt | self.llm | output_parser

        resp_comma = [] # 콤마로 구분된 결과를 저장할 리스트
        resp_line = [] # 줄바꿈으로 구분된 결과를 저장할 리스트 (가끔 줄바꿈으로 구분된 결과가 나오기도 합니다.)
        while len(resp_comma) != num_topic and len(resp_line) != num_topic:
            resp_comma = chain.invoke({"keywords": keywords})
            resp_line = resp_comma[0].split('\n')

            if len(resp_comma) == num_topic : # 콤마로 구분된 결과의 갯수가 num_topic과 같으면 결과를 반환합니다.
                if save : 
                    self.results['keywords'] = keywords
                    self.results['topics'] = resp_comma                
                return resp_comma
            if len(resp_line) == num_topic : #  줄바꿈으로 구분된 결과의 갯수가 num_topic과 같으면 결과를 반환합니다.
                if save : 
                    self.results['keywords'] = keywords
                    self.results['topics'] = resp_comma  
                return resp_line
    
    def create_prologue(self, topics, keywords, save=False):
        """프롤로그를 생성합니다."""
        # 프롤로그를 생성하기 위한 프롬프트입니다.
        prompt = ChatPromptTemplate.from_messages([
            ('system', "You are an SEO expert. Write a suitable **KOREAN** prologue for a blog post. Use the specific topics and keywords provided by the user in their original form directly in the prologue to ensure it is highly relevant and optimized for search engines."),
            ('human', f'Topics: {topics}'),
            ('human', f'Keywords: {keywords}'),            
        ])
        # 프롤로그를 생성하기 위한 체인입니다.
        chain = prompt | self.llm
        prologue = chain.invoke({'topics': topics, 'keywords': keywords}).content
        if save:
            self.results['prologue'] = prologue
        return prologue
    
    def create_title(self, topics, keywords, save=False):
        """제목을 생성합니다."""
        # 제목을 생성하기 위한 프롬프트입니다.
        prompt = ChatPromptTemplate.from_messages([
            ('system', "You are an SEO expert. Create a suitable **KOREAN** blog post title considering the topics and keywords provided by the user. Ensure that the keywords are used in their original form to optimize the title for search engines.The title should be catchy and optimized for search engines."),
            ('human', f'Topics: {topics}'),
            ('human', f'Keywords: {keywords}')
        ])
        # 제목을 생성하기 위한 체인입니다.
        chain = prompt | self.llm
        title = chain.invoke({'topics': topics, 'keywords': keywords}).content
        self.results['title'] = title
        return title

    
    # 번역기
    def recursive_ddgtrans(self, text, from_lang = 'en', to_language='ko', max_chunk_size = 950):
        from translate import Translator
        """덕덕고 웹사이트의 번역기를 사용하여 한글로 번역합니다.
        줄바꿈을 기준으로 텍스트를 분리하여 줄단위로 번역을 수행합니다.
        그렇게 하는 이유는 번역 후에도 원래 글의 형태를 유지하기 위함입니다.
        """
        
        translated_lines = []  # 번역된 줄들을 저장할 리스트               
        lines = text.split('\n') # 줄바꿈을 기준으로 텍스트를 분리

            
        def translator(data, from_lang = 'auto' , to_language = 'ko') :
            from deep_translator import GoogleTranslator

            # def retain_markdown(data) :
            #     markdown = ['# # # #', '# # #', '# #', '* *']
            #     for i in markdown :
            #         data = data.replace(i, i.replace(' ', ''))
            #     return data

            translated = GoogleTranslator(source=from_lang, target=to_language).translate(data)  # output -> Weiter so, du bist großartig
            return translated


        
        for line in lines:
            # 빈 줄인 경우 번역하지 않고 추가
            if not line.strip():
                translated_lines.append(line)
                continue
            
            # 한 줄의 길이가 최대청크크기를 초과하는 경우 줄을 최대 청크 크기에 맞게 나눕니다.
            line_parts = [line[i:i + max_chunk_size] for i in range(0, len(line), max_chunk_size)]
            
            translated_line_parts = []
            for part in line_parts:
                # 각 부분을 번역하고 결과를 리스트에 추가
                # translator = Translator()
                # translated_part = translator.transalte(part, dest=to_language).text # 구글번역개
                # translated_part = DDGS().transalte(part, to=to_language)[0]['translated'] # 덕덕고

                
                tranlation = False
                while not tranlation :
                    try :
                        translated_part = translator(part, from_lang = from_lang, to_language= to_language)
                        tranlation = True
                    except Exception as e :
                        print(e)
                        continue

                translated_line_parts.append(translated_part)
                time.sleep(0.5)  # API 요청 사이에 딜레이 추가
            
            # 번역된 부분들을 합쳐서 전체 번역된 줄을 만듦
            translated_line = '\n'.join(translated_line_parts)
            translated_lines.append(translated_line)
        
        # 번역된 줄들을 원본 텍스트의 줄바꿈 패턴에 맞게 합침
        translated_text = '\n'.join(translated_lines)
        return translated_text

    # 본문내용생성
    def create_content(self, topics, language='English', score_threshold=0.25, k=10, save=False) :
        """ 본문내용을 생성합니다. 내용생성은 영어를 기본값으로 합니다. 내용의 풍성도 측면에서 영어가 훨씬 유리하기 때문입니다.
        만약, 곧바로 한글로 생성하고 싶다면 개별 주제의 내용이 다소 부실해질 수 있기 때문에 소주제를 3개가 아니라 5개 이상으로 늘려야 할 필요가 있습니다.
        관련도가 높더라도 너무 많은 참고자료를 전달하면 모델 성능이 저하되서 10개로 제한합니다.
        """

        # 인터넷에서 서칭한 잘 작성된 글을 예문으로 부여합니다.
        contents_example_1 = """
Healthy Cooking Advice
It’s been proven that meat cooked until its well-done contains more potential carcinogens than meat cooked for a shorter time — laboratory tests have shown that this increase in heterocyclic amines can cause a higher risk of colon tumours and colon polyps. High intakes of well-done meat have also been linked to a greater risk of certain cancers.

Research also suggests that heavy red meat eaters have an increased risk of developing type II diabetes, coronary heart disease, and colorectal cancer — so less than 18 ounces a week is recommended. It’s important to choose steaks that are lower in fat — such as sirloin or beef tenderloin — and cook your steak to minimise the formation of heterocyclic acids.

Keeping portions of steak small will cut down on cooking time — and pre-cooking in the microwave for just two minutes will significantly reduce the acids when cooking. Marinating steaks before cooking with citrus juices, spices, and vinegar may prevent carcinogen formation –and cooking at a lower temperature will also help.

For an inch thick steak try this cooking option: season well with salt and pepper and sear in a hot cast iron pan. Put in the oven pre-heated to 160*C testing with a thermometer until centre of steak reaches 140*C. Take out of the oven and wrap in foil — let it rest at room temperature for at least five minutes. This way the steak will lose only 5% of its moisture and be juicy and pink all the way through.
"""
        # 잘 작성된 글을 예문으로 부여합니다.
        contents_example_2 = """
Grill Times and Temperature for Steak
Rare: 120 to 130 F; 5 then 3 minutes per side; pull off the grill at max 125 F
Medium-Rare: 130 to 135 F; 5 then 4 minutes per side; pull off the grill at max 130 F
Medium: 140 to 150 F; 6 then 4 minutes per side; pull off the grill at max 145 F
Medium-Well: 155 to 165 F; 7 then 5 minutes per side; pull off the grill at max 160 F
Well-Done: 170 F or more; 12 then 10 minutes per side; pull off the grill at max 165 F
How to Use a Meat Thermometer
Since the best way to determine when a steak is done is by checking the internal temperature of the meat, using an instant-read thermometer or grilling thermometer is key. To test for the correct temperature, stick the thermometer probe in the thickest part, away from fat, bone, or gristle. It's important to keep in mind that the meat will continue cooking with residual heat (carry over cooking) even after it's removed from the grill, by about 5 degrees. So if you're going for a final internal temperature of 160 F, remove the steak from the heat at about 155 F, give or take.

Rare steak cut in half on a plate
The Spruce Eats / Diana Chistruga
How to Cook Rare Steak
A steak done rare isn't requested that often; it is for the true carnivore who wants something nearly raw but gets it cooked as little as possible. A rare steak should be warm through the center, lightly charred on the outside, browned around the sides, and bright red in the middle. The meat should be soft to the touch, much like raw meat, but browned over the surface. 

For a 1-inch steak, place steak on​ a hot grill for 5 minutes. Turn and continue grilling for another 3 minutes. Cook to an internal temperature of 120 to 130 F (49 to 55 C).

Steak done medium cut in half on a plate
The Spruce Eats / Diana Chistruga
How to Cook Medium-Rare Steak
This is the recommended level of doneness for a good steak; ask any chef how they like their steak prepared and they will almost all say medium-rare. A medium-rare steak should be warm through the middle with most of the center pink in color with a hint of red. The sides should be well browned, the top and bottom caramelized to a dark brown color with good grill marks. This steak's firm surface should give a bit toward the middle (it will spring back quickly). 

For a 1-inch steak, place steak on a hot grill for 5 minutes. Turn and continue grilling for another 4 minutes to an internal temperature of 130 to 135 F (55 to 57 C).
"""

        

        if type(topics) == str : 
            topics = [topics] # 토픽이 문자열이면 리스트로 변환합니다.
        # 본문을 생성하기 위한 프롬프트입니다.
        prompt = ChatPromptTemplate.from_messages([
        ('system', 
         """context : {context}
            writing_example : {example}
         
         """),
        ('human', """
        
        instruction : 
            You are a fluent writer.
            with below topic and given context, create a long detailed blog post.
            
          
        * Refer to the example provided for a good quality post : 
        * Avoid using the provided context as is.
        * Avoid Closing. 
        * format : Markdown (Using only headers of level three or lower, as the level one and two headers are already prepared. )
        * tone : informative
        * language : {language}
         
        Topic : {topic}"""),
    ])

        


        # 본문을 생성하기 위한 체인입니다.
        chain = prompt | self.llm
        
        for topic in topics :
            context = self.vectorstore_extract(topic, score_threshold = score_threshold, k = k) # 참고자료를 불러옵니다
            contents_bef_trans = chain.invoke({'context' : context, 'language' : language, 'topic' : topic, 'example': contents_example_1 + contents_example_2}).content             
            if save : self.results['contents_bef_trans'].append(contents_bef_trans) # 결과를 저장합니다.

            contents = self.recursive_ddgtrans(contents_bef_trans) # 번역기를 이용하여 한글로 번역합니다.            
            if save : self.results['contents'].append(contents) # 결과를 저장합니다.
        return contents

    def create_HTML_formmater(self, result = None, save=False) :
        # 토픽별 글 합치기
        if result == None : result = self.results # 수집된 정보를 불러옵니다..
        # 여기다가 html text를 통합합니다.
        # 먼저 프롤로그만 포함합니다.    
        html = f"""
        {result['prologue']}
        """

        for idx in range(len(result['topics'])) :
            
            # 토픽별 topic_html을 생성합니다. : 1. 토픽 (소제목)을 더합니다.
            topic_html = f"""
                <h2>{result['topics'][idx]}</h2>                        
            """

            for small_idx in range(len(result['images'][idx])) : # 2. 이미지를 추가합니다. 이미지가 여러 장일 때를 대비하여 반복문으로 구성
                
                """ 이미지를 붙입니다. 이미지에는
                1. 사용자들이 확인하는 이미지 설명
                2. 시각장애인을 위한 대체텍스트 (alt)
                3. 이미지 
                4. 출처
                가 포함되며 이것을 <figure> 태그가 포함하여 중앙정렬을 합니다.
                
                이미지 크기는 현재 400px로  설정되어 있습니다."""

                topic_html += f"""
                    <figure style='align-items: center; text-align : center;'>
                         <img src="{result['images'][idx][small_idx]['image']}" alt="{result['topics'][idx]}" style='width=400px'>
                        <figcaption>
                            {result['topics'][idx]} (출처 : {result['images'][idx][small_idx]['url']})
                        </figcaption>
                    </figure>
                    """
                
                # 3. 본문내용을 추가합니다.
                """ 생성한 토픽별 글을 이어붙입니다. 현재 markdown 형식으로 되어있고 html형식으로 변환합니다. """
                topic_html += f"""
                {markdown2.markdown(result['contents'][idx])}
                """
            # 4. 완성된 토픽별 html 문서를 전체문서에 합칩니다.            
            html+=topic_html
        
        if save : self.results['html_for_upload'] = html
        return html



    def clear(self) :
        self.results = copy.deepcopy(self.basic_result_form)





