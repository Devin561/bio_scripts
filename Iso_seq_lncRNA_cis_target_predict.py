#!/usr/bin/env python3
# coding: utf-8
# Author: Devin561
# E-Mail: zengzhen561@163.com


import re
import os
import sys
import getopt

"""
files required：1. annotation file (gff or gtf)；2. id list of lncRNA
usage: python3 Iso_seq_lncRNA_cis_target_predict.py -g <annotation.gtf> -l <lncRNA_id.list> 
"""


def position_flanking_100kb(gtf_file, id):
    chrom, up_100kb, down_100kb = '', '', ''
    id_mod = id.split('.')[0] + '\\.' + id.split('.')[1] + '\\.' + id.split('.')[2]
    with open(gtf_file, 'r') as gtf:
        for line in gtf:
            RE_lnc_id = re.search('\ttranscript\t(.*?){0}";'.format(id_mod), line)
            if RE_lnc_id:
                print(RE_lnc_id.group())
                chrom = line.split('\t')[0]
                start, stop = line.split('\t')[3], line.split('\t')[4]
                up_100kb = int(start) - 100000
                down_100kb = int(stop) + 100000
                break
    return str(chrom), up_100kb, down_100kb


def find_cis_target(gtf_file, lnc_chrom, lnc_up_100kb, lnc_down_100kb):
    cis_gene_list = []
    print(lnc_chrom, lnc_up_100kb, lnc_down_100kb)
    with open(gtf_file, 'r') as gtf:
        for line in gtf:
            chrom, start, stop = line.split('\t')[0], int(line.split('\t')[3]), int(line.split('\t')[4])
            transcript_id = re.search('\ttranscript\t.*transcript_id "(.*?)";', line)
            if transcript_id:
                if chrom != lnc_chrom:
                    # print(line.split('\t')[0])
                    continue
                if chrom == lnc_chrom and lnc_up_100kb < stop < lnc_up_100kb + 100000:
                    # print(transcript_id.group())
                    cis_gene_list.append(transcript_id.group(1))
                if chrom == lnc_chrom and lnc_down_100kb > start > lnc_down_100kb - 100000:
                    # print(transcript_id.group())
                    cis_gene_list.append(transcript_id.group(1))
                if chrom == lnc_chrom and start > lnc_down_100kb:
                    break
    return cis_gene_list


def option_parameters(argv):
    gff_file, id_list = '', ''
    try:
        opts, args = getopt.getopt(argv, "hg:l:", ["help", "gff=", "list="])
    except getopt.GetoptError:
        print('[usage] python3 Iso_seq_lncRNA_cis_target_predict.py -g <annotation.gtf> -l <lncRNA_id.list>')
    for opt_name, opt_value in opts:
        if opt_name in ('-h', '--help'):
            try:
                os.system('figlet Love Python3')
            except:
                pass
            print('\n*--------------------------------↓--------------------------------------------↓\n')
            print('[usage] python3 Iso_seq_lncRNA_cis_target_predict.py -g <annotation.gtf> -l <lncRNA_id.list>')
            print('\n*--------------------------------↑--------------------------------------------↑\n')
            sys.exit(2)
        elif opt_name in ('-g', '--gff'):
            gff_file = opt_value
        elif opt_name in ('-l', "--list"):
            id_list = opt_value
    return gff_file, id_list


if __name__ == '__main__':
    # gtf = sys.argv[1]
    # idlist_file = sys.argv[2]
    # gff_file, id_list = '', ''
    # try:
    #     opts, args = getopt.getopt(sys.argv[1:], "hg:l:", ["help", "gff=", "list="])
    # except getopt.GetoptError:
    #     print('[usage] python3 Iso_seq_lncRNA_cis_target_predict.py -g <.gtf> -l <lncRNA.list>')
    # for opt_name, opt_value in opts:
    #     if opt_name in ('-h', '--help'):
    #         print('python3 Iso_seq_lncRNA_cis_target_predict.py -g <.gtf> -l <lncRNA.list>')
    #     elif opt_name in ('-g', '--gff'):
    #         gff_file = opt_value
    #         print(gff_file)
    #     elif opt_name in ('-l', "--list"):
    #         id_list = opt_value
    gff_file, id_list = option_parameters(sys.argv[1:])
    cis_target_id = open('cis_target_list2.txt', 'w')
    with open(id_list, 'r') as idlist:
        for id in idlist:
            id = id.strip()
            lnc_chrom, lnc_up_100kb, lnc_down_100kb = position_flanking_100kb(gff_file, id)
            cis_target = find_cis_target(gff_file, lnc_chrom, lnc_up_100kb, lnc_down_100kb)
            for cis_id in cis_target:
                cis_target_id.write(id + '\t' + cis_id + '\n')
    cis_target_id.close()
