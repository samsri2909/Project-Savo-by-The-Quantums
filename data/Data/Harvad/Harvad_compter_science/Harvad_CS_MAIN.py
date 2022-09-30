import contextlib
import time
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.parse import urljoin

start = time.time()

# initialize the list of all the data you need through lists

urls = []
name = []
types = []
duration = []
difficulty_level = []
Course_description = []
platforms = []
price = []

driver = webdriver.Chrome(executable_path = '/Users/sanskarjain/Project-Savo-by-The-Quantums/data/chromedriver')  # this is chrome you have to download it from google

# this is scrolling code if you need more data add this code in main function

"""
        while True:
            scroll_height = 3000
            document_height_before = driver.execute_script("return document.documentElement.scrollHeight")
            driver.execute_script(f"window.scrollTo(0, {document_height_before + scroll_height});")
            time.sleep(1.5)
            document_height_after = driver.execute_script("return document.documentElement.scrollHeight")
            if document_height_after == document_height_before:
                break    
"""

page = 18


def Data():
    base = 'https://online-learning.harvard.edu'
    for i in range(page):
        print("Loading Page number ", i)
        driver.get(f'https://online-learning.harvard.edu/catalog?keywords=&start_date_range%5Bmin%5D%5Bdate%5D=&start_date_range%5Bmax%5D%5Bdate%5D=&page={i}')

        content = driver.page_source.encode('utf-8').strip()
        soup = BeautifulSoup(content, 'lxml')
        link_class = soup.findAll("div", class_="field field-name-title-qs")
        for j in link_class[:]:
            link_tag = j.find("a")
            with contextlib.suppress(Exception):
                if 'href' in link_tag.attrs:
                    link = link_tag.get('href')
            url = urljoin(base, link)
            urls.append(url)


# sourcery skip: remove-redundant-pass, remove-zero-from-range, use-contextlib-suppress
Data()

for links in range(0, len(urls)):
    driver.get(urls[links])

    new_soup = BeautifulSoup(driver.page_source, "lxml")

    title = new_soup.find("div", class_="field field-name-title")

    subject = new_soup.find("div", class_="field field-name-subject-area field-type-ds field-label-inline clearfix")
    subject_tag = subject.find("a")

    length = new_soup.find("div", class_="field field-name-field-duration")

    difficulty = new_soup.find("div",
                               class_="field field-name-field-difficulty field-type-list-text field-label-inline clearfix")
    difficulty_tag = difficulty.find("div", class_="field")

    description = new_soup.find("div", class_="field field-name-body field-type-text-with-summary field-label-above")
    description_tag = description.find("p")

    platform = new_soup.find("div", class_="field field-name-platform")
    try:
        platform_tag = platform.find("div", class_="field field-name-field-course-platform")
    except AttributeError:
        pass

    prices = new_soup.find("div", class_="field field-name-price")

    name.append(title.text)
    types.append(subject_tag.text)
    try:
        duration.append(length.text)
    except AttributeError:
        duration.append("self paced")
        pass
    difficulty_level.append(difficulty_tag.text)
    Course_description.append(description_tag.text)
    platforms.append(platform_tag.text)
    price.append(prices.text)
    print("getting details of page no ", links)


print(len(urls))
print(len(name))
print(len(types))
print(len(duration))
print(len(price))
print(len(difficulty_level))
print(len(Course_description))
print(len(platforms))

driver.close()

df = pd.DataFrame({"links": urls,
                   "names": name,
                   'Type': types,
                   "Duration": duration,
                   "Price": price,
                   "difficulty": difficulty_level,
                   "Description": Course_description,
                   "platform": platforms})

df.to_csv("Harvard_courses.csv")
