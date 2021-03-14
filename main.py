from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time

GOOGLE_FORM_LINK = "https://docs.google.com/forms/d/e/1FAIpQLSciMiSxdDcpESFPuWp4f8kJRKTk6iAx8OP2G7J468S3FEev3w/viewform?usp=sf_link"
GOOGLE_FORM_ANSWERS_LINK = "https://docs.google.com/forms/d/1erK3jSZGDtc-XcHIAVjVOnrZyEe40oIre38efauI49c/edit#responses"
ZILLOW_LINK = "https://www.zillow.com/vancouver-bc/rentals/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22Vancouver%2C%20BC%22%2C%22mapBounds%22%3A%7B%22west%22%3A-123.33506481640626%2C%22east%22%3A-122.91209118359376%2C%22south%22%3A49.14772965639199%2C%22north%22%3A49.36732081125591%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A791534%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A888096%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A11%7D"
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
    "Accept-Language": "ru,en-US;q=0.9,en;q=0.8,ky;q=0.7"
}

response = requests.get(url=ZILLOW_LINK, headers=header)

soup = BeautifulSoup(response.content, "html.parser")

links = soup.find_all(name="a", class_="list-card-link list-card-link-top-margin list-card-img")
links_list = []
for link in links:
    if not link["href"].startswith("https"):
        link["href"] = "https://www.zillow.com" + link["href"]
    links_list.append(link["href"])

prices = soup.find_all(name="div", class_="list-card-price")
prices_list = [price.text[0 : 7] for price in prices]

addresses = soup.find_all(name="address", class_="list-card-addr")
addresses_list = [address.text for address in addresses]

chrome_driver_path = "C:\chromedriver_win32\chromedriver.exe"
driver = webdriver.Chrome(chrome_driver_path)
driver.implicitly_wait(10)
driver.get(GOOGLE_FORM_LINK)
driver.maximize_window()

time.sleep(3)

for index in range(len(links_list)):
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(addresses_list[index])
    driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(prices_list[index])
    driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(links_list[index])

    driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div/span/span').click()
    time.sleep(2)
    driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[4]/a').click()


driver.get(GOOGLE_FORM_ANSWERS_LINK)
driver.maximize_window()

driver.find_element_by_xpath('//*[@id="ResponsesView"]/div/div[1]/div[1]/div[2]/div[1]/div/div/span/span').click()