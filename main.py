import time
import requests
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

RENTAL_URL = os.getenv("RENTAL_URL")  # rental url
FORM_URL = os.getenv("FORM_URL")  # form url

def setup():
    """
    Setup the environment variables and get the rental ads
    """
    load_dotenv() # load the environment variables

    chrome_options = webdriver.ChromeOptions()  # Create a new option object
    chrome_options.add_experimental_option("detach", True)  # Attach the driver to the background
    user_data_dir = os.path.join(os.getcwd(), "chrome_profile")  # Set the user data directory
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")  # Add the user data directory argument

    driver = webdriver.Chrome(options=chrome_options)  # Set up Selenium

    print("ℹ️ Initialized Selenium")

    return driver
def scrape_ads():
    """
    Scrape the rental ads from the rental url
    :return: titles, prices, locations, typologies, areas, links
    """
    headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36", "Accept-Language": "en-US,en;q=0.9"} # set the headers

    response = requests.get(RENTAL_URL, headers=headers)  # get the response
    yc_webpage = response.text  # get the text
    soup = BeautifulSoup(yc_webpage, "html.parser")  # parse the text

    ads = soup.select("article[data-sentry-component='AdvertCard']")  # select the ads
    print(f"ℹ️ {len(ads)} ads found")

    titles, prices, locations, typologies, areas, links = [], [], [], [], [], [] # initialize the lists
    for ad in ads:  # loop through the ads
        title = ad.select_one("[data-cy='listing-item-title']")  # select the title
        title = title.get_text(strip=True) if title else None  # get the text
        titles.append(title)  # append the title

        price = ad.select_one("[data-cy='listing-item-price'] span")  # select the price
        price = price.get_text(strip=True) if price else None  # get the text
        prices.append(price)  # append the price

        location = ad.select_one("[data-cy='advert-card-address']")  # select the location
        location = location.get_text(strip=True) if location else None  # get the text
        locations.append(location)  # append the location

        typology = ad.find("dt", string="Tipologia")  # select the typology
        if typology:  # if the typology is found
            typology = typology.find_next("dd").get_text(strip=True)  # get the text
            typologies.append(typology)  # append the typology

        area = ad.find("dt", string="Preço por metro quadrado")  # select the area
        if area:  # if the area is found
            area = area.find_next("dd").get_text(strip=True)  # get the text
            areas.append(area)  # append the area

        link = ad.select_one("[data-cy='listing-item-link']")  # select the link
        link = "https://www.imovirtual.com" + link["href"] if link else None  # get the link
        links.append(link)  # append the link

    print("ℹ️ Concluded scraping ads")
    return titles, prices, locations, typologies, areas, links
def submit_to_form(driver, titles, prices, locations, typologies, areas, links):
    """
    Submit the ads to the form
    :param driver: selenium driver
    :param titles: list of ads titles
    :param prices: list of ads prices
    :param locations: list of ads locations
    :param typologies: list of ads typologies
    :param areas: list of ads areas
    :param links: list of ads links
    """
    wait = WebDriverWait(driver, 5)  # Create a new wait object

    for i in range(len(links)):  # loop through the links
        driver.get(FORM_URL)  # go to the website

        wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div[2]/form/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input"))).send_keys(titles[i]) # wait for the title input
        wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div[2]/form/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input"))).send_keys(prices[i])  # wait for the price input
        wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div[2]/form/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input"))).send_keys(locations[i])  # wait for the location input
        wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div[2]/form/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[1]/div/div[1]/input"))).send_keys(typologies[i])  # wait for the typology input
        wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div/div[2]/form/div[2]/div/div[2]/div[5]/div/div/div[2]/div/div[1]/div/div[1]/input"))).send_keys(areas[i])  # wait for the area input
        wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div[2]/form/div[2]/div/div[2]/div[6]/div/div/div[2]/div/div[1]/div/div[1]/input"))).send_keys(links[i])  # wait for the link input

        submit_button = wait.until(EC.element_to_be_clickable((By.XPATH,"/html/body/div/div[2]/form/div[2]/div/div[3]/div[1]/div[1]/div/span"))) # wait for the Submit button
        submit_button.click()  # click the Submit button

        print(f"✅ Ad {i+1} submitted")
        time.sleep(5) # sleep for 5 seconds
    print("ℹ️ All ads submitted")

driver = setup() # setup the driver
titles, prices, locations, typologies, areas, links = scrape_ads(RENTAL_URL) # scrape the ads
submit_to_form(driver, FORM_URL, titles, prices, locations, typologies, areas, links) # submit the ads