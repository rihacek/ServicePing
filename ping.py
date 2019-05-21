import subprocess
import os
import re
from secrets import MySQL
import pymysql

pingParam = '-n' if os.name == 'nt' else '-c'

#call web page to get system info:
#systemid, method (ping, http), address
#"ping" each of them
#upload the responses via web page

for service in ["www.google.com","127.0.0.2"]:
    try:
        res = subprocess.check_output(['ping', pingParam, '1', service])
        ms = re.search('Average = (.*)ms', res.decode('utf-8'))
        print(service + ": " + ms.group(1) + "ms")
    except subprocess.CalledProcessError as e:
        #do failed ping stuff
        print(service + ": No response.")


