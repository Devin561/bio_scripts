#!/usr/bin/env python3
# coding: utf-8
# Author: Devin561
# E-Mail: zengzhen561@163.com

import re
import os
import time
import sys
import pandas as pd


PB_NUM = re.compile('PB\.\d+\.\d+')
PB_list = []
output_list = open('lncRNA_PB_list.txt', 'w')

with open('CNCI_CPC2_PLEK_Pfam_noncoding.fa', 'r') as fasta:
    for line in fasta:
        RE_id = re.search(PB_NUM, line)
        if RE_id:
            PB_list.append(RE_id.group())
            output_list.write(RE_id.group())

output_list.close()

with open('gff_cmp_1.annotated.gtf', 'r') as gtf:
    for line in gtf:
        for pb in PB_list:
            RE_transcript = re.search('transcript\t.*(transcript_id "{0}").*(class_code ".")'.format(pb), line)
            if RE_transcript:
                print(pb + '\t' + RE_transcript.group(2))