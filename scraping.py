import time
import uuid
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from time import sleep




# MongoDB setup
client = MongoClient('mongodb+srv://ronitd552:PfmoRTlhoJJ5ivoN@cluster0.t0piakl.mongodb.net/webscrapdb?retryWrites=true&w=majority')
db = client['twitter_scrape']
collection = db['trending_list']

# ProxyMesh setup
proxy = "http://us-dc.proxymesh.com:31280"

# Selenium setup with ProxyMesh

chrome_options = webdriver.ChromeOptions()

chrome_options.add_argument('–proxy-server=http://us-ca.proxymesh.com:31280')
                            

# chrome_options.add_argument(f"--proxy-server={proxy}")

driver = webdriver.Chrome(options=chrome_options)

def scrape_twitter_trends():
    
    driver.get('https://twitter.com/login')
    print("inside twitter home page")

    # Enter your login details using find_element (safer)
    # username = driver.find_element(By.NAME, 'text')
    # username.send_keys('DasRonit44793')
    
    # driver.find_element(By.CSS_SELECTOR, 'css-175oi2r.r-sdzlij.r-1phboty.r-rs99b7.r-lrvibr.r-ywje51.r-184id4b.r-13qz1uu.r-2yi16.r-1qi8awa.r-3pj75a.r-1loqt21.r-o7ynqc.r-6416eg.r-1ny4l3l').click()
    
    username = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.NAME, 'text'))
    )

    username.send_keys('DasRonit44793')

    login_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.css-175oi2r.r-sdzlij.r-1phboty.r-rs99b7.r-lrvibr.r-ywje51.r-184id4b.r-13qz1uu.r-2yi16.r-1qi8awa.r-3pj75a.r-1loqt21.r-o7ynqc.r-6416eg.r-1ny4l3l'))
    )

    login_button.click()

    time.sleep(5) 

    password = driver.find_element(By.NAME, 'password')
    password.send_keys('tweet#123')
    
    driver.find_element(By.CSS_SELECTOR, '[data-testid="LoginForm_Login_Button"]').click()
    time.sleep(5)  
    # driver.get('https://x.com/home')
    print("Inside Home page")
   # Wait for the section to load that contains the trending topics
    WebDriverWait(driver, 70).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'section[aria-labelledby="accessible-list-0"] div.css-175oi2r'))
    )

    trending_divs = driver.find_elements(By.CSS_SELECTOR, 'section[aria-labelledby="accessible-list-0"] div.css-175oi2r')

    trend_names = [div.text for div in trending_divs[:5]]

    if len(trend_names) < 5:
        print(f"Error: Expected 5 trending topics, but got {len(trend_names)}. List: {trend_names}")
        driver.quit()
        return

    print("Trending topics:", trend_names)



    # Use safe access to avoid index out of range errors
    unique_id = str(uuid.uuid4())
    end_time = datetime.now()
    current_ip = proxy.split('@')[-1]

    document = {
            '_id': unique_id,
            'trend1': trend_names[0] if len(trend_names) > 0 else None,
            'trend2': trend_names[1] if len(trend_names) > 1 else None,
            'trend3': trend_names[2] if len(trend_names) > 2 else None,
            'trend4': trend_names[3] if len(trend_names) > 3 else None,
            'end_time': end_time,
            'ip_address': current_ip
        }
    collection.insert_one(document)

    # Close browser
    driver.quit()

    return document
