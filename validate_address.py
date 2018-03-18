import json
import time
from urllib.request import urlopen
import re

# get address and check it with Google API if the address is valid
def validate_address(address):

    if re.search(r'israel', address, re.I):
        my_address = re.sub(r'\s+', '+', address)
    else:
        my_address = 'israel+' + address
        my_address = re.sub(r'\s+', '+', my_address)

    maps_key = 'AIzaSyDMIxx6GqU9oBiIop9DU3rpHPWIVg5-GP4'
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + my_address + '&key=' + maps_key
    current_delay = 0.1  # Set the initial retry delay to 100ms.
    max_delay = 2  # Set the maximum retry delay to 1 hour.

    while True:
        try:
            # Get the API response.
            response = urlopen(url).read()
        except IOError:
            pass  # Fall through to the retry loop.
        else:
            # If we didn't get an IOError then parse the result.
            result = json.loads(response)
            print(result['status'])
            if result['status'] == 'OK':
                return True
            elif result['status'] != 'UNKNOWN_ERROR':
                # Many API errors cannot be fixed by a retry, e.g. INVALID_REQUEST or
                # ZERO_RESULTS. There is no point retrying these requests.
                raise Exception(result['error_message'])

        if current_delay > max_delay:
            raise Exception('Too many retry attempts.')
        print('Waiting', current_delay, 'seconds before retrying.')
        time.sleep(current_delay)
        current_delay *= 2  # Increase the delay each time we retry.
