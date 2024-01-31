import requests
from bs4 import BeautifulSoup
import html
import re
from datetime import datetime, timedelta

def scrape_events_within_days(url, days=None):
    events = scrape_events(url)
    if days is not None:
        filtered_events = []
        today = datetime.now()
        for event in events:
            name_date = event.split(' - ')
            if len(name_date) == 2:
                event_date = datetime.strptime(name_date[1].split(',')[0], '%d.%m.%Y')
                if event_date <= today + timedelta(days=days):
                    filtered_events.append(event)
        return filtered_events
    else:
        return events

def scrape_events(url, days=None):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    event_blocks = soup.find_all('div', class_='event-list-item__details')

    event_list = []
    for block in event_blocks:
        # Extract event name
        title_tag = block.find('h2', class_='event-details__title')
        if title_tag and title_tag.a:
            event_name = html.unescape(title_tag.get_text(strip=True))
        else:
            event_name = "No title"

        # Find the parent of the current block to get the date
        parent_block = block.find_parent('div', class_='event-list-item')
        if parent_block:
            meta_tag = parent_block.find('div', class_='event-details__meta')
            if meta_tag:
                # Extract all dates
                date_text = meta_tag.get_text(strip=True).replace('&ndash;', '-')
                all_dates = re.findall(r'\d{1,2}\.\d{1,2}\.\d{4}', date_text)

                if all_dates:
                    event_date = ', '.join(all_dates)
                else:
                    event_date = "No date"
            else:
                event_date = "No date"
        else:
            event_date = "No date"

        event_list.append(f"{event_name} - {event_date}")

    # Filter events if a specific number of days is given
    if days is not None:
        today = datetime.now()
        filtered_event_list = []
        for event in event_list:
            name, date_str = event.split(' - ', 1)  # Split the event string into name and date
            # Extract the first date for comparison
            first_date_str = date_str.split(',')[0]
            try:
                event_date = datetime.strptime(first_date_str, '%d.%m.%Y')
                if event_date <= today + timedelta(days=days):
                    filtered_event_list.append(event)
            except ValueError:
                # Handle any date parsing errors (e.g., "No date")
                pass
        return filtered_event_list

    return event_list


# URL of the webpage to scrape
url = 'https://www.paviljonki.fi/tapahtumat-liput/'
events = scrape_events(url)
#for event in events:
#    print(event)
