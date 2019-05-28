import subprocess, os, re, json, urllib.request, secrets

#call web page to get system info:
urlString = "https://uptime.rihaceks.com/ping/list/" + secrets.pinglist
webCall = urllib.request.urlopen(urlString)
listData = webCall.read()
encoding = webCall.info().get_content_charset('utf-8')
jsonList = json.loads(listData.decode(encoding))

#temporary for debugging off network:
#jsonList = json.loads('{"systems":[{"address":"127.0.0.42","description":"Local whatever on ESXI","parent":4,"pingtype":"PING","systemID":4,"systemName":"ESXi"},{"address":"127.0.0.10","description":"Local movie-streaming service","parent":4,"pingtype":"PING","systemID":5,"systemName":"Plex"}]}')

#"ping" each system in the response
pingParam = '-n' if os.name == 'nt' else '-c' #account for different ping parameters in Windows/Linux
for system in jsonList["systems"]:
    try:
        res = subprocess.check_output(['ping', pingParam, '1', system["address"]])
        #ms = re.search('Average = (.*)ms', res.decode('utf-8'))
        #print(system["systemName"] + ": " + ms.group(1) + "ms")
        failures = ['Received = 0','TTL expired in transit']
        if any(x in res.decode('utf-8') for x in failures):
            #do failed ping stuff
            print(system["systemName"],"failed ping:",system["address"])
        else:
            #do successful ping stuff
            ms = re.search('Average = (.*)ms', res.decode('utf-8'))
            print(system["systemName"] + ": " + ms.group(1) + "ms")

        #upload the data via POST

    except subprocess.CalledProcessError as e:
        #do error logging stuff
        print(system["systemName"] + ": todo - log this error.")



print("****************************************************") #debug separator
'''
for service in ["www.google.com","127.0.0.2"]:
    try:
        res = subprocess.check_output(['ping', pingParam, '1', service])
        ms = re.search('Average = (.*)ms', res.decode('utf-8'))
        print(service + ": " + ms.group(1) + "ms")
    except subprocess.CalledProcessError as e:
        #do failed ping stuff
        print(service + ": No response.")
'''

