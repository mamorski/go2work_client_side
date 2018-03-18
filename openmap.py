import os
import sys
import re

# get route and open it on Google Maps in default browser
def openmap(route, index):
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

    if sys.platform=='win32':
        os.startfile(url)
    elif sys.platform =='darwin':
        subprocess.Popen(['open', url])
    else:
        try:
            subprocess.Popen(['xdg-open', url])
        except OSError:
            print('Please open a browser on: ' + url)