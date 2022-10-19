"""Use Ticketmaster API to get local events using list of bands."""

import webbrowser
import urllib.parse
import requests

HOME_CURRENCY = 'GBP'

def get_api_key():
    """Get Ticketmaster API key from ticketmaster_key. Get your own!"""
    with open('ticketmaster_key', 'r', encoding='utf-8') as file:
        return file.read()

API_KEY = get_api_key()
TICKETMASTER_URL = f'https://app.ticketmaster.com/discovery/v2/events.json?apikey={API_KEY}'

def get_bands():
    """Get bands from band_list.txt, one band per line."""
    with open('band_list.txt', 'r', encoding='utf-8') as file:
        return file.read().split('\n')

def get_band_events(band):
    """Call the Ticketmaster API and get a list of results from a search."""
    return requests.get(f'{TICKETMASTER_URL}&keyword={band}').json()

def check_band_events(events, band):
    """Check that a given event is in the home currency, indicating it's local."""
    valid_events = []
    if '_embedded' in events:
        for event in events['_embedded']['events']:
            try:
                if event['priceRanges'][0]['currency'] == HOME_CURRENCY and \
                    band_present(event, band):
                    valid_events.append(event['url'])
            except KeyError:
                pass
    return valid_events

def band_present(event, band):
    """Check that a band is actually attending, since the event name is not a sure indicator."""
    for attendee in event['_embedded']['attractions']:
        if band.lower() == attendee['name'].lower():  # Sometimes returns false positives?
            return True
    return False

def open_events(urls):
    """If the user chooses, open the output results in a browser. One tab per URL."""
    webbrowser.open_new('localhost')  # If possible, try and open a new window first for management
    for url in urls:
        webbrowser.open(url, new=0, autoraise=False)

def main():
    """Main function."""
    browser_open_choice = input('Open results in browser? (Y/N)\n\
This may lag your browser or computer if you have a lot of bands or results!\n').upper()
    all_valid_events = []
    bands = get_bands()

    for band in bands:
        encoded_band = urllib.parse.quote(band)
        band_events = get_band_events(encoded_band)
        all_valid_events += check_band_events(band_events, band)

    all_valid_events = sorted(set(all_valid_events))

    if browser_open_choice == 'Y':
        open_events(all_valid_events)
    else:
        for url in all_valid_events:
            print(url)

main()
