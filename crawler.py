from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import base64
import os
import requests
import urllib.parse

from config import engine_url
from utils import generate_dirlist

class CrawPictures():
    def __init__(self,data_path,keyword,prefix,suffix,indexoff,maxnum,search_engine,generate_list):
        self.data_path = data_path
        self.keyword = urllib.parse.quote(keyword)
        self.prefix = prefix
        self.suffix = suffix
        self.indexoff = indexoff
        self.maxnum = maxnum
        self.search_engine = search_engine
        self.generate_list = generate_list

    def run(self):
        self.browser = webdriver.Chrome()
        self.img_index = 1
        picelementsbase = []
        picelementsurls = []
        current_count = 0
        url = engine_url[self.search_engine].format(self.keyword,self.keyword)
        self.browser.get(url)
        while True:
            try:
                picelementsbase = self.browser.find_elements_by_css_selector("[class='mimg rms_img']")
                picelementsurls = self.browser.find_elements_by_css_selector("[class='mimg']")
                current_count = len(picelementsbase) + len(picelementsurls)
            except:
                pass
            if current_count >= self.maxnum:
                break
            try:
                seemore_btn = self.browser.find_element_by_css_selector("[class='mm_seemore']")
                seemore_btn.click()
            except:
                try:
                    body = self.browser.find_element_by_css_selector('body')
                    body.send_keys(Keys.PAGE_DOWN)
                except:
                    pass

        os.makedirs(self.data_path,exist_ok=True)
        print('current page have {} images'.format(current_count))
        print('image urls : {}'.format(len(picelementsurls)))
        print('image bases : {}'.format(len(picelementsbase)))
        for element in picelementsurls:
            try:
                basedata = requests.get(element.get_attribute('src')).content
                basedata = base64.b64encode(basedata)
                with open(os.path.join(self.data_path,
                                       '{}_{}.{}'.format(self.prefix, self.img_index + self.indexoff, self.suffix)),
                          'wb') as f:
                    f.write(base64.b64decode(basedata))
                if self.img_index >= self.maxnum:
                    break
                self.img_index += 1
            except:
                pass

        for element in picelementsbase:
            try:
                basedata = element.get_attribute('src')
                basedata = basedata.replace('data:image/jpeg;base64,', '')
                with open(os.path.join(self.data_path,'{}_{}.{}'.format(self.prefix, self.img_index + self.indexoff,self.suffix)),'wb') as f:
                    f.write(base64.b64decode(basedata))
                if self.img_index >= self.maxnum:
                    break
                self.img_index += 1
            except:
                pass
        print('crawlering done')
        if self.generate_list:
            generate_dirlist(self.data_path,os.path.relpath(os.path.join(self.data_path,'list.txt')))
            print('generate list done')

    def quit(self):
        self.browser.quit()
        pass