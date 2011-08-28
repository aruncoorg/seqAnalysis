#!/usr/bin/env python

import sys
import os
import shutil
from subprocess import Popen, PIPE
def main(argv):
    
    # Execute intersectBed on given preprocessed BED6 file with annotation library

    #annotation_path = "/home/user/lib/annotations"
    annotation_path = "/home/user/lib/annoset_export"
    annotation_files = os.listdir(annotation_path) 
    BED = argv[1]
    BED_name_split = BED.split(".")
    data_path = "/home/user/data/working/" + BED
    output_path = "/home/user/analysis/profiles/" + BED_name_split[0] + "_profiles"
    
    if os.path.exists(output_path):
        shutil.rmtree(output_path)
    os.mkdir(output_path)
    
    for annotation_file in annotation_files:
        anno = annotation_path + "/" + annotation_file
        print "intersecting with " + annotation_file
        outfile = open(output_path + "/" + annotation_file, 'w')
        cmd_args = ['/usr/local/bin/intersectBed', '-a', anno, '-b', data_path, '-wa', '-c']
        p = Popen(cmd_args,stdout=outfile)
        return_code = p.wait()
        outfile.close()
        
if __name__ == "__main__":
    main(sys.argv)
