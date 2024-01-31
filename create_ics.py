from ics import Calendar, Event
from pyScraper import scrape_events, url  # Assuming scrape_events and URL are defined in pyScraper.py
from datetime import datetime


def create_event_calendar(events):
    cal = Calendar()
    for event_name, event_date in events:
        # Create an Event
        event = Event()
        event.name = event_name

        # Handle events with date ranges
        if ',' in event_date:  # If there's a comma, it's a date range
            dates = event_date.split(', ')
            start_date = datetime.strptime(dates[0], '%d.%m.%Y')
            # Add one day to the end date for inclusivity
            end_date = datetime.strptime(dates[1], '%d.%m.%Y')
            event.end = end_date
        else:
            start_date = datetime.strptime(event_date, '%d.%m.%Y')
            # For a single day event, start and end dates are the same
            event.end = start_date

        event.begin = start_date
        cal.events.add(event)
    
#    with open('events_calendar.ics', 'w') as my_file:
#        my_file.writelines(cal)
    return cal.serialize()

def save_events_to_ics_file(events, file_path):
    event_tuples = [(name_date.split(' - ')[0], name_date.split(' - ')[1]) for name_date in events]
    ics_content = create_event_calendar(event_tuples)
    with open(file_path, 'w') as f:
        f.write(ics_content)

# Scrape events
events = scrape_events(url)

# Create a list of tuples (event_name, event_date)
event_tuples = []
for event in events:
    name_date = event.split(' - ')
    if len(name_date) == 2:
        event_tuples.append((name_date[0], name_date[1]))

create_event_calendar(event_tuples)
