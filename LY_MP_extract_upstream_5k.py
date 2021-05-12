#!/usr/bin/env python3
# coding: utf-8
# Author: Devin561
# E-Mail: zengzhen561@163.com


import re
import os
import sys
import time
import pysam
import gzip

"""需要文件：1. 基因组fasta文件；2. NLR_Annotator输出文件"""


# def apa_up_and_down_50bp(seq, site):
#     str = seq
#     up_seq = str[site - 50: site]
#     down_seq = str[site + 1: site + 51]
#     return up_seq, down_seq


def get_seq_from_genome_location(file, genomefile):
    """"从polyA_summmary.csv文件中获得位置信息，并确定提取序列的位置"""
    with open(file, 'r') as summary:
        print('The present is {0} ... '.format(species))
        print('nlr_txt is read\n' + '---------------'*4 + '---{0}---'.format(n) + '  ^~.~^  ---------->')
        for line in summary:
            tab = line.split('\t')
            gene_pattern = re.search('pseudogene', line)
            chr_num = tab[0]
            nlr_id = tab[1]
            start_loc = tab[3]
            stop_loc = tab[4]
            strand = tab[5]
            genome_chr_id = get_genome_file_chr_id_del_blank(genomefile)
            if gene_pattern:
                """取染色体id"""
                print('The present is {0} ... '.format(species))
                print('A target is found\n' + '---------------'*4 + '---{0}---'.format(n) + '  ^~.~^  ---------->')
                for chr_id in genome_chr_id:
                    # print(chr_id)
                    if chr_num == chr_id.split(' ')[0]:
                        # print(chr_num)
                        if strand == '+':
                            """正链"""
                            start, end = int(start_loc) - 5000, int(stop_loc)
                            try:
                                seq_up5k = get_seq(genome_file, chr_num, start, end)
                            except:
                                seq_up5k = get_seq(genome_file, chr_num, 1, end)
                            gene_id = '>' + nlr_id + '_upstream_5kb\n'
                            outfile_upstream.write(gene_id + seq_up5k + '\n')

                        if strand == '-':
                            """负链，需要反向互补转化为正链"""
                            start, end = int(start_loc), int(stop_loc) + 5000
                            try:
                                seq_up5k_rev = get_seq(genome_file, chr_num, start, end)
                            except:
                                seq_up5k_rev = get_seq(genome_file, chr_num, start, None)
                            seq_up5k = rev(seq_up5k_rev)
                            gene_id = '>' + nlr_id + '_upstream_5k\n'
                            outfile_upstream.write(gene_id + seq_up5k + '\n')


def rev(seq):
    """反向互补"""
    base_trans = {'A': 'T', 'C': 'G', 'T': 'A', 'G': 'C', 'N': 'N', 'a': 't', 'c': 'g', 't': 'a', 'g': 'c', 'n': 'n'}
    rev_seq = list(reversed(seq))
    rev_seq_list = [base_trans[k] for k in rev_seq]
    rev_seq = ''.join(rev_seq_list)
    return rev_seq


def get_seq(fasta_file, chr_id, start, end):
    """获得基因组fasta文件指定染色体上特定位置的序列"""

    fasta = pysam.Fastafile(fasta_file)
    sub_seq = fasta.fetch(chr_id, start - 1, end)  # fetch函数是从start+1开始，比如start为1，则从2开始，所以减去1，让其从start开始
    fasta.close()
    return sub_seq


def get_genome_file_chr_id_del_blank(GenomeFile):
    genome_chr_id = []
    if GenomeFile.endswith('.gz'):
        with gzip.open(GenomeFile) as genome:
            for line in genome:
                if line.startswith('>'):
                    chr = line.lstrip('>').strip()
                    # print(chr)
                    genome_chr_id.append(chr)
    else:
        with open(GenomeFile) as genome:
            for line in genome:
                if line.startswith('>'):
                    chr = line.lstrip('>').strip()
                    # print(chr)
                    genome_chr_id.append(chr)
    return genome_chr_id


def read_list(list_file):
    """读取物种id"""
    species_list = []
    with open(list_file) as list:
        for species in list:
            species = species.strip()
            species_list.append(species)
    return species_list


if __name__ == '__main__':
    species_list = read_list('list.txt')
    # print(species_list)
    files = os.listdir()
    n = 0
    for species in species_list:
        for file in files:
            # print(file)
            if species == file.split('.')[0]:
                n += 1
                genome_file = file
                nlr_file = './nlr/' + species + '.nlr.txt'
                # print(nlr_file)
                print('\n' + '*'*100)
                print(species + ' is starting\n' + '---------------'*4 + '---{0}---'.format(n) + '  ^~.~^  ---------->')
                if genome_file.endswith('.gz'):
                    os.system('gunzip {0}'.format(genome_file))
                    genome_file = genome_file.replace('.gz', '')
                outfile_upstream = open('./result/{0}_upstream_5k.fa'.format(species), 'w')
                get_seq_from_genome_location(nlr_file, genome_file)
                outfile_upstream.close()
                print(species + ' is finished\n' + '---------------'*4 + '---{0}---'.format(n) + '  ^~.~^  ---------->')
                print('*' * 100)

