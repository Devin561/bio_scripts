#!/usr/bin/env python3
# coding: utf-8
# Author: Devin561
# E-Mail: zengzhen561@163.com

import re
import os
import sys
import time

"""
[usage] python3 Iso_seq_GTF_merge_modify.py gtf.file
将merge后的gtf文件的gene_id中的'XLOC_'和transcript_id的'TCONS_'修改为对应的Ref、Pacbio或NGS的编号
适用于标注为phytozomev13、PacBio和StringTie的注释文件
若要用于其它注释文件，需修改正则表达式
"""


def combined_gtf_modify(index_file, out_file):
    """将combined后的GTF文件修正，去掉XLOC和TCONS等，gene_id以Soly、NGS或PB开头"""
    RE_XLOC = re.compile('gene_id "(XLOC_\d+)";')
    RE_oId = re.compile('oId "(\S+)"; ')  # 匹配非空字符
    RE_transcript_id = re.compile('transcript_id "(TCONS_\d+)"; gene_id')
    RE_gene_id = re.compile('gene_name "(Solyc\w+\.\d+\.ITAG3\.2)";')

    dict = {}

    with open(index_file, 'r') as GTF:
        for line in GTF:
            """分别处理phytozomev13、StringTie和PacBio三种情况"""
            RE_phytozomev13_Transcript = re.search('phytozomev13\ttranscript\t', line)
            RE_phytozomev13_exon = re.search('phytozomev13\texon\t', line)
            RE_PacBio_Transcript = re.search('PacBio\ttranscript\t', line)
            RE_PacBio_Exon = re.search('PacBio\texon\t', line)
            RE_stringtie_Transcript = re.search('StringTie\ttranscript\t', line)
            RE_stringtie_Exon = re.search('StringTie\texon\t', line)

            if RE_phytozomev13_Transcript:
                XLOC = re.search(RE_XLOC, line).group(1)
                TCONS = re.search(RE_transcript_id, line).group(1)
                oId = re.search(RE_oId, line).group(1)
                Ref_gene_id = re.search(RE_gene_id, line).group(1)
                print(XLOC + TCONS + oId + Ref_gene_id)
                name = re.sub(XLOC, Ref_gene_id, line)
                name = re.sub(TCONS, oId, name).strip()
                dict[name] = ''
                print('++++')
            elif RE_PacBio_Transcript:
                XLOC = re.search(RE_XLOC, line).group(1)
                TCONS = re.search(RE_transcript_id, line).group(1)
                oId = re.search(RE_oId, line).group(1)
                Gene_Name = re.search('gene_name', line)
                if Gene_Name:
                    PB_gene_id = re.search('gene_name "(\S+)";', line).group(1)
                else:
                    PB_gene_id = re.search('(\w+\.\d+)\.\d+', oId).group(1)
                print(XLOC + TCONS + oId + PB_gene_id)
                name = re.sub(XLOC, PB_gene_id, line)
                name = re.sub(TCONS, oId, name).strip()
                dict[name] = ''
            elif RE_stringtie_Transcript:
                XLOC = re.search(RE_XLOC, line).group(1)
                TCONS = re.search(RE_transcript_id, line).group(1)
                oId = re.search(RE_oId, line).group(1)
                Gene_Name = re.search('gene_name', line)
                if Gene_Name:
                    NGS_gene_id = re.search('gene_name "(\S+)";', line).group(1)
                else:
                    NGS_gene_id = re.search('(\w+\.\d+)\.\d+', oId).group(1)
                print(XLOC + TCONS + oId + NGS_gene_id)
                name = re.sub(XLOC, NGS_gene_id, line)
                name = re.sub(TCONS, oId, name).strip()
                dict[name] = ''
                print('++++')
            elif RE_PacBio_Exon:
                value = re.sub(TCONS, oId, line)
                value = re.sub(XLOC, PB_gene_id, value)
                dict[name] += value
            elif RE_phytozomev13_exon:
                value = re.sub(TCONS, oId, line)
                value = re.sub(XLOC, Ref_gene_id, value)
                dict[name] += value
            elif RE_stringtie_Exon:
                value = re.sub(TCONS, oId, line)
                value = re.sub(XLOC, NGS_gene_id, value)
                dict[name] += value

        output = open(out_file, 'w')
        for k, v in dict.items():
            output.write(k + '\n' + v)
    output.close()


if __name__ == '__main__':
    input_FILE = sys.argv[1]
    basename = os.path.basename(input_FILE)
    outfile_l = re.split('\.', basename)[:-1]
    out_FILE = '.'.join(outfile_l) + '_modified.' + re.split('\.', basename)[-1]
    combined_gtf_modify(input_FILE, out_FILE)
