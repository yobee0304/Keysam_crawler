import datetime
import requests
import os
from pandas import DataFrame
from bs4 import BeautifulSoup

def collect_article():

    # API 1번 호출
    response = requests.get('http://localhost:8080/spGetWebpage')
    result_dict = {'sid':[], 'url':[]}

    for json_data in response.json():
        # API 호출을 통해 받은 파라미터 값들
        sid = json_data["sid"]
        keyword = json_data["keyword"]
        url = json_data["webpage"]
        classid = json_data["classid"]

        baseUrl = "https://" + url.split("/")[2]

        req = requests.get(url)
        html = req.text

        soup = BeautifulSoup(html, 'html.parser')

        # 하이퍼텍스트가 포함된 html 검색
        article_url = soup.select(
            'div.' + classid + ' > a'
        )

        # 키워드가 포함된 게시물의 url 리스트
        article_url_list = []

        for a in article_url:
            # 키워드가 존재하는 하이퍼텍스트
            # url에는 키워드 포함 X
            # if keyword in str(a) and keyword not in a['href']:

            # For test
            if keyword in str(a):
                article_url_list.append(a['href'])

        #TODO 게시불 게시된 시간 있으면 가져오기
        for url in article_url_list:
            result_dict["sid"].append(sid)
            result_dict["url"].append(baseUrl+url)

    # Article 테이블에 맞게 csv파일 생성
    result_df = DataFrame(result_dict)
    result_df.to_csv(os.getcwd()+"/result.csv",
                     sep=',',
                     na_rep='NaN',
                     columns=['sid', 'url'],
                     index=False)

    # API 2번 호출
    # 보내고자하는 파일을 'rb'(바이너리 리드)방식 열고
    files = open(os.getcwd()+'/result.csv', 'rb')
    upload = {'csv_file': files}
    # String 포맷
    obj = {"temperature": '23.5', "humidity": '54.5'}

    requests.post('http://localhost:8080/spInsertArticle', files=upload, data=obj)


if __name__ == "__main__":
    print("Start Crawling... :", datetime.datetime.now())

    collect_article()

    print("End Crawling... :", datetime.datetime.now())