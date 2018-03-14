import os
import sys
import re
# google response to wrong address
# {
#    "results" : [],
#    "status" : "ZERO_RESULTS"
# }
def openmap(route, index):
    # print(route[0])
    print(index)
    # print(route[1])
    print(route[index])
    url = 'https://www.google.com/maps/dir/?api=1&'
    length = len(route)
    if len == 1:
        str = re.sub(r'\s+', '+', route[index][0])
        url += 'origin=' + str + '&destination=Ort+Braude+College&travelmode=driving'
    else:
        i = 0
        for var in route[index]:
            str = re.sub(r'\s+', '+', var)
            if i == 0:
                url += 'origin=' + str + '&destination=Ort+Braude+College&travelmode=driving&waypoints='
            elif i != length-1:
                url += str + '%7C'
            else:
                url += str
            i += 1

    # key = 'AIzaSyDMIxx6GqU9oBiIop9DU3rpHPWIVg5-GP4'
    # google_url = 'https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&key=' + key
    # url = 'https://www.google.com/maps/dir/?api=1&origin=Paris,' \
    #       'France&destination=Cherbourg,France&travelmode=driving&waypoints=Versailles,' \
    #       'France%7CChartres,France%7CLe+Mans,France%7CCaen,France'
    print(url)
    if sys.platform=='win32':
        os.startfile(url)
    elif sys.platform =='darwin':
        subprocess.Popen(['open', url])
    else:
        try:
            subprocess.Popen(['xdg-open', url])
        except OSError:
            print('Please open a browser on: ' + url)