""" 
[저장해야 하는 것]

[저장] 1. collected 키워드 - csv
[저장] 2. screened 키워드 - csv
[저장] 3. 컨텐츠 생성 dict - json
[저장] 4. 컨텐츠 생성 dict - csv
[저장] 5. 컨텐츠 - texts
[옮기기] 6. 업로드 완료 컨텐츠 옮기기
[읽어들이기] 7. txt, csv, json

폴더구조

업로드할것
창고
업로드완료
"""

import pandas as pd
import os
import shutil
import json
import re
class File_manager() :
    def __init__(self, 
    blogname,
    parent_path = os.path.join(os.getcwd(), 'bloggers'),    
    verbose = False) :        
        self.verbose = verbose
        self.blogname = blogname
        self.parent_path = parent_path
        self.root_path = os.path.join(parent_path, blogname)        
        self.makeFolder(self.root_path)
        self.result_folder_path = os.path.join(self.root_path,'for_upload') # 결과물을 저장할 폴더 경로 설정
        self.uploaded_folder_path = os.path.join(self.root_path,'uploaded') # 업로드 완료된 파일을 저장할 폴더 경로 설정
        self.storage_folder_path = os.path.join(self.root_path,'storage')  # 창고 폴더 경로 설정
        self.verbose = verbose
        self.makeFolder(self.result_folder_path) # 루트폴더에 업로드할것 폴더 생성
        self.makeFolder(self.uploaded_folder_path) # 루트폴더에 업로드완료 폴더 생성
        self.makeFolder(self.storage_folder_path) # 루트폴더에 창고 폴더 생성

    def makeFolder(self, result_folder_path) :        
        try :
            os.makedirs(result_folder_path)
            self.result_folder_path = result_folder_path
        except FileExistsError:
            if self.verbose : print('기존에 생성된 폴더가 존재합니다.')
        except Exception as e:
            if self.verbose : print(e)
        return result_folder_path


    def embedding_dict_for_same_length(self, data) :
        # 가장 긴 리스트의 길이를 찾음
        max_length = max(len(lst) for lst in data.values())

        # 모든 리스트를 동일한 최대 길이로 맞춤
        for key in data:
            current_length = len(data[key])
            # 부족한 길이만큼 None (또는 다른 플레이스홀더 값)을 추가
            data[key].extend([None] * (max_length - current_length))
        
        return data
    
    # Windows에서 파일 이름에 사용할 수 없는 문자를 제거하거나 대체
    def sanitize_filename(self, filename):
        # Windows에서 파일 이름에 사용할 수 없는 문자를 제거하거나 대체
        invalid_chars = r'[<>:"/\\|?*]'  # Windows에서 금지된 문자들
        safe_filename = re.sub(invalid_chars, '', filename)  # 금지된 문자들을 언더스코어로 대체
        return safe_filename

    def createSavingFilePath(self, subject, language, contents, format, folder_category) :
        if (folder_category != 'storage') and (folder_category != 'uploaded') and (folder_category != 'for_upload') :
            print("we have folder category : storage, uploaded, for_upload"  )

        file_name = self.createFileName(subject=subject, language=language, contents=contents, format=format)

        # 폴더를 정합니다. -> 경로를 반환합니다.
        if folder_category == 'storage' : return os.path.join(self.storage_folder_path, file_name)
        if folder_category == 'uploaded' : return os.path.join(self.uploaded_folder_path, file_name)
        if folder_category == 'for_upload' : return os.path.join(self.result_folder_path, file_name)

    def createFileName(self, subject, language, contents, format) :
        subject = subject.lower() # 소문자 처리합니다.
        language = language.lower() # 소문자 처리합니다.
        contents = contents.lower() # 소문자 처리합니다.
        format = format.lower() # 소문자 처리합니다.
        return self.sanitize_filename(f"[[{subject}]]_(({language}))_``{contents}``.{format}")
    
    

    # dict -> json
    def saveGeneratedDict2Json(self, data, subject, language, contents, folder_category, transpose = False) :
        if type(data) != dict :
            raise ValueError('data type should be dict')
        pathnfilename = self.createSavingFilePath(subject, language, contents, 'json', folder_category)  
        if transpose : data = pd.DataFrame(data).T.to_dict()      

        with open(pathnfilename, 'w', errors='ignore') as json_file:
            json.dump(data, json_file)
        if self.verbose : print(f'contents saved as JSON : ', pathnfilename)

    # dict -> csv
    def saveGeneratedDict2CSV(self, data, subject, language, contents, folder_category, transpose = True) :
        if type(data) != dict :
            raise ValueError('data type should be dict')
        pathnfilename = self.createSavingFilePath(subject, language, contents, 'csv', folder_category)
        # 보기 좋도록 돌려서 저장한다.
        if transpose : data = pd.DataFrame(data).T.to_dict()      
        
        pd.DataFrame(data).to_csv(pathnfilename, encoding='cp949', errors='ignore')
        if self.verbose : print(f'dict contents saved as csv : ', pathnfilename)

    # text -> text
    def saveGeneratedText2Text(self, data, subject, language, contents, folder_category) :
        pathnfilename = self.createSavingFilePath(subject, language, contents, 'txt', folder_category)
        # 파일을 열고, cp949 인코딩을 사용하여 data를 저장
        with open(pathnfilename, 'w', encoding='cp949', errors='ignore') as file:
            file.write(data)
        if self.verbose : print(f'Data successfully saved to {pathnfilename}')

    def get_file_names(self, folder = 'for_upload' ) :
        # 각 폴더의 모든 파일이름을 가져옵니다.
        if folder == 'for_upload' :
            return os.listdir(self.result_folder_path)
        elif folder == 'uploaded' :
            return os.listdir(self.uploaded_folder_path)
        elif folder == 'storage' :
            return os.listdir(self.storage_folder_path)

    def extract_elements_from_filename(self, filename):
        # 파일 이름에서 정보를 추출합니다.
        pattern = r"\[\[(.*?)\]\]_\(\((.*?)\)\)_``(.*?)``\.(.*)"
        match = re.match(pattern, filename)
        if match:
            elements = {
                "subject": match.group(1),
                "language": match.group(2),
                "contents": match.group(3),
                "format": match.group(4)
            }
            return elements["subject"],elements["language"],elements["contents"],elements["format"],
        else :
            assert False, "파일 이름 확인 요망"


    # JSON 파일 읽기
    def loadJson2Dict_w_filename(self, filename, folder_category, to_pandas_DataFrame = False, transpose = False) :
        """JSON 파일을 읽어서 판다스 데이터프레임으로 반환합니다."""        
        subject, language, contents, _format = self.extract_elements_from_filename(filename)
        pathnfilename = self.createSavingFilePath(subject, language, contents, 'json', folder_category)

        print(to_pandas_DataFrame)
        print(transpose)

        try:
            with open(pathnfilename, 'r', errors='ignore') as json_file:
                data = json.load(json_file)
            if self.verbose: print(f'Data loaded from JSON')

            if to_pandas_DataFrame and transpose : return pd.DataFrame(data).T
            elif to_pandas_DataFrame and not transpose: return pd.DataFrame(data)
            elif not to_pandas_DataFrame and transpose: return pd.DataFrame(data).T.to_dict()          
            elif not to_pandas_DataFrame and not transpose: return data
            
        except Exception as e:
            print(e)

    # CSV 파일 읽기
    def loadCSV2DataFrame_w_filename(self, filename, folder_category, index_col= 0, to_pandas_DataFrame = True, transpose = False) :
        """CSV 파일을 읽어서 판다스데이터프레임으로 반환합니다."""
        subject, language, contents, _format = self.extract_elements_from_filename(filename)
        pathnfilename = self.createSavingFilePath(subject, language, contents, 'csv', folder_category)
        try:
            data = pd.read_csv(pathnfilename, encoding='cp949', index_col= index_col)
            if self.verbose: print(f'Data loaded from CSV:{pathnfilename}')

            if to_pandas_DataFrame and transpose : return pd.DataFrame(data).T
            if to_pandas_DataFrame and not transpose: return pd.DataFrame(data)
            if not to_pandas_DataFrame and transpose: return pd.DataFrame(data).T.to_dict()          
            if not to_pandas_DataFrame and not transpose: return pd.DataFrame(data).to_dict()          
        except Exception as e:
            print(e)

    # 텍스트 파일 읽기
    def loadText2Text_w_filename(self, filename, folder_category) :
        """텍스트 파일을 읽어서 텍스트로 반환합니다."""
        subject, language, contents, _format = self.extract_elements_from_filename(filename)
        pathnfilename = self.createSavingFilePath(subject, language, contents, 'txt', folder_category)
        try:
            with open(pathnfilename, 'r', encoding='cp949', errors='ignore') as file:
                data = file.read()
            if self.verbose: print(f'Data loaded from text file:')
            return data
        except Exception as e:
            print(e)


    # JSON 파일 읽기
    def loadJson2Dict(self, subject, language, contents, folder_category, to_pandas_DataFrame = False, transpose = False) :
        """JSON 파일을 읽어서 판다스 데이터프레임으로 반환합니다."""                
        pathnfilename = self.createSavingFilePath(subject, language, contents, 'json', folder_category)
        print(to_pandas_DataFrame)
        print(transpose)
        

        try:
            with open(pathnfilename, 'r', errors='ignore') as json_file:
                data = json.load(json_file)
            if self.verbose: print(f'Data loaded from JSON')
            if to_pandas_DataFrame and transpose : return pd.DataFrame(data).T 
            if to_pandas_DataFrame and not transpose: return pd.DataFrame(data)
            if not to_pandas_DataFrame and transpose: return pd.DataFrame(data).T.to_dict()          
            if not to_pandas_DataFrame and not transpose: return data
        except Exception as e:
            print(e)

    # CSV 파일 읽기
    def loadCSV2DataFrame(self, subject, language, contents, folder_category, index_col= 0, to_pandas_DataFrame = True, transpose = False) :
        """CSV 파일을 읽어서 판다스데이터프레임으로 반환합니다."""
        pathnfilename = self.createSavingFilePath(subject, language, contents, 'csv', folder_category)
        try:
            data = pd.read_csv(pathnfilename, encoding='cp949', index_col= index_col)
            if self.verbose: print(f'Data loaded from CSV:')
            if to_pandas_DataFrame and transpose : return data.T
            if to_pandas_DataFrame and not transpose: return data
            if not to_pandas_DataFrame and transpose: return data.T.to_dict()          
            if not to_pandas_DataFrame and not transpose: return data.to_dict()          
        except Exception as e:
            print(e)

    # 텍스트 파일 읽기
    def loadText2Text(self, subject, language, contents, folder_category) :
        """텍스트 파일을 읽어서 텍스트로 반환합니다."""
        pathnfilename = self.createSavingFilePath(subject, language, contents, 'txt', folder_category)
        try:
            with open(pathnfilename, 'r', encoding='cp949', errors='ignore') as file:
                data = file.read()
            if self.verbose: print(f'Data loaded from text file:')
            return data
        except Exception as e:
            print(e)

    def save_keywords(self, what_keywords, data) : 
        assert type(data) == dict, 'data type should be dict'

        if what_keywords == 'collected_keywords' :            
            self.saveGeneratedDict2CSV(data, self.blogname, 'ko', 'collected_keywords', 'storage')            
            self.saveGeneratedDict2Json(data, self.blogname, 'ko', 'collected_keywords', 'storage')            
            if self.verbose : print(f"{self.blogname} : collected_keywords saved")
        if what_keywords == 'screened_keywords' :
            self.saveGeneratedDict2CSV(data, self.blogname, 'ko', 'screened_keywords', 'storage')            
            self.saveGeneratedDict2Json(data, self.blogname, 'ko', 'screened_keywords', 'storage')            
            if self.verbose : print(f"{self.blogname} : screened_keywords saved")
        if what_keywords == 'suitable_keywords' :
            self.saveGeneratedDict2CSV(data, self.blogname, 'ko', 'suitable_keywords', 'storage')            
            self.saveGeneratedDict2Json(data, self.blogname, 'ko', 'suitable_keywords', 'storage')            
            if self.verbose : print(f"{self.blogname} : suitable_keywords saved")

    # 키워드 파일 손쉽게 가져오기
    def get_keywords(self, what_keywords, to_pandas_DataFrame = True) :
        if what_keywords == 'collected_keywords' :
            try:
                return self.loadJson2Dict(self.blogname, 'ko', 'collected_keywords', 'storage', to_pandas_DataFrame=to_pandas_DataFrame, transpose=to_pandas_DataFrame)
            except Exception as e :
                print('collected_keywords 파일이 없습니다.')
                print(e)
            
        if what_keywords == 'screened_keywords' :
            try:
                return self.loadJson2Dict(self.blogname, 'ko', 'screened_keywords', 'storage', to_pandas_DataFrame=to_pandas_DataFrame, transpose=to_pandas_DataFrame)
            except Exception as e :
                print('screened_keywords 파일이 없습니다.')
                print(e)
        if what_keywords == 'suitable_keywords' :
            try :
                return  self.loadJson2Dict(self.blogname, 'ko', 'suitable_keywords', 'storage', to_pandas_DataFrame=to_pandas_DataFrame, transpose=to_pandas_DataFrame)
            except Exception as e :
                print('suitable_keywords 파일이 없습니다.')
                print(e)
        

    def moveComplete(self, file_name) :
        # 파일 경로 설정
        original_path = os.path.join(self.result_folder_path, file_name)  # 여기에 파일의 현재 경로 입력
        destination_path = os.path.join(self.uploaded_folder_path, file_name)  # 파일을 옮기고 싶은 폴더 경로 입력

        # 파일을 새로운 위치로 이동
        shutil.move(original_path, destination_path)
    



        
    
    

    
    