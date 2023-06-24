from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
from bs4 import BeautifulSoup
import pandas as pd

#selenium으로 chrome브라우저 열기
chrome_option = webdriver.ChromeOptions()
chrome_option.add_experimental_option('detach',True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_option)

#화면창 크게하기
driver.maximize_window()
driver.get('http://www.theborn.co.kr/store/domestic-store/')

#10초동안 서울특별시 클릭하기
time.sleep(10)

#다음페이지 넘기기 위한 함수
def incdec(x):
    if x == 0:
        return 6
    elif x == 1 or x == 53:
        return 7
    else: return 8

#빈 리스트 생성
name_list = []
address_list = []

#페이지 넘길때마다 받아옴
for i in range(54):

    scroll_height = driver.execute_script('return document.body.scrollHeight')

    while True:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(1)

        now_height = driver.execute_script('return document.body.scrollHeight')

        if scroll_height == now_height:
            break

# id_list = soup.select("div#header-author > h3 > #author-text > span")
# comment_list = soup.select("yt-formatted-string#content-text")

    html_source = driver.page_source
    soup = BeautifulSoup(html_source, 'html.parser')
    id_list = soup.find_all('ul', class_='map_more2')

    time.sleep(2)
    for temp in id_list:
        li = temp.text
        li = li.split(' ')[1:-3]
        del li[1]
        del li[1]
        name = li[0]
        address = ' '.join(li[1:])
        name_list.append(name)
        address_list.append(address)
    time.sleep(1)

    driver.find_element(By.CSS_SELECTOR, '#pagination > li:nth-child(' + str(incdec(i)) + ')').click()
    # driver.find_element(By.CSS_SELECTOR, '#pagination > li:nth-child(6)').click()

    time.sleep(3)

#마지막 페이지는 스크롤 없이, 다음페이지 넘기기 없이 받아오기만 하기

html_source = driver.page_source
soup = BeautifulSoup(html_source, 'html.parser')
id_list = soup.find_all('ul', class_='map_more2')

for temp in id_list:
    li = temp.text
    li = li.split(' ')[1:-3]
    del li[1]
    del li[1]
    name = li[0]
    address = ' '.join(li[1:])
    name_list.append(name)
    address_list.append(address)

#dictionary형태로 저장
result_dict = {}
result_dict['name'] = name_list
result_dict['address'] = address_list

#csv로 저장
df = pd.DataFrame.from_dict(result_dict)
df.to_csv(('더본코리아 주소 데이터.csv'))
