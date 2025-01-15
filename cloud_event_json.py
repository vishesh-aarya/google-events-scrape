from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json

# Function to scrape event data
def scrape_events(url):
    # Set up the webdriver (assuming you're using Chrome)
    driver = webdriver.Chrome()

    # Open the provided URL
    driver.get(url)

    # Wait for the page to load (you can adjust the time if necessary)
    time.sleep(5)

    # Find all event list items
    events = driver.find_elements(By.XPATH, "//li[@class=' AZgcHf pV2hx']")

    # List to store event data
    event_data = []

    # Loop through each event and extract the required details
    for event in events:
        # Extract the title
        title = event.find_element(By.XPATH, ".//div[@class=' CilWo ']").text
        
        # Extract the date
        date = event.find_element(By.XPATH, ".//p[@class='mmPl6c JdGRg I5uvM']| .//p[contains(@class,'mmPl6c')]").text
        
        # Extract the event type (online, live, etc.)
        event_type = event.find_element(By.XPATH, ".//div[@class='aNvNV']").text

        #extract the event url
        event_url = event.find_element(By.XPATH, ".//a[@class='aOrzRd yIs5hd']").get_attribute("href")

        #extract the event description
        # Extract the description
        event_description = event.find_element(By.XPATH, ".//div[@class='Y1Fktf']").text
        
        # Add the extracted data to the list
        event_data.append({
            "title": title,
            "date": date,
            "type": event_type,
            "url" : event_url,
            "description" : event_description
        })

    # Close the browser window
    driver.quit()

    # Return the collected data
    return event_data

# Take the URL input from the user
root_url = input("Enter the root URL to scrape: ")

# Call the scrape function
scraped_data = scrape_events(root_url)

# Convert the data to JSON format and print it
json_data = json.dumps(scraped_data, indent=4)

# Optionally, save the data to a JSON file
with open('scraped_events.json', 'w') as json_file:
    json_file.write(json_data)

# Print the scraped data
print(json_data)
