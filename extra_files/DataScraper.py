import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

class DataScraper:

    def url_maker(self, NCSC_ID):
        # url = "https://www.ncsc.nl/actueel/advisory?id=" + "NCSC-2023-0256"
        url = "https://www.ncsc.nl/actueel/advisory?id=" + NCSC_ID
        return url
    
    def load_beautifulsoup(self, url):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        browser = webdriver.Chrome(options=chrome_options)
        browser.get(url)
        try:
            WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, 'ncsc_adv_history')))
            html = browser.page_source
            soup = BeautifulSoup(html, 'lxml')
            return soup
        except: 
           pass

    def scrape_data(self, soup, scrape):
        
        if scrape == "kans":
            data_class = "adv_field adv_field_kans"
        elif scrape == "schade":
            data_class = "adv_field adv_field_schade"
        else:
            print("wrong data input (possible inputs: kans / schade)")


        data_found = soup.find("tr", class_= data_class)

        # print(kans.prettify())

        data_questions = data_found.find_all("th", class_="matrix_explain")
        data_answers = data_found.find_all("td", class_="matrix_short")

        questions = []
        answers = []

        for element in data_questions:
            questions.append(element.text)

        for element in data_answers:
            answers.append(element.text)

        answers.pop(0)

        data_dict = dict()

        for item in range(0,len(questions)):
            data_dict[questions[item]] = answers[item]

        # print(scrape)
        # print(data_dict)

        return data_dict
    
