#!/usr/bin/env python3
# coding: utf-8
# Author: Devin561
# E-Mail: zengzhen561@163.com
import sys

file1 = open(sys.argv[1], 'r').readlines()
file2 = open(sys.argv[2], 'r').readlines()

differece = set(file1) ^ set(file2)
# differece = sorted(differece)
outtxt = open('output_diff_file.txt', 'w')
for line in differece:
    # linenew = line[0:]
    # line[:-1] == '\n':
    outtxt.write(line)
    # else:
    #     outtxt.write(line + '\n')
outtxt.close()
