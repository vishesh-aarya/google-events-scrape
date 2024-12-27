import asyncio
import pandas as pd
from playwright.async_api import async_playwright

# Define input and output CSV file paths
INPUT_CSV = "google_cloud_events_regions.csv"
OUTPUT_CSV = "events_url.csv"

async def scrape_urls():
    # Load the input CSV
    data = pd.read_csv(INPUT_CSV)

    # Filter URLs with 'N' flag
    urls_to_scrape = data[data['flag'] == 'N']

    # Create or append to the output CSV
    output_columns = ['Region', 'Event URL', 'Flag']
    try:
        output_data = pd.read_csv(OUTPUT_CSV)
    except FileNotFoundError:
        output_data = pd.DataFrame(columns=output_columns)

    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="chrome", headless=True)

        for _, row in urls_to_scrape.iterrows():
            region = row['Region']
            url = row['URL']
            
            print(f"Scraping URL for Region: {region}")
            try:
                page = await browser.new_page()
                await page.goto(url)
                
                # Wait for dynamic content (adjust selector if needed)
                await page.wait_for_selector("a.aOrzRd")
                
                # Extract href attributes of event URLs
                event_links = await page.eval_on_selector_all(
                    "a.aOrzRd",
                    "elements => elements.map(el => el.href)"
                )

                # Add the data to the output dataframe
                for link in event_links:
                    output_data = pd.concat([
                        output_data,
                        pd.DataFrame({'Region': [region], 'Event URL': [link], 'Flag': ['N']})
                    ], ignore_index=True)

                # Update the input CSV flag to 'Y'
                data.loc[data['Region'] == region, 'flag'] = 'Y'

                print(f"Scraped {len(event_links)} event URLs for Region: {region}")

            except Exception as e:
                print(f"Error scraping URL for Region: {region}: {e}")
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
asyncio.run(scrape_urls())
