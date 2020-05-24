from selenium import webdriver
import time
from PIL import Image
import requests
from io import BytesIO
import base64
import inspect

queries = ["text conversation"]
fles_to_get = 100 # optional param

path = 'train'

driver = webdriver.Chrome("/home/cjv/chromedriver")

SCROLL_PAUSE_TIME = 2

fle_num = 0

for query in queries:

    driver.get(f"https://www.google.com/search?q={query.replace(' ', '+')}&tbm=isch")

    divs = driver.find_elements_by_xpath('//div[@class="islrc"]/div/a/div/img')

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while len(divs) < fles_to_get:

        # check to see if the load more button is available, if it is then click it
        try:
            driver.find_element_by_xpath('//input[@type="button"]').click()
        except:
            pass

        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:

            print("We've reached the end")
            break

        # update the last height
        last_height = new_height

        divs = driver.find_elements_by_xpath('//div[@class="islrc"]/div/a/div/img')

    for div in divs:

        if fles_to_get and fle_num >= fles_to_get: # we exceeded the files to get
            break

        try:

            div.click()

            # wait to open
            time.sleep(0.5)

            # get the opened sidebar
            tags = driver.find_elements_by_xpath("//div[@id='islsp']/div/div/div/div/div/c-wiz/div/div/div/div/a/img")
            if len(tags) == 2:
                img = tags[0]
            else:
                img = tags[1]

            # get src and make call for data
            src = img.get_attribute('src')

            data = requests.get(url=src).content
            fle_type = Image.open(BytesIO(data)).format

            filename = f'{query}-{fle_num}.{fle_type}'  

            with open(f'{path}/{filename}', 'wb') as f:
                f.write(data)

            fle_num +=1
        
        except:

            continue

     
        

print(f'{fle_num} files returned')





