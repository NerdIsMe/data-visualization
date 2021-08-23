import requests
from fake_useragent import UserAgent
from pyvirtualdisplay import Display
from selenium import webdriver

# 開啟虛擬化界面
display = Display(visible=0, size=(400, 300))
display.start()

driver = webdriver.Chrome()
url = 'https://en.wikipedia.org/wiki/'

driver.get(url)
print(driver.current_url)
# response = requests.get(url, headers={'user-agent': UserAgent().random})
# # print(response.text)
# for resp in response.history:
# 	print(resp.url)