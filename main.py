import time
import webdriver_manager.chrome
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

options = Options()
options.add_argument("start-maximized")
#options.headless = True

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://google.com/")

driver.implicitly_wait(2)

search = driver.find_element("name", "q")
search.send_keys("hii")
search.submit()
time.sleep(5000)
driver.close()
