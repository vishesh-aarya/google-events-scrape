# google-events-scrape
first-stage-scraping

1. Run regions.py. It will read the input file google_cloud_events_region.csv and change the flag to Y once the events url are fetched. It will create another csv file as output event_details.csv (contains all urls corresponding to its region with inital flag initialized as N)
2. Run event_details.py to fetch the final event details like event_name, date etc.

Note - this script is still in progress and will be updated in future. 

