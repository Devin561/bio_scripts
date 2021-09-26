#!/usr/bin/env python3
# coding: utf-8
# Author: Devin561
# E-Mail: zengzhen561@163.com

import re
import os
import sys
import time



def read_fasta(fasta_file):
    dict = {}
    with open(fasta_file, 'r') as fasta:
        for line in fasta:
            if line.startswith('>'):
                name = line.lstrip('>').strip()
                dict[name] = ''
            else:
                dict[name] += line.strip()

    for n in range(101):
        A, B, C, D = 0, 0, 0, 0
        list = []
        for v in dict.values():
            base = v[n]
            print(str(n))
            list.append(base)
            A = list.count('A') + list.count('a')
            T = list.count('T') + list.count('t')
            C = list.count('C') + list.count('c')
            G = list.count('G') + list.count('g')

        freq_A = A / (A + G + C + T)
        freq_T = T / (A + G + C + T)
        freq_C = C / (A + G + C + T)
        freq_G = G / (A + G + C + T)

        count_file.write(
            str(n + 1) + '\t' + str(freq_A) + '\t' + str(freq_T) + '\t' + str(freq_C) + '\t' + str(freq_G) + '\n')


if __name__ == '__main__':
    count_file = open('count_frequency', 'w')
    count_file.write('location' + '\t' + 'freq_A' + '\t' + 'freq_T' + '\t' + 'freq_C' + '\t' + 'freq_G' + '\n')
    read_fasta('./total_101.fa')
    print(time.perf_counter())
