from bs4 import BeautifulSoup
#Using Selenium3 due to being on windows
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from seleniumwire import webdriver

# Change to True if running chrome in background is desired
run_browser_in_background = False

def get_user_agent():
    # Hide the fact we are a bot
    ua = UserAgent(browsers=['chrome'], use_cache_server=False, cache=False, verify_ssl=False)
    user_agent = ua.random
    return user_agent

def create_chrome_options():
    chrome_options = webdriver.ChromeOptions()

    # Check to see if user wants chrome in the background instead
    if run_browser_in_background is True:
        chrome_options.add_argument("--headless")

    # Help disguise the bot
    user_agent = get_user_agent()
    chrome_options.add_argument(f'user-agent={user_agent}')

    return chrome_options

def scrape_amazon_page(soup):
    # Scrape amazon page for specific tags
    product_title = soup.find("span", attrs={"id": 'productTitle'}).text.strip()
    price_parent = soup.find('span', 'a-price')
    product_price = float(price_parent.find('span', 'a-offscreen').text.replace('$', ''))
    return product_title, product_price

def scrape_walmart_page(soup):
    # TODO walmart page for specific tags
    return "", 0.0

def start_scrape_page(url, event=None):
    chrome_options = create_chrome_options()
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), chrome_options=chrome_options)

    product_title = ""
    product_price = 0.00

    try:
        # Assign the url to the driver and wait for all elements to load on the page before moving forward
        driver.get(url)

        # Check to see if event is set to stop thread
        if event is not None:
            if event.is_set():
                return product_title, product_price

        # Timeout in 10 seconds if the page is still loading
        item = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '/html/body')))

        # Check to see if event is set to stop thread
        if event is not None:
            if event.is_set():
                return product_title, product_price

        # Soup Object containing all data from the selenium page running in the background
        soup = BeautifulSoup(driver.page_source, "lxml")

        if str(url).find("amazon") > -1:
            product_title, product_price = scrape_amazon_page(soup)
        elif str(url).find("walmart") > -1:
            product_title, product_price = scrape_walmart_page(soup)

    except Exception as e:
        # TODO: Create tkinter window where this is shown
        # Program will continue to run even after a fail
        print("ERROR: The provided url does not contain the needed elements to determine price.\n"
              "Please check the validity of the url.")

    # Close the driver after use
    driver.quit()

    return product_title, product_price
