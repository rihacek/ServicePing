import subprocess, os, re, json, urllib.request, secrets
from datetime import datetime
import requests #todo: ditch urllib stuff

#call web page to get system info:
url = "https://uptime.rihaceks.com"
pingString = url + "/ping/list/" + secrets.pinglist
webCall = urllib.request.urlopen(pingString)
listData = webCall.read()
encoding = webCall.info().get_content_charset('utf-8')
jsonList = json.loads(listData.decode(encoding))

pingParam = '-n' if os.name == 'nt' else '-c' #account for different ping parameters in Windows/Linux

for system in jsonList["systems"]:

    thisSystem = system["systemID"]
    thisTime = datetime.now() #might have to format this later
    try:
        res = subprocess.check_output(['ping', pingParam, '1', system["address"]])
        failures = ['Received = 0', 'TTL expired in transit', 'host unreachable']
        if any(x in res.decode('utf-8') for x in failures):
            print(system["systemName"] + ": todo - log this error.")
            thisStatus = '6'
            thisDuration = 0
        else:
            ms = re.search('Average = (.*)ms', res.decode('utf-8'))
            print(system["systemName"] + ": " + ms.group(1) + "ms")
            
            thisStatus = '5'   #5=ok, 6=fail:static is fine for now
            thisDuration = ms.group(1)
        
    except subprocess.CalledProcessError as e:        
        print(system["systemName"] + ": todo - log this error.")
        thisStatus = '6'
        thisDuration = 0

    payload = { 'pw' : secrets.pinglist,
                'st' : thisStatus,
                'time' : thisTime,
                'dur' : thisDuration } 
    url = "http://127.0.0.1:5000" #debugging
    postURL = url + "/responses/" + str(thisSystem)
    res = requests.post(postURL, data=payload)
    
    print(res.text)
    print('* * * * * *')