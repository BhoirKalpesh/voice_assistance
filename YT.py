from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

class Music():
    def __init__(self):
        service = Service('C:\\Drivers\\chromedriver.exe')
        self.driver = webdriver.Chrome(service=service)

    def play(self, query):
        self.query = query
        self.driver.get(url="https://www.youtube.com/results?search_query=" + query)
        video = self.driver.find_element(By.XPATH, '//*[@id="dismissible"]')
        video.click()

#assist=Music()
#assist.play('kesariya by arijit singh')