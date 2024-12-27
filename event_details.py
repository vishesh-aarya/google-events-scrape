import asyncio
import pandas as pd
from playwright.async_api import async_playwright

# Define input and output CSV file paths
INPUT_CSV = "events_url.csv"
OUTPUT_CSV = "event_detail.csv"

async def scrape_event_details():
    # Load the input CSV
    data = pd.read_csv(INPUT_CSV)

    # Filter URLs with 'N' flag
    urls_to_scrape = data[data['Flag'] == 'N']

    # Create or append to the output CSV
    output_columns = ['Region', 'Event Title', 'Event Date', 'Event URL']
    try:
        output_data = pd.read_csv(OUTPUT_CSV)
    except FileNotFoundError:
        output_data = pd.DataFrame(columns=output_columns)

    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="chrome", headless=True)

        for _, row in urls_to_scrape.iterrows():
            region = row['Region']
            url = row['Event URL']
            
            print(f"Scraping event details for Region: {region}, URL: {url}")
            try:
                page = await browser.new_page()
                await page.goto(url)
                
                # Wait for the dynamic content (adjust the selector if needed)
                await page.wait_for_selector("div.day-range", timeout=5000)

                # Extract event title
                event_title = await page.title()  # Extract page title as event title

                # Extract and parse event dates
                try:
                    date_elements = await page.query_selector("div.day-range")
                    if date_elements:
                        event_date = await date_elements.inner_text()  # Keep the full date string as-is
                    else:
                        event_date = "NULL"
                except Exception:
                    event_date = "NULL"

                # Add the data to the output dataframe
                output_data = pd.concat([
                    output_data,
                    pd.DataFrame({
                        'Region': [region],
                        'Event Title': [event_title],
                        'Event Date': [event_date],
                        'Event URL': [url]
                    })
                ], ignore_index=True)

                # Update the input CSV flag to 'Y'
                data.loc[data['Event URL'] == url, 'Flag'] = 'Y'

            except Exception as e:
                print(f"Error scraping event details for URL: {url}: {e}")
            finally:
                await page.close()

        await browser.close()

    # Save the updated input and output CSVs
    data.to_csv(INPUT_CSV, index=False)
    output_data.to_csv(OUTPUT_CSV, index=False)
    print(f"Scraping completed. Data saved to {OUTPUT_CSV}.")

# Execute the async script
import nest_asyncio
nest_asyncio.apply()
asyncio.run(scrape_event_details())
