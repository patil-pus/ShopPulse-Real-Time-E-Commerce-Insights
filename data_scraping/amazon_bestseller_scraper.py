from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time
import json
from selenium.common.exceptions import NoSuchElementException
from saveCSV import save_to_csv

def setup_driver():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    service = webdriver.ChromeService()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.execute_cdp_cmd("Network.enable", {}) 
    return driver


def scrape_amazon_sportswear():
    driver = setup_driver()
    url = "https://www.amazon.com"
    driver.get(url)
    time.sleep(2)
    driver.get(url)
    search_box = driver.find_element(By.ID, "twotabsearchtextbox")
    search_box.send_keys("Sport")
    driver.find_element(By.ID, "nav-search-submit-button").click()
    time.sleep(3)

    scraped_data = []
    while True:
        items = driver.find_elements(By.XPATH, '//div[@data-component-type="s-search-result"]')

        for item in items:
            try:
                name = item.find_element(By.CSS_SELECTOR, "h2.a-size-medium.a-spacing-none.a-color-base.a-text-normal").text
            except NoSuchElementException:
                name = "N/A"

            try:
                price = item.find_element(By.CSS_SELECTOR, "span.a-price").text
            except NoSuchElementException:
                price = "N/A"

            try:
                original_price = item.find_element(By.CSS_SELECTOR, "div.a-section.aok-inline-block span.a-price.a-text-price span.a-offscreen").get_attribute('innerHTML')
            except NoSuchElementException:
                original_price = "N/A"

            try:
                rating = item.find_element(By.CSS_SELECTOR, "span.a-icon-alt").get_attribute("innerHTML").split(" ")[0]
            except NoSuchElementException:
                rating = "N/A"

            try:
                num_ratings = item.find_element(By.CSS_SELECTOR, "span.a-size-base.s-underline-text").text
            except NoSuchElementException:
                num_ratings = "N/A"

            scraped_data.append({
                "Name": name,
                "Price": price,
                "Original Price": original_price,
                "Rating": rating,
                "Number of Ratings": num_ratings
            })

        try:
            next_button = driver.find_element(By.CSS_SELECTOR, "a.s-pagination-next")
            if "s-pagination-disabled" in next_button.get_attribute("class"):
                print("Last page reached!")
                break
            else:
                print(scraped_data)
                next_button.click()
                time.sleep(3) 
            
        except NoSuchElementException:
            print("No 'Next' button found. Exiting...")
            break
    save_to_csv(scraped_data,'amazon_sports_collection')
    time.sleep(60)
    
    driver.quit()


if __name__ == "__main__":
    scrape_amazon_sportswear()
