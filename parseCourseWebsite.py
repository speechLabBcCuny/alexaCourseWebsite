#!/usr/bin/python

import cisc1600status

import datetime

def main():
    now = datetime.datetime.now()
    
    print "Default time"
    print cisc1600status.parseCisc1600Page()
    print
    print "Now"
    print cisc1600status.parseCisc1600Page(now)
    print
    print "1 day from now"
    print cisc1600status.parseCisc1600Page(now + datetime.timedelta(days=1))
    print
    print "5 days from now"
    print cisc1600status.parseCisc1600Page(now + datetime.timedelta(days=5))
    
    

if __name__ == '__main__':
    main()
    
