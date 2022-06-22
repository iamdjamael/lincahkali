from datetime import datetime
import time
import os
import getpass
import telnetlib
#import apscheduler

from apscheduler.schedulers.background import BackgroundScheduler


def telnet():
    HOST = "192.168.100.100"
    usr = "admin"
    pwd = "admin"

    tn = telnetlib.Telnet(HOST)

    tn.read_until(b"Username: ")
    tn.write(usr.encode('ascii') + b"\n")
    tn.read_until(b"Password: ") #input by typing
    tn.write(pwd.encode('ascii') + b"\n")

    tn.write(b"enable\n")
    #tn.write(b"cisco\n")
    tn.write(b"conf t\n")
    tn.write(b"int gig 0/1\n")
    tn.write(b"ip add 210.0.0.2 255.255.255.0\n")
    tn.write(b"shutdown\n")
    tn.write(b"no shutdown\n")
    tn.write(b"end\n")
    tn.write(b"exit\n")
    #tn.close

    print(tn.read_all().decode('ascii'))


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(telnet, 'interval', seconds=5)
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()
