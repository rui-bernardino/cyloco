#!/usr/bin/python3
# Concatenate agent logs, sorted by date/time.


import glob,sys,re
from datetime import datetime
from pathlib import Path

# parse the many date/time formats in the logs...
def getdate(line):
    # regexes vs datetime formats
    dateformats= {
        '^(\w+ \d+, \d+\. \d+:\d+:\d+ \w+)'     :   '%B %d, %Y. %I:%M:%S %p',
        '^(\d+/\d+/\d+ \d+:\d+:\d+):'           :   '%d/%m/%Y %H:%M:%S',
        '^(\d+/\d+/\d+ \d+:\d+:\d+ [AP]M)'      :   '%m/%d/%Y %H:%M:%S %p'
    }
    utc_time=datetime.max
    for f in dateformats:
        s=re.search(f,line)
        if s :
            readdate=s.group(1)
            try:
                utc_time = datetime.strptime(readdate, dateformats[f])
                return utc_time
            except ValueError as e:
                # we should never really reach this as the regex will fail before strptime()
                print(readdate)
                print(line)
                print(e)
                sys.exit("Couldn't figure out date... :(")
    return 0


# args: list of files or *.txt in current directory
filelist=[]
if len(sys.argv) == 1:
    filelist=glob.glob("*.txt")
    filelist+=glob.glob("*.log")
else:
    for input in sys.argv[1:]:
        filelist+=glob.glob(input)

# determine the longest stem'ed filename, for "pretty" printing..
stemedfilename={}
maxfilenamelen=0
for filename in filelist:
    stemedfilename[filename]=Path(filename).stem
    if len(stemedfilename[filename])>maxfilenamelen:
        maxfilenamelen=len(stemedfilename[filename])



# read all logs into a time indexed dictionary
fulltext={}
for filename in filelist:
    f = open(filename,"r")
    text=f.read()
    f.close
    # split lines and append each to the dict
    for line in text.splitlines(): 
        
        utc_time=getdate(line)
        if utc_time:
            lasttime=utc_time
            # format if line starts with parseable date
            outputline="%-*s| %s\n" % (maxfilenamelen+1,stemedfilename[filename], line)
        else:
            # if "line" is part of a multi-line entry; or date unparseable...
            outputline="%-*s|               %s\n" % (maxfilenamelen+1,stemedfilename[filename], line)
            utc_time=lasttime
        
        try:
            fulltext[utc_time]+=outputline
        except KeyError:
            fulltext[utc_time]=outputline
        
for k in sorted(fulltext.keys()):
    # print("%s - %s" % (k, fulltext[k]))
    print(fulltext[k],end='')
