#!/usr/bin/env python
import sys
from pyGTF import Transcript
from pyGTF import GTFReader

def usage():
	print("xxx.py .gtf class_code out_gtf")
in_gtf = sys.argv[1]
class_code = sys.argv[2]
out_gtf = sys.argv[3]

fw = open(out_gtf,'w')

with GTFReader(in_gtf,flag_stream=True) as fi:
    for i in fi:
        if i._attri['class_code'] == class_code:
            i.to_gtf(fw)
            
fw.close()
