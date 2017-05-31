#!/usr/bin/python
#Based on the original script by https://gist.github.com/michelwilhelm/8de35523570c82eabfdb
import os
import sys
import csv
import datetime
import time
import twitter

def test():

        #run speedtest-cli
        print 'running test'
        a = os.popen("python /root/speedtest-cli --simple").read()
        print 'ran'
        #split the 3 line result (ping,down,up)
        lines = a.split('\n')
        print a
        ts = time.time()
        date =datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        tm = time.strftime('%H%M%S')
        #if speedtest could not connect set the speeds to 0
        if "Cannot" in a:
                p = 100
                d = 0
                u = 0
        #extract the values for ping down and up values
        else:
                p = lines[0][6:11]
                d = lines[1][10:14]
                u = lines[2][8:12]
        print date,p, d, u
        #save the data to file for local network plotting
        out_file = open('/root/data.csv', 'a')
        writer = csv.writer(out_file)
        writer.writerow((ts*1000,p,d,u))
        out_file.close()

        #connect to twitter
        CON_SEC="xxxx"
        CON_SEC_KEY="xxxx"
        TOKEN="xxxx"
        TOKEN_KEY="xxxx"
        my_auth = twitter.OAuth(TOKEN,TOKEN_KEY,CON_SEC,CON_SEC_KEY)
        twit = twitter.Twitter(auth=my_auth)

        #try to tweet if speedtest couldnt even connet. Probably wont work if the internet is down
        if "Cannot" in a:
                try:
                        tweet="Hey @virginmedia looks like my connection is flaky in area 25. Problems? #virginoutage #VirginMedia"
                        twit.statuses.update(status=tweet)
                except:
                        pass

        # tweet if down speed is less than whatever I set
        elif eval(d)<150:
                print "trying to tweet"
                try:
                        # i know there must be a better way than to do (str(int(eval())))
                        tweet="I pay #VirginMedia for 200mbps #broadband but am currently only getting " + str(int(eval(d))) + "mbps. #speedtestcli #speedtest #bad #poorservice #area25 #" + tm
                        twit.statuses.update(status=tweet)
                except Exception,e:
                        print str(e)
                        pass
        return

if __name__ == '__main__':
        test()
        print 'completed'
