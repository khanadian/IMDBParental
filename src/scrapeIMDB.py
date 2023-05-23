from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import csv
import time

start_time = time.time()
MOST_POPULAR_URL = "https://www.imdb.com/chart/tvmeter/?ref_=tt_ov_pop"
TOP_RATED_URL = "https://www.imdb.com/chart/toptv/?sort=rk,asc&mode=simple&page=1"

#Grabs the parents guide from IMDB
def main(url):
    driver = webdriver.Chrome()
    driver.set_window_position(2000, 100) #moves window to 2nd monitor

    file = open("IMDBParentsGuide.csv", 'w', newline='')
    writer = csv.writer(file)

    #write header rows
    writer.writerow(['Show', 'Popularity', 'IMDB Rating', 'Sex/Nudity', 'Violence/Gore',\
                     'Profanity', 'Alochol/Drugs/Smoking', 'Frightening/Intense'])

    driver.get(url)
    shows = WebDriverWait(driver, 10).until(EC.presence_of_element_located(\
    (By.CLASS_NAME, "lister-list")))

    show_array = [[]]
    for show in shows.find_elements(By.CSS_SELECTOR, 'tr'):
        show_array += [get_info(show, driver)]
    show_array.pop(0) #remove the empty array
    for i in range(len(show_array)):
        guide_link = get_guide_link(driver, show_array[i][3])
        guide = get_guide(driver, guide_link)
        show_array[i].pop(3) #remove url
        show_array[i] += guide
        writer.writerow(show_array[i])
    
    driver.close()
    driver.quit()
    file.close()
    
def get_info(show, driver):
    title_wrapper = show.find_element(By.CLASS_NAME, "titleColumn")
    rating_wrapper = show.find_element(By.CLASS_NAME, "ratingColumn")
    
    temp = title_wrapper.text.split(')')
    title = temp[0] + ')'
    popularity = temp[1].split('(')[0].strip()
    
    show_link = title_wrapper.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
    rating = rating_wrapper.text

    return ([title, popularity, rating, show_link])


def get_guide_link(driver, show_link):
    driver.get(show_link)
    body = driver.find_element(By.CSS_SELECTOR, 'body')
    for i in range(6):
        body.send_keys(Keys.PAGE_DOWN)
    try:
        guideLink = WebDriverWait(driver, 10).until(EC.presence_of_element_located(\
    (By.CSS_SELECTOR, "a[aria-label='Parents guide: see all']"))).get_attribute("href")
    except:
        return "N/A"
    return guideLink

def get_guide(driver, guide_link):
    if guide_link == "N/A":
        return []
    driver.get(guide_link)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(\
    (By.CSS_SELECTOR, "div[class='advisory-severity-vote__container ipl-zebra-list__item']"))) #workaround since classname has a space
    guides = driver.find_elements(By.CSS_SELECTOR, "div[class='advisory-severity-vote__container ipl-zebra-list__item']")
    return_values = []
    for guide in guides:
        if len(guide.text) != 0:
            return_values += [guide.text.split()[0]]
    return return_values

if __name__ == "__main__":
    start_time = time.time()
    main(TOP_RATED_URL)
    print("--- %s seconds ---" % (time.time() - start_time))
