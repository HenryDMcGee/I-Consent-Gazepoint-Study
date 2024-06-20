#!/usr/bin/env python

import sys, os, math

#subj,cond,AOI,duration,order
class Header:
  subj         = 0
  cond         = 1
  AOI          = 2
  duration     = 3
  order        = 4

def catCSVFile(infile,df,ct):
  try:
    f = open(infile,'r')
  except IOError:
    print "Can't open file: " + infile
    return

  # read lines, throwing away first one (header)
# linelist = f.readlines()
# linelist = f.read().split('\r')
  linelist = f.read().splitlines()
  linelist = linelist[1:]

  for line in linelist:
    entry = line.split(',')

    # init subj
    subj      = entry[Header.subj]
    cond      = entry[Header.cond]
    AOI       = entry[Header.AOI]
    duration  = entry[Header.duration]

    # dump out line excluding "trial"
    str = "%s,%s,%s,%s,%s" % (subj,cond,AOI,duration,ct)
    print >> df,str
    ct += 1

  return ct

###############################################################################

# clear out output file
df = open("aois.csv",'w')
print >> df,"subj,cond,AOI,duration,order"

dir = './data/'

# find all files in dir with .csv extension
lst = filter(lambda a: a.endswith('-aois.csv'),os.listdir(dir))

lineno = 1

for item in lst:

  file = dir + item
  print 'Processing ', file

  # cat csv files into one
  lineno = catCSVFile(file,df,lineno)

df.close()
