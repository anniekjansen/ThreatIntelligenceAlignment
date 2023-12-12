import pandas as pd

import requests

from bs4 import BeautifulSoup
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

from DataLoaderSaver import DataLoaderSaver
from DataAnalyzer import DataAnalyzer
# from DataProcessor import DataProcessor

""" Load initial dataset """
# data = DataLoaderSaver().load_dataset("initial")
# print(data)

"""   """


from bs4 import BeautifulSoup
from selenium import webdriver

URL = "https://www.ncsc.nl/actueel/advisory?id=NCSC-2023-0256"
browser = webdriver.Chrome()
browser.get(URL)

element = WebDriverWait(browser, 3).until(
    EC.presence_of_element_located((By.ID, 'ncsc_adv_history'))
)
html = browser.page_source
soup = BeautifulSoup(html, 'lxml')

kans = soup.find("tr", class_="adv_field adv_field_kans")

# print(kans.prettify())

kans_questions = kans.find_all("th", class_="matrix_explain")
kans_answers = kans.find_all("td", class_="matrix_short")

# print(len(kans_questions))
# print(len(kans_answers))

questions = []
answers = []

for element in kans_questions:
    # print(element.text, end="\n"*2)
    questions.append(element.text)

for element in kans_answers:
    # print(element.text, end="\n"*2)
    answers.append(element.text)

answers.pop(0)
# print(questions)
# print(answers)

kans_dict = dict()

for item in range(0,len(questions)):
    kans_dict[questions[item]] = answers[item]

print(kans_dict)

