import datetime
import requests
from bs4 import BeautifulSoup

# 서버로부터 받아야 하는 파라미터
# sid
# webpage
# keyword
def collect_article():

    # 임시 테스트용
    # url = "https://careers.kakao.com/jobs"
    url = "https://recruit.webtoonscorp.com/webtoon/ko/job/list?classNm=developer"
    baseUrl = "https://" + url.split("/")[2]

    #TODO 베이스 URL 접속 후 status 확인 -> 200일 때만 진행

    # 임시 키워드
    keyword = "서버"

    req = requests.get(url)
    html = req.text

    soup = BeautifulSoup(html, 'html.parser')

    # 하이퍼텍스트가 포함된 html 검색
    article_url = soup.select(
        'a'
    )

    # 키워드가 포함된 게시물의 url 리스트
    #TODO 게시물 url status 확인해서 되는 것만 추가
    article_url_list = []

    for a in article_url:
        # 키워드가 존재하는 하이퍼텍스트
        # url에는 키워드 포함 X
        if keyword in str(a) and keyword not in a['href']:
            article_url_list.append(a['href'])

    #TODO Article 테이블에 맞게 csv파일 생성


if __name__ == "__main__":
    print("Start Crawling... :", datetime.datetime.now())

    collect_article()

    print("End Crawling... :", datetime.datetime.now())