
import subprocess, time, socket
from subprocess import check_output

class os_utilities():

    def scan_networks():
        print('scanning for wifi networks')
        scanoutput = check_output(["iwlist", "wlan0", "scan"])
        list = ""
        for line in scanoutput.split():
            if line.startswith("ESSID"):
                line=line[7:-1]
                list += line
                print line
        return list

    def reboot():
        print('rebooting')
        subprocess.call("sync")
        subprocess.call(["reboot", "-h", "now"])
