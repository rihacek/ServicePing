import subprocess, os, re, json, urllib.request, secrets
from datetime import datetime
import requests #todo: ditch urllib stuff

#call web page to get system info:
# get these into config, dummy. url = "http://127.0.0.1:5000" #debugging
url = "https://uptime.rihaceks.com"
pingString = url + "/ping/list/" + secrets.pinglist
webCall = urllib.request.urlopen(pingString)
listData = webCall.read()
encoding = webCall.info().get_content_charset('utf-8')
jsonList = json.loads(listData.decode(encoding))

pingParam = '-n' if os.name == 'nt' else '-c' #account for different ping parameters in Windows/Linux

for system in jsonList["systems"]:

    thisSystem = system["systemID"]
    thisTime = datetime.now() 
    try:
        res = subprocess.check_output(['ping', pingParam, '1', system["address"]])
        failures = ['Received = 0', 'TTL expired in transit', 'host unreachable']
        if any(x in res.decode('utf-8') for x in failures):
            thisStatus = '2'
            thisDuration = 0
        else:
            #windows ping: ms = re.search('Average = (.*)ms', res.decode('utf-8'))            
            ms = re.search('time (.*)ms', res.decode('utf-8'))   
            thisStatus = '1'   #LOCAL: 5=ok, 6=fail: this is a mess
            thisDuration = ms.group(1)
        
    except subprocess.CalledProcessError as e:        
        thisStatus = '2'
        thisDuration = 0

    payload = { 'pw' : secrets.pinglist,
                'st' : thisStatus,
                'time' : thisTime,
                'dur' : thisDuration } 
    
    postURL = url + "/responses/" + str(thisSystem)
    res = requests.post(postURL, data=payload)