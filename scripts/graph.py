#!/usr/bin/env python2

# was using /sw/bin/python2.7 -tt
# filter.py
# this file is the driver for the python analysis script

# system includes
import sys
import os
import getopt
import glob
#import xml.etree.ElementTree as ET
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import tostring
import numpy as np
import math

# local includes
from scanpath import Scanpath
from aoi import AOI
from lagrange import Lagrange

import plotter
import point
from point import Point

from scipy import spatial 

def usage():
  print "Usage: python graph.py " \
        " --width=? --height=? --screen=? --dist=?" \
        " --xtiles=? --ytiles=?\n" \
        " --indir=? --imgdir=? --outdir=? --pltdir=?" \
        " --file=?\n"\
        " --hertz=?\n"\
        " --sfdegree=? --sfcutoff=?\n"\
        " --dfdegree=? --dfwidth=?\n"\
        " --vt=?\n" \
        " --smooth=?\n"\
        "   width, height: screen dimensions (in pixels)\n" \
        "   screen: screen diagonal dimension (in inches)\n" \
        "   dist: viewing distance (in inches)\n" \
        "   xtiles: number of AOI tiles (in x direction)\n" \
        "   ytiles: number of AOI tiles (in y direction)\n" \
        "   indir: a directory containing input files to be processed\n" \
        "   imgdir: a directory containing image files\n" \
        "   outdir: a directory containing output files\n" \
        "   pltdir: a directory containing plot files\n" \
        "   file: a single file to process\n" \
        "   image: a single image to use as background\n" \
        "   hertz: the sampling rate of the data\n" \
        "   sfdegree: butterworth filter smoothing degree \n" \
        "   sfcutoff: butterworth filter smoothing cutoff \n" \
        "   dfwidth: savitzky-golay filter width \n" \
        "   vt: min velocity for change to be a saccade\n"\
        "   smooth: True enables butterworth smoothing\n"

def parseAOI(aoifile,aoilist):

  print "parsing: ", aoifile

  if(aoifile != None and os.path.isfile(aoifile)):
    tree = ET.parse(aoifile)
#   print "tree = %s" % tree
  else:
    return

  # should be something like Experiment, {}
  root = tree.getroot()
# print "root.tag = %s, root.attrib = %s" % (root.tag, root.attrib)

  # iterate through PAGEOBJECT objects, look for PTYPE=''6'
  print "PAGE INFO:"
  for obj in root.iter('MASTERPAGE'):
    px = obj.get('PAGEXPOS')
    py = obj.get('PAGEYPOS')
    pw = obj.get('PAGEWIDTH')
    ph = obj.get('PAGEHEIGHT')
    bl = obj.get('BORDERLEFT')
    br = obj.get('BORDERRIGHT')
    bt = obj.get('BORDERTOP')
    bb = obj.get('BORDERBOTTOM')
#   print "%s %s %s %s" % (px,py,pw,ph)
#   print "%s %s %s %s" % (bl,br,bt,bb)

  # iterate through PAGEOBJECT objects, look for PTYPE=''6'
  for obj in root.iter('PAGEOBJECT'):
    if obj.get('PTYPE') == '6':
      # x,y is the top-left corner
      x = obj.get('XPOS')
      y = obj.get('YPOS')
      w = obj.get('WIDTH')
      h = obj.get('HEIGHT')
      label = obj.get('ANNAME')
      print "%s: %s %s %s %s" % (label,x,y,w,h)

      # need to subtract the pagexpos and pageypos and need to add in height
      # to get bottom left corner
      fx = float(x) - float(px)
      fy = (float(y) - float(py)) + float(h)
      fw = float(w)
      fh = float(h)
      aoi = AOI(fx,fy,fw,fh)
      aoi.setAOILabel(label)
      aoi.dump()
#     if aoidict.has_key(stimulus):
#       aoidict[stimulus].append(aoi)
#     else:
#       aoidict[stimulus] = [aoi]
      aoilist.append(aoi)

      del aoi

def main(argv):
# if not len(argv):
#   usage()

  try:
    opts, args = getopt.getopt(argv, '', \
                 ['width=','height=',\
                  'hertz=',\
                  'screen=','dist=',\
                  'xtiles=','ytiles=',\
                  'indir=','imgdir=','outdir=','pltdir=',\
                  'file=','image=', 'hertz=', 'sfdegree=', 'sfcutoff=',\
                  'vt=', 'smooth='])
  except getopt.GetoptError, err:
    usage()
    exit()

  # Enable/disable butterworth smoothing.
  smooth = False
  # screen height in pixels
  width = 1680
  height = 1050
  # screen diagonal (in inches)
  screen = 22
  # viewing distance (in inches)
  dist = 22.44
  # sampling rate
  herz = 60.0
  # smoothing (Butterworth) filter parameters: degree, cutoff
  sfdegree = 2
# sfcutoff = 1.15 # more smooth
# sfcutoff = 1.65
# sfcutoff = 1.85
#  sfcutoff = 2.15 # last used
# sfcutoff = 2.35
# sfcutoff = 3.15
# sfcutoff = 4.15
  sfcutoff = 6.15 # less smooth
  # differentiation (SG) filter parameters: width, degree, order
  # 5, 3 for no smoothing, 3, 2 for smoothing
  if (smooth):
    dfwidth = 3
    dfdegree = 2
  else:
    dfwidth = 5
    dfdegree = 3
  dfo = 1
  # velocity threshold
# T = 5.0  # more fixations
# T = 18.0
# T = 20.0
# T = 25.0
  T = 30.0
# T = 35.0 # fewer fixations
# T = 40.0 # last used

  file = None
  # initially don't use an image (just plain white bgnd for plots)
  image = None

  # set up AOI grid
  xtiles = 4
  ytiles = 3

  outdir = "./data"
  pltdir = "./plots"

  # Checked beforehand so that custom parameters could still be used...
  # Check if smooth is an option. We will set default parameters based on 
  # value. If others are provided via the command line, we will use them.
  try:
      arg = opts[[t[0] for t in opts].index('--smooth')][1]
      if arg.lower() == 'true':
          smooth = True
      elif arg.lower() == 'false':
          smooth = False
      else:
          print "Warning, invalid smooth value. Assuming default."
      if (smooth):
        dfwidth = 3
        dfdegree = 2
      else:
        dfwidth = 5
        dfdegree = 3
  except Exception as e:
    print e
    sys.exit()
    pass

  dfwidth = 3
  dfdegree = 3

  for opt,arg in opts:
    opt = opt.lower()
    if(opt != '--file' and opt != '--image'):
      arg = arg.lower()

    if opt == '--indir':
      indir = arg
    elif opt == '--imgdir':
      imgdir = arg
    elif opt == '--outdir':
      outdir = arg
    elif opt == '--pltdir':
      pltdir = arg
    elif opt == '--width':
      width = arg
    elif opt == '--height':
      height = arg
    elif opt == '--screen':
      screen = float(arg)
    elif opt == '--dist':
      dist = float(arg)
    # elif opt == '--xtiles':
    #   xtiles = int(arg)
    # elif opt == '--ytiles':
    #   ytiles = int(arg)
    elif opt == '--file':
      file = arg
    elif opt == '--image':
      image = arg
    elif opt == '--hertz':
      herz = float(arg)
    elif opt == '--sfdegree':
      sfdegree = float(arg)
    elif opt == '--sfcutoff':
      sfcutoff = float(arg)
    elif opt == '--dfdegree':
      dfdegree = float(arg)
    elif opt == '--dfwidth':
      dfwidth = float(arg)
    elif opt == '--vt':
      T = float(arg)
    else:
      sys.argv[1:]

  # get .raw input files to process
  if os.path.isdir(indir):
    files = glob.glob('%s/*.raw' % (indir))

  # if user specified --file="..." then we use that as the only one to process
  if(file != None and os.path.isfile(file)):
    files = [file]

  # check to see if use specified image, if so, then don't compose filename
  # every time through loop; same image will be used (calibration image
  # presumably)...kind of a hack, but WTF...
  haveimage = False
  if(image != None and os.path.isdir(imgdir)):
    image = os.path.join(imgdir,image)
    haveimage = True

  lagrange = Lagrange(int(width),int(height))

  for file in files:
    # print(files)
    scanpath = Scanpath()
    scanpath.parseFile(file,width,height,herz)

    base = os.path.basename(file)

    print "Processing: ", file, "[", base, "]"

    subj, ext = os.path.splitext(base.split('_')[0])

    aoifile = "NONE"

    # extract stimulus name
    imagebase, ext = os.path.splitext(base.split('_')[1])
    if imagebase == 'calibration-verification-image':
      imagebase = "composite-grid-1680x1050"
      cond = 'calib-verif'
      aoifile = "calibration_verification.sla"
    elif imagebase == 'page1':
      imagebase = "page1-811x1050"
      cond = 'page1'
      aoifile = "consent_page1.sla"
    elif imagebase == 'page2':
      imagebase = "page2-811x1050"
      cond = 'page2'
      aoifile = "consent_page2.sla"
    elif imagebase == 'page3':
      imagebase = "page3-811x1050"
      cond = 'page3'
      aoifile = "consent_page3.sla"
    elif imagebase == 'page4':
      imagebase = "page4-811x1050"
      cond = 'penn-state'
    else:
      # if stimulus not in this list, not interested in this image (instruction page)
      imagebase = "NONE"
      cond = "NONE"
      aoifile = "NONE"

    if(aoifile == "NONE"):
      continue
    
    print "Image: ", image, "[", imagebase, "]"

    aoidir = "../src/scribus-AOIs/"

    aoifilepath = aoidir + aoifile

    print "aoifile = ", aoifilepath

    aoidict = {}
    aoilist = []

    parseAOI(aoifilepath,aoilist)

#   print aoidict
#   for key in aoidict:
#     print key
#     print "number of AOIs: ",len(aoidict[key])
#     for aoi in aoidict[key]:
#       aoi.dump()


    print "subj, cond: ", subj, cond

    # create filename of corresponding image
    if(haveimage == True):
      print "Image: ", image
    else:
      image = '{0}.jpg'.format(os.path.join(imgdir,imagebase))
      print "Image: ", image, "[", imagebase, "]"

    # split filename from extension
    filename, ext = os.path.splitext(base)

    scanpath.smooth("%s/%s-smth%s" % (outdir,filename,".dat"),\
                    width,height,herz,sfdegree,sfcutoff, smooth)
    scanpath.differentiate("%s/%s-diff%s" % (outdir,filename,".dat"),\
                            width,height,screen,dist,herz,dfwidth,dfdegree,dfo)
    scanpath.threshold("%s/%s-fxtn%s" % (outdir,filename,".dat"),\
                            width,height,T)
    scanpath.amfoc("%s/%s-amfo%s" % (outdir,filename,".dat"),\
                            width,height)
    scanpath.gridify("%s/%s-aois%s" % (outdir,filename,".csv"),\
                            subj,cond,width,height,xtiles,ytiles)

    scanpath.dumpDAT("%s/%s%s" % (outdir,filename,".dat"),width,height)

    scanpath.dumpFixatedAOIs("%s/%s-fxtn-aoi%s" % (outdir,filename,".csv"),\
                        width,height,\
                        aoilist)

    scanpath.ann("%s/%s-ann%s" % (outdir,filename,".csv"),\
                        subj,cond, imagebase,width,height)
#   scanpath.dumpXML("%s/%s%s" % (outdir,filename,".xml"),width,height)

#   plotter.renderPoints1D("%s/%s-%s" % (pltdir,filename,"gzpt"),\
#                          width,height,\
#                          scanpath.gazepoints,'x',\
#                          "Gaze point data")

#   plotter.renderPoints1D("%s/%s-%s" % (pltdir,filename,"gzpt"),\
#                          width,height,\
#                          scanpath.gazepoints,'y',\
#                          "Gaze point data")

    plotter.renderPoints2D("%s/%s-%s" % (pltdir,filename,"gzpt"),\
                           width,height,\
                           scanpath.gazepoints,\
                           "Gaze point data",\
                           image,True,\
                           xtiles,ytiles)

#   plotter.renderPoints1D("%s/%s-%s" % (pltdir,filename,"smth"),\
#                          width,height,\
#                          scanpath.smthpoints,'x',\
#                          "Smoothed gaze point data")

#   plotter.renderPoints1D("%s/%s-%s" % (pltdir,filename,"smth"),\
#                          width,height,\
#                          scanpath.smthpoints,'y',\
#                          "Smoothed gaze point data")

#   plotter.renderPoints2D("%s/%s-%s" % (pltdir,filename,"smth"),\
#                          width,height,\
#                          scanpath.smthpoints,\
#                          "Smoothed gaze point data",
#                          image,True,\
#                          xtiles,ytiles)

#   plotter.renderPoints1D("%s/%s-%s" % (pltdir,filename,"dfft"),\
#                         width,height,\
#                         scanpath.velocity,'x',\
#                         "Differentiated gaze point data",False)

#   plotter.renderPoints1D("%s/%s-%s" % (pltdir, filename, "accel"), \
#                          width, height, \
#                          scanpath.acceleration, 'x',\
#                          "Twice Differentiated gaze point data", False)
    
#    plotter.renderPoints1D("%s/%s-%s" % (pltdir,filename,"dfft"),\
#                          width,height,\
#                          scanpath.velocity,'y',\
#                          "Differentiated gaze point data",False)

#   plotter.renderPoints2D("%s/%s-%s" % (pltdir,filename,"dfft"),\
#                          width,height,\
#                          scanpath.velocity,\
#                          "Differentiated gaze point data",\
#                          None,False,\
#                          xtiles,ytiles)

    plotter.renderFixations("%s/%s-%s" % (pltdir,filename,"fxtn"),\
                            width,height,\
                            screen,dist,\
                            scanpath.fixations,\
                            "Fixations",\
                            image,\
                            lagrange,\
                            xtiles,ytiles)

    plotter.renderAOIs("%s/%s-%s" % (pltdir,filename,"aois"),\
                            width,height,\
                            aoilist,\
                            imagebase,\
                            "AOIs",\
                            image,\
                            xtiles,ytiles)

#   plotter.renderAOIFixations("%s/%s-%s" % (pltdir,filename,"aoi-fxtn"),\
#                           width,height,\
#                           scanpath.fixations,\
#                           aoidict,\
#                           imagebase,\
#                           "AOI Fixations",\
#                           image,\
#                           xtiles,ytiles)

    plotter.renderFixatedAOIs("%s/%s-%s" % (pltdir,filename,"fxtn-aoi"),\
                            width,height,\
                            scanpath.fixations,\
                            aoilist,\
                            imagebase,\
                            "AOI Fixations",\
                            image,\
                            xtiles,ytiles)

    plotter.renderAmfocFixations("%s/%s-%s" % (pltdir,filename,"affx"),\
                            width,height,\
                            scanpath.fixations,\
                            scanpath.K,\
                            "Ambient/Focal Fixations",\
                            image,\
                            xtiles,ytiles)

#   plotter.renderCalibFixations("%s/%s-%s" % (pltdir,filename,"clbf"),\
#                           width,height,\
#                           screen,dist,\
#                           scanpath.fixations,\
#                           "Mean Error and Fit of Fixated Calibration Locations",\
#                           image,\
#                           lagrange,\
#                           xtiles,ytiles)

#   plotter.renderHeatmap("%s/%s-%s" % (pltdir,filename,"heat"),\
#                           width,height,\
#                           scanpath.fixations,\
#                           "Heatmap",\
#                           image,\
#                           xtiles,ytiles)

    print " "
    del scanpath

if __name__ == "__main__":
  main(sys.argv[1:])
