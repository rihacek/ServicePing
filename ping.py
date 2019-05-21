import subprocess
import secrets

for ping in range(1,3):
    address = "127.0.0." + str(ping)
    res = subprocess.call(['ping', address])
    if res == 0:
        print("ping to", address, "OK")
    elif res == 2:
        print("no response from", address)
    else:
        print("ping to", address, "failed!")

