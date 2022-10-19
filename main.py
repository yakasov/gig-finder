"""Use Ticketmaster API to get local events using list of bands."""

import urllib.parse
import requests

HOME_CURRENCY = 'GBP'

def get_api_key():
    """Get Ticketmaster API key from ticketmaster_key. Get your own!"""
    with open('ticketmaster_key', 'r', encoding='utf-8') as f:
        return f.read()

API_KEY = get_api_key()
TICKETMASTER_URL = f'https://app.ticketmaster.com/discovery/v2/events.json?apikey={API_KEY}'

def get_bands():
    """Get bands from band_list.txt, one band per line."""
    with open('band_list.txt', 'r', encoding='utf-8') as f:
        return f.read().split('\n')

def get_band_events(band):
    """Call the Ticketmaster API and get a list of results from a search."""
    return requests.get(f'{TICKETMASTER_URL}&keyword={band}').json()

def check_band_events(events):
    """Check that a given event is in the home currency, indicating it's local."""
    valid_events = []
    if '_embedded' in events:      
        for event in events['_embedded']['events']:
            try:
                if event['priceRanges'][0]['currency'] == HOME_CURRENCY:
                    valid_events.append(event['url'])
            except KeyError:
                pass
    return valid_events

def main():
    """Main function."""
    for band in get_bands():
        encoded_band = urllib.parse.quote(band)
        band_events = get_band_events(encoded_band)
        print(check_band_events(band_events))

main()
