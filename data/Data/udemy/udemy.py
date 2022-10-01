# made this ready for web scraping
import requests
from bs4 import BeautifulSoup
import json
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from user_agent import get_ua
from requests import get
import pandas as pd

request = requests.Session()
retry = Retry(connect=5, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
request.mount('http://', adapter)
request.mount('https://', adapter)



# https://www.udemy.com/api-2.0/search-courses/?src=ukw&q=python&skip_price=true

# make a class for the udemy
class Udemy:
    def __init__(self):
        self.pages = 10
    
    def get_courses(self, keyword):
        """
        Fetch courses using keyword from server side www.udemy.com
        :param keyword: str
        :return: list[dict]
        """

        courses_list = []
        for i in range(self.pages):
            curr_page = i + 1
            print(f"Fetching page {curr_page} for '{keyword}'")

            URL = f"https://www.udemy.com/api-2.0/search-courses/?p={curr_page}&q={keyword}" \
                  f"&sort=newest&src=ukw&skip_price=true&ordering=newest"
            #print(URL)

            HEADERS = {"authority": "www.udemy.com",
                       "User-Agent": get_ua(),
                       "referer": f"https://www.udemy.com/courses/search/?q={keyword}"}
            try:
                response = get(URL, headers=HEADERS, timeout=10)

                if response.status_code == 200:
                    courses = response.json()['courses']
                    courses_list += courses
                    df = pd.DataFrame(courses_list)
                    df.to_json("data/Data/udemy/udemy_info_{}.json".format(keyword), orient='records', lines=True)

                else:
                    print(f"Failed to fetch page {curr_page} for '{keyword}'")
            except:
                print("connection problems please check your internet")
    
        return None


    def get_course_info(self):

        """
        Fetch course info with chosen fields from server side www.udemy.com
        :param course_id: int
        :return: dict (_class, course id, title, url, created, published_time) of requested course
        """
        df = pd.read_json("data/Data/data.json", lines=True)
        course_id = df["id"].tolist()
        course_info = []
        for i in range(0,len(course_id)):

            URL = "https://www.udemy.com/api-2.0/courses/{}/?fields[course]=title,url,created,published_time".format(course_id[i])

            HEADERS = {"authority": "www.udemy.com",
                    "User-Agent": get_ua()
                    }
            try:
                response = get(URL, headers=HEADERS, timeout=5)
                #print(response.status_code)
                if response.status_code == 200:
                    print("get course info from course id", i)
                    course_info.append(response.json())

            except:
                print("connection problems please check your internet")
            
        df = pd.DataFrame(course_info)
        df.to_json("data/Data/compile_data.json", orient='records', lines=True)

        return None



if __name__ == '__main__':
    scraper = Udemy()
    df = pd.read_csv("data/Data/udemy/keywords.txt")
    keywords = df["0"].tolist()
    for i in range(0,len(keywords)):
        scraper.get_courses(keywords[i])
    
    data = []
    for i in range(len(keywords)):
        for line in open('data/Data/udemy/udemy_info_{}.json'.format(keywords[i]), 'r'):
            data.append(json.loads(line))

    df = pd.DataFrame(data)
    df.to_json('data/Data/data.json', orient='records', lines=True)

    scraper.get_course_info()