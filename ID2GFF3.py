#!/usr/bin/env python3
#coding: utf-8
#Author: Devin561
#E-Mail: zengzhen561@163.com
import pandas as pd

df = pd.read_table('Slycopersicum_390_ITAG2.4.gene_exons.gff3', sep='\t', header=None)
df_exon_mRNA = df[df.iloc[:,2].str.contains('exon|mRNA')]

print(df_exon_mRNA[:4])
a = open('diff.txt', 'r').readlines()
# d = open('df1.gff3', 'w')
d = []
for i in a:
    df_exon_mRNA_c = df_exon_mRNA[df_exon_mRNA.iloc[:,8].str.contains(i[:15])]
    for row in df_exon_mRNA_c.index:
        r = df_exon_mRNA_c.loc[row].values
        d.append(r)
d = pd.DataFrame(d)
d.to_csv('df1.gff3', sep='\t', header=False, index=False)
        # s = '\t'.join(r)
        # r = '\t'.split(r)
        # d.write(r + '\n')
# d.close()