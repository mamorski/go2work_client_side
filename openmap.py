import os
import sys
# google response to wrong address
# {
#    "results" : [],
#    "status" : "ZERO_RESULTS"
# }
def openmap(route):
    key = 'AIzaSyDMIxx6GqU9oBiIop9DU3rpHPWIVg5-GP4'
    # google_url = 'https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&key=' + key
    url = 'https://www.google.com/maps/dir/?api=1&origin=Paris,' \
          'France&destination=Cherbourg,France&travelmode=driving&waypoints=Versailles,' \
          'France%7CChartres,France%7CLe+Mans,France%7CCaen,France'
    if sys.platform=='win32':
        os.startfile(url)
    elif sys.platform =='darwin':
        subprocess.Popen(['open', url])
    else:
        try:
            subprocess.Popen(['xdg-open', url])
        except OSError:
            print('Please open a browser on: ' + url)