from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import time

# 웹 크롤링
headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"}
url = "https://www.melon.com/chart/"

r = requests.get(url, headers = headers)
print(r.raise_for_status)# 연결 상태 확인 // 200>정상 406>헤더 문제 발생

html = r.text
soup = BeautifulSoup(html,"html.parser")

lst_50 = soup.select(".lst50")
lst_100 = soup.select(".lst100")
lst = lst_50 + lst_100 
# lst = soup.select(".lst50,.lst100") 한 번에 
song = []
artist = []

album = []
rank = []

for num,i in enumerate(lst,1):
    
    rank.append(num)
    song.append(i.select_one(".ellipsis.rank01 > span > a").text)
    album.append(i.select_one(".ellipsis.rank03 > a").text)
    
    # 2개이상의 artist 존재함
    artists = []
    for x in i.select(".ellipsis.rank02 > a"):
        artists.append(x.text)
    artist.append(",".join(artists))
    
    
    
# pandas로 데이터 정리
data = {'Ranking':rank, 'Artist' : artist, 'Song':song, 'Album':album}
df = pd.DataFrame(data)
print("complete")

# excel로 내보내기
date = time.strftime('%Y%m%d_%H%M', time.localtime(time.time())) # 날짜_시간 : 20221103_1839
df.to_excel("./MelonTop100_{}.xlsx".format(date), index=False)
