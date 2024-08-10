from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from exceptions import *
from time import sleep
from sys import exit
import os
import pickle
import pandas as pd

class Pinterest():
    def __init__(self, login, pw):
        self.domains = [".pinterest.com", ".www.pinterest.com", "www.pinterest.com", ".www.pinterest.co.kr", "www.pinterest.co.kr"]
        self.piclist = []
        self.href_list = []  # Add this line
        self.currentdir = os.getcwd()
        self.user_agent = ""
        options = webdriver.ChromeOptions()
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")
        options.add_argument("--log-level=3")
        self.driver = webdriver.Chrome(options=options)
        self.user_agent = self.driver.execute_script("return navigator.userAgent;")
        
        if os.path.exists("cookies.pkl"):
            print("Loading cookies...")
            self.driver.get("https://pinterest.com")
            self.driver.implicitly_wait(3)
            sleep(2)
            cookies = pickle.load(open("cookies.pkl", "rb"))
            for cookie in cookies:
                for domain in self.domains:
                    try:
                        self.driver.add_cookie({
                            "domain": domain,
                            "name": cookie["name"],
                            "value": cookie["value"],
                            "path": '/'
                        })
                    except Exception as e:
                        print(f"Failed to add cookie for domain {domain}: {e}")
                        pass
            self.driver.get("https://pinterest.com")
            self.driver.implicitly_wait(3)
            try:
                self.driver.find_element(By.XPATH, '//*[@id="HeaderContent"]')
                return
            except:
                print("Failed to login from cookies.. login manually")

        try:
            self.driver.get("https://pinterest.com/login")
            self.driver.implicitly_wait(3)
            for i in range(3):
                try:
                    self.driver.find_element(By.ID, "email")
                    break
                except:
                    sleep(1)
            emailelem = self.driver.find_element(By.ID, "email")
            passelem = self.driver.find_element(By.ID, "password")
            emailelem.send_keys(login)
            passelem.send_keys(pw)
            sleep(1)
            self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        except Exception as e:
            raise e
        
        while True:
            try:
                self.driver.find_element(By.XPATH, '//*[@id="HeaderContent"]')
                break
            except:
                sleep(1)
                try:
                    self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
                except:
                    pass
        self.dump()

    def dump(self):
        cookies = self.driver.get_cookies()
        pickle.dump(cookies, open("cookies.pkl", "wb"))

    def crawl(self):
        timeout = 0
        height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(2)
            now_height = self.driver.execute_script("return document.body.scrollHeight")

            if now_height != height:
                self.collect_image_urls()
                break
            else:
                timeout += 1
                if timeout >= 5:
                    print("It seems we find the end of current page, stop crawling.")
                    raise EndPageException
        sleep(2)
    
    def single_download(self, n=-1, url="https://pinterest.com/", name="default"):
        if n == -1:
            n = 999999999

        directory = os.path.join(self.currentdir, name)
        if not os.path.exists(directory):
            os.mkdir(directory)
        
        self.driver.get(url)
        self.driver.implicitly_wait(3)
        for i in range(n):
            try:
                self.crawl()
            except EndPageException:
                break
            print(f"Scroll down {i} Page, collected URLs.")
        
        print(f"Totally collected {len(self.piclist)} image URLs.")
        self.save_to_csv(name)
    
    def batch_download(self, n=-1, url_list=[], name_list=[], default_name="default"):
        url_count = len(url_list)
        name_count = len(name_list)
        if n == -1:
            n = 9999999
        if name_list and url_count != name_count:
            print("url_list and name_list must have same length.")
            exit()

        for i in range(url_count - 1):
            self.driver.execute_script("window.open('','_blank');")

        for i in range(url_count):
            self.driver.switch_to.window(self.driver.window_handles[i])
            self.driver.get(url_list[i])
            self.driver.implicitly_wait(3)

        for i in range(n):
            for uindex in range(url_count):
                name = name_list[uindex] if name_count != 0 else default_name

                directory = os.path.join(self.currentdir, name)
                if not os.path.exists(directory):
                    os.mkdir(directory)
                
                try:
                    self.driver.switch_to.window(self.driver.window_handles[uindex])
                except:
                    continue

                try:
                    self.crawl()
                except EndPageException:
                    del url_list[uindex]
                    del name_list[uindex]
                    self.driver.close()
                    url_count -= 1
                    name_count -= 1

                print(f"Scroll down from {url_list[uindex]}, {i} Page, collected URLs.")
                self.save_to_csv(name)

    def collect_image_urls(self):
        req = self.driver.page_source
        soup = BeautifulSoup(req, 'html.parser')
        pics = soup.find_all("img")
        if not pics:
            return 0
        for pic in pics:
            src = pic.get("src")
            parent = pic.find_parent('a')
            href = parent.get('href') if parent else None

            if "75x75_RS" in src:
                continue

            if src not in self.piclist:
                self.piclist.append(src)
                self.href_list.append(href)
    
    def save_to_csv(self, name):
        data = {"name": [name] * len(self.piclist), "url": self.piclist, "href": self.href_list}
        df = pd.DataFrame(data)
        csv_file = os.path.join(self.currentdir, "url_data.csv")
        
        if os.path.exists(csv_file):
            df.to_csv(csv_file, mode='a', header=False, index=False)
        else:
            df.to_csv(csv_file, mode='w', header=True, index=False)
        
        self.piclist = []
        self.href_list = []

    def getdriver(self):
        return self.driver
