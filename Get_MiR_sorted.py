#!/usr/bin/env python3
# coding: utf-8
# Author: Devin561
# E-Mail: zengzhen561@163.com

import re
import os
import sys
from collections import OrderedDict


def get_miR(num, file):
    outfile = open(os.path.basename(file).split('.')[0] + "_{0}.".format(num) + os.path.basename(file).split('.')[1],
                   'w')
    dict = {}
    num = str(num)
    with open(file, 'r') as fasta:
        for line in fasta:
            if line.startswith('>'):
                name = line.lstrip('>').strip()
                dict[name] = ''
            else:
                dict[name] += line.strip()
    dict1 = OrderedDict(sorted(dict.items(), key=lambda d: d[0])) #将名字排序，d[0]是按照键来排序，d[1]是按照值来排序
    for k, v in dict1.items():
        RE = re.search(r'\D' + num + r'\D', k)
        if RE:
            outfile.write('>' + k + '\n' + str(''.join(v)) + '\n')
        else:
            pass
    outfile.close()


if __name__ == '__main__':
    get_miR(sys.argv[1], './mature.fa')
