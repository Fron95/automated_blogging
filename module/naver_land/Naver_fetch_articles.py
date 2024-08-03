import pandas as pd
import os
from module.naver_land.Naver_seoul_land import Naver_seoul_land

class Naver_fetch_articles(Naver_seoul_land) :
    def __init__(self) :
        super().__init__()
        self.results = pd.DataFrame()
    # todo : 셀레니움으로 header를 좀 가져와야한다.
    def fetch(self, 
              complexNos = [1147, 119219], 
            #   complexNos = [1147], 
              tradeType = "A1:B1", 
              areaNos = '',
              page = 1, 
              rentPriceMin= 0,
              rentPriceMax= 900000000,
              priceMin= 0,
              priceMax= 900000000,
              areaMin= 0,
              areaMax= 900000000,
              oldBuildYears= "",
              recentlyBuildYears= "",
              minHouseHoldCount= "",
              maxHouseHoldCount= "",
              progressChanged=None,
              resultReady=None) : 
        
        total = len(complexNos)
        trial = 0
        for complexNo in complexNos : 
            progress = int(trial/total)
            progressChanged.emit(progress)
            trial += 1
            # 위치 가져오기
            # apt = self.total_apts[self.total_apts['complexNo'] == complexNo]
            
            # info 가져오기
            info = self.apt_info(
                complexNo = complexNo
            )
            
            # todo : result를 제거해야함
            # 매물 가져오기
            articles = self.apt_items_mult(
                complexNo = complexNo, 
                tradeType = tradeType,
                areaNos = areaNos,
                page = page, 
                rentPriceMin = rentPriceMin,
                rentPriceMax = rentPriceMax,
                priceMin = priceMin,
                priceMax = priceMax,
                areaMin = areaMin,
                areaMax = areaMax,
                oldBuildYears = oldBuildYears,
                recentlyBuildYears = recentlyBuildYears,
                minHouseHoldCount = minHouseHoldCount,
                maxHouseHoldCount = maxHouseHoldCount,)
            articles = pd.DataFrame(articles)
            
            

            # for col in apt.columns :
            #     articles[col] = apt[col].values[0]
            for col in info.columns :
                articles[col] = info[col].values[0]
                

            self.results = pd.concat([self.results, articles])

        return self.results
            
