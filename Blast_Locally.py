#!/usr/bin/env python3
# coding: utf-8
# Author: Devin561
# E-Mail: zengzhen561@163.com

from collections import OrderedDict
import re
import os
import time
import sys
import pandas as pd


class LocalBlast():

    def __init__(self, species, file):
        self.species = species
        self.file = file

    def make_blast_db(self):
        CDS = re.search('cds', self.file, re.I)
        GZ = re.search('.gz', self.file, re.I)
        if CDS:
            """提取cds文件，判断是否是压缩格式，然后建库"""
            if GZ:
                os.system('gzip -d ../genome/{0}/{1}'.format(self.species, self.file))
                print("\n\n{0} cds文件解压缩完成\n\n".format(self.species))
                cds_name = self.file[:-3]
                os.system('makeblastdb -in ../genome/{1}/{0} -dbtype nucl -parse_seqids -out ../blast/{1}'.format(
                    cds_name, self.species))
            else:
                print("\n\n不需要压缩，直接开始建库\n\n".format(self.species))
                os.system(
                    'makeblastdb -in ../genome/{1}/{0} -dbtype nucl -parse_seqids -out ../blast/{1}'.format(self.file,
                                                                                                            self.species))

    def local_blast(self, pattern):
        genus = re.split('_', self.species)[0]
        sp = re.split('_', self.species)[1]
        out = genus[0] + sp[:2]
        print('\n\n{0}开始比对'.format(self.species))
        if pattern == 'tblastn':
            os.system('tblastn -query pho2.fa -db ../blast/{0} -outfmt 6 -out ../result/{0}_pho2 -evalue 1e-8 '
                      '-num_threads 4'.format(self.species, out))
        elif pattern == 'blastp':
            os.system('blastp -query pho2.fa -db ../blast/{0} -outfmt 6 -out ../result/{0}_pho2 -evalue 1e-8 '
                      '-num_threads 4'.format(self.species, out))
        elif pattern == 'blastn':
            os.system('blastn -query pho2.fa -db ../blast/{0} -outfmt 6 -out ../result/{0}_pho2 -evalue 1e-8 '
                      '-num_threads 4'.format(self.species, out))
        elif pattern == 'blastx':
            os.system('blastx -query pho2.fa -db ../blast/{0} -outfmt 6 -out ../result/{0}_pho2 -evalue 1e-8 '
                      '-num_threads 4'.format(self.species, out))
        print('{0}比对完成\nresult is in result folder\n'.format(self.species))

    def get_seq_from_id(self, gene_id):
        outfile = open('Blast_Pho2.fa', 'a')
        dict = {}
        with open('../genome/{0}/{1}'.format(self.species, file), 'r') as fasta:
            for line in fasta:
                if line.startswith('>'):
                    name = line.lstrip('>').strip()
                    dict[name] = ''
                else:
                    dict[name] += line.strip()

        dict1 = OrderedDict(sorted(dict.items(), key=lambda d: d[0]))
        for k, v in dict1.items():
            RE = re.search(str(gene_id), k)
            if RE:
                outfile.write('>' + self.species + '_' + str(gene_id) + '\n' + str(''.join(v)) + '\n')
            else:
                pass
        outfile.close()

    def get_seq_from_id_work(self):
        out = open('Blast_Pho2.fa', 'w')
        out.close()
        n = 0
        try:
            table = pd.read_table('../result/{0}_pho2'.format(self.species), header=None)
            n += 1
        except:
            print('File {0}_pho2 is not exist'.format(self.species))
            # table = pd.DataFrame()
            # raise Exception('File {0}_pho2 is not exist'.format(self.species))
            return None
        id_list = table[1]
        CDS = re.search('cds', self.file, re.I)
        if CDS:
            for gene_id in id_list:
                print(self.species + ' ' + str(gene_id) + '\n开始提取\n->->->->->->->->->->->->->')
                self.get_seq_from_id(str(gene_id))
                print('提取完毕\n')
        print('totally {0} species have done blast'.format(n))

    def translate(self, seq):
        table = {
            'ATA': 'I', 'ATC': 'I', 'ATT': 'I', 'ATG': 'M',
            'ACA': 'T', 'ACC': 'T', 'ACG': 'T', 'ACT': 'T',
            'AAC': 'N', 'AAT': 'N', 'AAA': 'K', 'AAG': 'K',
            'AGC': 'S', 'AGT': 'S', 'AGA': 'R', 'AGG': 'R',
            'CTA': 'L', 'CTC': 'L', 'CTG': 'L', 'CTT': 'L',
            'CCA': 'P', 'CCC': 'P', 'CCG': 'P', 'CCT': 'P',
            'CAC': 'H', 'CAT': 'H', 'CAA': 'Q', 'CAG': 'Q',
            'CGA': 'R', 'CGC': 'R', 'CGG': 'R', 'CGT': 'R',
            'GTA': 'V', 'GTC': 'V', 'GTG': 'V', 'GTT': 'V',
            'GCA': 'A', 'GCC': 'A', 'GCG': 'A', 'GCT': 'A',
            'GAC': 'D', 'GAT': 'D', 'GAA': 'E', 'GAG': 'E',
            'GGA': 'G', 'GGC': 'G', 'GGG': 'G', 'GGT': 'G',
            'TCA': 'S', 'TCC': 'S', 'TCG': 'S', 'TCT': 'S',
            'TTC': 'F', 'TTT': 'F', 'TTA': 'L', 'TTG': 'L',
            'TAC': 'Y', 'TAT': 'Y', 'TAA': '_', 'TAG': '_',
            'TGC': 'C', 'TGT': 'C', 'TGA': '_', 'TGG': 'W',
        }
        protein = ""
        if len(seq) % 3 == 0:
            for i in range(0, len(seq), 3):
                codon = seq[i:i + 3]
                protein += table[codon]
        return protein

    def get_seq_from_cds_id(self):
        outfile = open('../protein/{0}_Pho2_pro.fa'.format(self.species), 'w')
        print('\n{0} is started\n>>>>>>>>>>>>>>>>>>'.format(self.species))
        dict = {}
        with open('../genome/{0}/{1}'.format(self.species, self.file), 'r') as fasta:
            for line in fasta:
                if line.startswith('>'):
                    name = line.lstrip('>').strip()
                    dict[name] = ''
                else:
                    dict[name] += line.strip()
        dict1 = OrderedDict(sorted(dict.items(), key=lambda d: d[0]))
        for k, v in dict1.items():
            pro = self.translate(v)  # tranlate DNA to Protein
            outfile.write('>' + k + '\n' + pro + '\n')
        outfile.close()

    def get_seq_from_cds_id_work(self):
        CDS = re.search('cds', self.file, re.I)
        if CDS:
            """提取cds文件"""
            self.get_seq_from_cds_id()
            print('\n{0} has completed\n'.format(self.species))

    def get_seq_from_cds_id_work_use_perl(self):
        CDS = re.search('cds', self.file, re.I)
        if CDS:
            """用BIO::PERL提取cds文件"""
            os.system('perl Translate_DNA.pl -i ../genome/{1}/{0} -o ../protein/{1}'.format(self.file, self.species))
            print('\n{0} has completed\n'.format(self.species))


def make_dir():
    folders = ['project_blast', 'genome', 'work', 'protein', 'genome', 'result']
    for folder in folders:
        if os.path.exists('./project_blast/{0}'.format(folder)):
            print('{0} is existing'.format(folder))
        else:
            try:
                os.mkdir('./project_blast/{0}'.format(folder))
            except Exception as e:
                os.makedirs('./project_blast/{0}'.format(folder))


if __name__ == '__main__':
    make_dir()
    species_name = os.listdir('../genome')
    species_name.sort()
    for species in species_name:
        file_type = os.listdir('../genome/{0}'.format(species))
        for file in file_type:
            blast = LocalBlast(species, file)
            blast.make_blast_db()
            blast.local_blast('tblastn')
            # blast.get_seq_from_cds_id_work_use_perl()
