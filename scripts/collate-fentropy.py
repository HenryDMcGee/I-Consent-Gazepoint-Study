#!/usr/bin/env python

import sys, os, math

class Header:
  subj         = 0
  cond         = 1
  stim         = 2
  entropy      = 3
  spectral     = 4
  uncertainty  = 5

def catCSVFile(infile,df):
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
    subj         = entry[Header.subj]
    cond         = entry[Header.cond]
    stim         = entry[Header.stim]
    entropy      = entry[Header.entropy]
    spectral     = entry[Header.spectral]
    uncertainty  = entry[Header.uncertainty]

    # dump out line
    str = "%s,%s,%s,%s,%s,%s" % (subj,cond,stim,entropy,spectral,uncertainty)
    print >> df,str

###############################################################################

# clear out output file
df = open("fentropy.csv",'w')
print >> df,"subj,cond,stim,entropy,spectral_entropy,uncertainty"

dir = './data/'

# find all files in dir with .csv extension
lst = filter(lambda a: a.endswith('-entropy.csv'),os.listdir(dir))

for item in lst:

  file = dir + item
  print 'Processing ', file

  # cat csv files into one
  catCSVFile(file,df)

df.close()
