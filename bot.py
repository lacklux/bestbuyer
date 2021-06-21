"""
@author : tailorwilliams
Date : June 14 2020
"""

import json
import os
import re
import random
import sys
import time
from datetime import date
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
import undetected_chromedriver.v2 as uc


class Bot:
        def __init__(self):                
            self.option = uc.ChromeOptions()
            self.option.add_argument("--incognito")
            # self.option.add_argument('--headless')
            self.option.add_argument("--no-sandbox")
            self.option.add_argument("--disable-dev-shm-usage")
            self.option.add_argument("--disable-notifications")
            self.option.add_argument('--disable-blink-features=AutomationControlled')
            self.option.add_argument("--window-size=1280,800")
            self.option.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36")
            # self.option.add_argument('--user-data-dir=c:\\temp\\profile2')
            self.option.add_argument('--no-first-run --no-service-autorun --password-store=basic')
            self.driver= uc.Chrome(options=self.option)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.login()
        
        """login in to tiktok"""        
        def login(self):
            self.driver.get("https://www.tiktok.com/login/phone-or-email/email")
            print(self.driver.title)
            text_file = open('user.txt','+r')
            user_list = [line.split(line.strip(line.replace(":", ""))) for line in text_file]
            for user in user_list:
                self.username_key =  user[0]   
                self.password =user[1]
                # self.password = self.password.lstrip()
                time.sleep(random.randint(5,10))
                try:
                    self.login_details()
                    for i in range(10):
                        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                        print(f"scrolling through pages:{i}")
                        i-=1
                        time.sleep(8)
                    time.sleep(8)
                    self.get_videos()
                except Exception as e:
                    print(f"Unable to login because of {e}")
                    title_name = self.driver.title
                    print(title_name)
                    if title_name != "Log in with phone or email | TikTok":
                        pass
                    else:
                        self.login()
         
        """getting login details note:only use this format in your user.txt e.g username:password
        it most not be space embeded
        """            
        def login_details(self):
            username_input = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.NAME, 'email')))
            username_input.send_keys(self.username_key)
            print("username send successfully")
            password_input = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.NAME, 'password')))
            password_input.send_keys(self.password)
            print("password send successfully")
            login_button = WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div[1]/form/button')))
            login_button.click()
            print("login button clicked")
            print("solving captcha")
            time.sleep(random.randint(30,60))
            
        """getting the links of all the trending videos"""
        def get_videos(self):
            check= WebDriverWait(self.driver, 60).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'a')))
            links =[]
            for link in check:
                links.append(link.get_attribute('href'))
            get_video = "video"
            video = [url for url in links if get_video in url and url.startswith('https://www.tiktok.com/@')and not url.endswith('?lang=en')]
            print("videos",video)
            if video is not None:
                for trend in video:
                    self.driver.get(trend)
                    print("trend gets")
                    time.sleep(random.randint(10,15))
                    self.like()
                    self.comment()
                    time.sleep(random.randint(5,10))
            else:
                self.login()    
                
            
            """ loving the videos"""    
        
        """liking video"""    
        def like(self):
            print("liking video")
            try:
                heart = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, '//div/video')))
                action = ActionChains(self.driver)
                action.double_click(heart).perform()
                print("video like successfully")
            except Exception as e:
                print(f"error while liking vide:{e}")
            
        """comment on vidoe"""    
        def comment(self):
            try:
                comment_button = WebDriverWait(self.driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, '//div/div[@class="jsx-1809469258 bar-item-img engagement-icon-v23"]')))
                comment_button[1].click()
                print("comment button clicked")
                comment_input = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//div/div[@class="public-DraftStyleDefault-block public-DraftStyleDefault-ltr"]')))
                time.sleep(4)
                print("sending comment")
                with open('comment.txt','+r') as comment:
                    for line in comment:
                        comment_input.send_keys(line)
                        post = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, '//div/div[@class="jsx-338934743 post-container active"]')))
                        post.click()
                        print("comment post successfully")    
                        time.sleep(random.randint(5,8))
                        """close the comment windows"""
                    self.driver.execute_script("arguments[0].click();", WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH,'//div/img[@class="jsx-2034646630 control-icon close"]'))))
            except Exception as e:
                print(f"unable to comment due to :{e}")
                    
if __name__ =="__main__":
    Bot()
    
    
# https://developer.mozilla.org/en-US/docs/Web/API/Element/scrollTop