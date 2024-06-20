#!/usr/bin/env python

import sys, os, math

class Header:
  subj         = 0
  cond         = 1
  stim         = 2
  NNI          = 3
  ANN          = 4

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
    stim      = entry[Header.stim]
    NNI       = entry[Header.NNI]
    ANN       = entry[Header.ANN]

    # dump out line excluding "trial"
    str = "%s,%s,%s,%s,%s" % (subj,cond,stim,NNI,ANN)
    print >> df,str
    ct += 1

  return ct

###############################################################################

# clear out output file
df = open("anns.csv",'w')
print >> df,"subj,cond,stim,nni,ann"

dir = './data/'

# find all files in dir with .csv extension
lst = filter(lambda a: a.endswith('-ann.csv'),os.listdir(dir))

lineno = 1

for item in lst:

  file = dir + item
  print 'Processing ', file

  # cat csv files into one
  lineno = catCSVFile(file,df,lineno)

df.close()
