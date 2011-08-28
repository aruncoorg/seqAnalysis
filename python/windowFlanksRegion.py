#!/usr/bin/env python

import os
import shutil
import sys
from string import *
from math import *
import argparse
import operator

"""
Three sets of intervals of length opt.window:
        opt.flank times upstream and downstream
        gene body divided into opt.number equally spaced windows of length opt.window
        rounded to match DipData indexing
"""

def main(argv):

  parser = argparse.ArgumentParser()

  parser.add_argument("-i", "--input", action="store", dest="input", metavar="<str>")
  parser.add_argument("-o", "--ouput", action="store", dest="output", metavar="<str>")
  parser.add_argument("-f", action="store", dest="flank", metavar="<int>")
  parser.add_argument("-w", action="store", dest="window", metavar="<int>")
  parser.add_argument("-n", action="store", dest="number", metavar="<int>")

  args = parser.parse_args()
	
  infile = open(args.input, 'r');
  outfile = open(args.output, 'w');
  window = atoi(args.window)
#       round_factor = -2
  number = atoi(args.number)
  flank = atoi(args.flank)
#	genome_sizes = open('/home/user/packages/bedtools/genomes/mouse.mm9.genome','r');

#  infile = open(argv[1], 'r')
#  outfile = open(argv[1] + "_W" + argv[2] + "N" + argv[3] + "F" + argv[4], 'w')
#  window = atoi(argv[2])
#  number = atoi(argv[3])
#  flank = atoi(argv[4])
  genome_sizes = open('/seq/lib/mouse.mm9.genome', 'r')

  d = {}
  for line in genome_sizes:
	  line = line.strip()
	  sline = line.split()
	  if len(sline) > 0:
		  d[sline[0]]=sline[1]
			
  line_number = 0
  strand = "+"
  name = ""
	
  for line in infile:
	  line_number = line_number + 1
	  line = line.strip();
	  sline = line.split();
		
#                initial_start = int(round(atoi(sline[1]), round_factor)) + 1
#		initial_end = int(round(atoi(sline[2]), round_factor))
		
	  initial_start = atoi(sline[1]) + 1
	  initial_end = atoi(sline[2]) + 1
 
	  if len(sline) == 6: strand = sline[5]
	  else: strand = "+"
		
	  if len(sline) > 4: name = sline[3]
	  else: name = str(line_number)
		
	  span = initial_end - initial_start + 1
	  remain = span - number * window
#		rwindow = int(round(remain / (number - 1), round_factor))
	  rwindow = int(remain / (number - 1))
	  if remain < 0:
		  continue
			
	  for x in xrange(3):
		  if x == 0:
			  start = initial_start - flank * window
			  end = initial_end + flank * window
			  step_amount = 0
			  section_range = xrange(flank)
			  for index in section_range:	
				  out = ""
				  if strand == "+":
					  end = start + window - 1
					  out = sline[0] + "\t" + str(start) + "\t" + str(end) + "\t" + name + "\t" + \
					      str(index + 1) + "\t" + strand + "\n"
					  start = end + 1
				  else:
					  start = end - window + 1
					  out = sline[0] + "\t" + str(start) + "\t" + str(end) + "\t" + name + "\t" + \
					      str(index+1) + "\t" + strand + "\n"
					  end = start - 1  
				  if (start and end >=0) and (start and end <= atoi(d[sline[0]])): 
					  outfile.write(out)
		  elif x == 1:
			  start = initial_start
			  end = initial_end
			  step_amount = rwindow
			  section_range = xrange(number)
			  for index in section_range:
				  out = ""
				  if strand == "+":
					  end = start + window - 1
					  out = "\t".join([sline[0], str(start), str(end), name, str(flank + index + 1), strand]) + "\n"
					  #out = sline[0] + "\t" + str(start) + "\t" + str(end) + "\t" + name + "\t" + str(flank+index+1) + "\t" + strand + "\n"
					  start = end + rwindow + 1
				  else:
					  start = end - window + 1
					  out = "\t".join([sline[0], str(start), str(end), name, str(flank + index + 1), strand]) + "\n"
#out = sline[0] + "\t" + str(start) + "\t" + str(end) + "\t" + name + "\t" + str(flank+index+1) + "\t" + strand + "\n"
					  new_end = start - rwindow - 1
				  if (start and end >=0) and (start and end <= atoi(d[sline[0]])): 
					  outfile.write(out)                                             
		  elif x == 2:
			  start = initial_end + 1
			  end = initial_start - 1 
			  step_amount = 0
			  section_range = xrange(flank)				
			  for index in section_range:
				  out = ""
				  if strand == "+":
					  end = start + window - 1
					  out = "\t".join([sline[0], str(start), str(end), name, 
							   str(flank + number + index + 1), strand]) + "\n"
#out = sline[0] + "\t" + str(start) + "\t" + str(end) + "\t" + name + "\t" + str(flank+number+index+1)  + "\t" + strand + "\n"
					  start = end + 1
				  else:
					  start = end - window + 1
					  out = "\t".join([sline[0], str(start), str(end), name, 
							   str(flank + number + index + 1), strand]) + "\n"
#out = sline[0] + "\t" + str(start) + "\t" + str(end) + "\t" + name + "\t" + str(flank+number+index+1)  + "\t" + strand + "\n"
					  end = start - 1
				  if (start and end >=0) and (start and end <= atoi(d[sline[0]])): 
					  outfile.write(out)
  outfile.close()
		
if __name__ == "__main__":
	main(sys.argv) 	
