#! /usr/bin/env python

import os
import shutil
import sys
import argparse
from string import *
from math import *

"""
Takes five column file with feature midpoints:
  1) chr
  2) midpoint
  3) name
  4) score
  5) strand

Generates given number of windows of given size around mid point
"""

def main(argv):
  parser = argparse.ArgumentParser(description="Takes five column file with:\n\t chr \n" + 
                                   "\t position \n\t name \n\t score \n\t strand \n" + 
                                   "Generates file with windows of given size around each position")
  parser.add_argument("-i", required=True, dest='input')
  parser.add_argument("-w", required=True, dest='window')
  parser.add_argument("-f", required=True, dest='flanks', help="Number of windows on each side of point")
  args = parser.parse_args()
  infile = open(args.input, 'r')
  outfile = open(args.input + "_W" + args.window + "F" + args.flanks, 'w')
  window = atoi(args.window)
  flanks = atoi(args.flanks)
  genome_sizes = open('/seq/lib/mouse.mm9.genome', 'r')

  d = {}
  for line in genome_sizes:
      line = line.strip()
      sline = line.split()
      if len(sline) > 0:
          d[sline[0]]=sline[1]

  for line in infile:
      sline = line.strip().split();
      strand = sline[4]
      start = 0
      if strand == "+":
          start = atoi(sline[1]) - flanks * window + 1
      else: 
          end = atoi(sline[1]) + flanks * window + 1

      for index in xrange(2*flanks):
          out = ""
          if strand == "+":
              end = start + window - 1
              out = (sline[0] + "\t" + str(start) + "\t" + str(end) + "\t" + \
                    sline[2] + "\t" + str(index) + "\t" + sline[4] + "\n")
              start = end + 1
          else:
              start = end - window + 1
              out = sline[0] + "\t" + str(start) + "\t" + str(end) + "\t" + \
                    sline[2] + "\t" + str(index) + "\t" + sline[4] + "\n"
              end = start - 1
          if (start and end >= 0) and (start and end <= atoi(d[sline[0]])):
              outfile.write(out)
  outfile.close()

if __name__ == "__main__":
    main(sys.argv)
