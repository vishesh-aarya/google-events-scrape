from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time

# Set up Chrome options (no headless mode, so you can see the window)
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

# Path to your ChromeDriver (update this path)
driver_path = "C:/Users/Relanto/Desktop/chromedriver.exe"

# Initialize the Chrome driver
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open the target URL
url = "https://cloud.google.com/events/?hl=en&ser=EiQKDWZpbHRlcl90eXBlXzMQASIREg9maWx0ZXJfdmFsdWVfMzYSIwoNZmlsdGVyX3R5cGVfMRABIhASDmZpbHRlcl92YWx1ZV8y"
driver.get(url)

# Function to scroll down the page
def scroll_down():
    """Scroll down to the bottom of the page."""
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    scroll_height = driver.execute_script("return document.body.scrollHeight")
    target_height = scroll_height * 0.6  # 80% of the page height
    driver.execute_script(f"window.scrollTo(0, {target_height});")
    time.sleep(2)  # Allow time for the page to load

# Function to click the "Show more" button
def click_show_more():
    try:
        # Locate the "Show more" button using Scrapy-style CSS selector
        show_more_button = driver.find_element(By.XPATH, '//button[@track-type="button" and contains(text(), "Show")]')
        
        # Scroll to the "Show more" button to make it visible
        ActionChains(driver).move_to_element(show_more_button).perform()
        
        # Click the "Show more" button
        show_more_button.click()
        print("Clicked 'Show more' button.")
        
        # Wait for new content to load
        time.sleep(2)
    except Exception as e:
        print(f"Error clicking 'Show more' button: {e}")

# Click "Show more" button up to 5 times
for i in range(5):
    print(f"Iteration {i + 1}:")
    click_show_more()
    
    # Scroll down to load more content
    scroll_down()

# Scrape the event URLs
# event_elements = driver.find_elements(By.CSS_SELECTOR, "a[data-testid='event-link']")
# event_elements = driver.find_elements(By.XPATH, '//div//ul//li[@class="AZgcHf pV2hx"]//a')
# event_urls = [event.get_attribute("href") for event in event_elements]

links = driver.find_elements(By.XPATH, '//div//ul//li[@class="AZgcHf pV2hx"]//a')

# Extract and print the URLs
for link in links:
    url = link.get_attribute('href')
    print(url)

# Print the scraped URLs
# print("\nScraped event URLs:")
# for url in event_urls:
#     print(url)

# Close the browser
driver.quit()