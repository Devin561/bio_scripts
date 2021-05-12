#!/usr/bin/env python3
# coding: utf-8
# Author: Devin561
# E-Mail: zengzhen561@163.com

import re
import os
import sys


class IdentifyDomainChange:
    def __init__(self, as_file, hmm_domain_file):
        self.as_file = as_file
        self.hmm_domain_file = hmm_domain_file
        self.domain_dict = {}

    def read_as_event_result(self):
        tup_1st = ()
        tup_2nd = ()
        with open(self.as_file) as file:
            for line in file:
                re_1st = re.search(RE_as_transcript_1st, line).group(1)
                re_2nd = re.search(RE_as_transcript_2nd, line).group(1)
                # print(re_1st)
                tup_1st = tup_1st + (re_1st,)
                tup_2nd = tup_2nd + (re_2nd,)
        return tup_1st, tup_2nd

    def read_domain_result(self):
        tup_1st, tup_2st = self.read_as_event_result()
        with open(self.hmm_domain_file) as file:
            num_1 = 0
            num_2 = 0
            for line in file:
                domain_list = line.strip().split('\t')
                # print(domain_list[0])
                # print(len(tup_1st))
                # while num_1 < len(tup_1st):
                for num_1 in range(0, len(tup_1st)):
                    """当id匹配到domain的文件时，break跳出本次循环"""
                    if tup_1st[num_1] == domain_list[0]:
                        # print(domain_list[0])
                        self.domain_dict[tup_1st[num_1]] = domain_list[1:]
                        num_1 += 1
                        break
                # while num_2 < len(tup_2st):
                for num_2 in range(0, len(tup_2st)):
                    if tup_2st[num_2] == domain_list[0]:
                        self.domain_dict[tup_2st[num_2]] = domain_list[1:]
                        num_2 += 1
                        break
        return tup_1st, tup_2st, self.domain_dict

    def cmp_domain(self):
        tup_1st, tup_2st, self.domain_dict = self.read_domain_result()
        equal = 0
        # cplx = 0
        change = 0
        add_sub = 0
        for i in range(0, len(tup_1st)):
            # print(i)
            print(tup_1st[i])
            if set(self.domain_dict[tup_1st[i]]) == set(self.domain_dict[tup_2st[i]]):
                equal += 1
            # elif set(self.domain_dict[tup_1st[i]]) < (self.domain_dict[tup_2st[i]]):
            elif set(self.domain_dict[tup_1st[i]]).issubset((self.domain_dict[tup_2st[i]])):
                add_sub += 1
                print(tup_1st[i])
            # elif set(self.domain_dict[tup_1st[i]]) > (self.domain_dict[tup_2st[i]]):
            elif set(self.domain_dict[tup_2st[i]]).issubset((self.domain_dict[tup_1st[i]])):
                add_sub += 1
                print(tup_1st[i])
            else:
                change += 1
        return equal, add_sub, change

    def test_print(self):
        print(self.as_file, self.hmm_domain_file)


if __name__ == '__main__':
    RE_as_transcripts = re.compile('transcript_id "(.*)"; gene_id')
    RE_as_transcript_1st = re.compile('transcript_id "(PB\.\d+\.\d+)')
    RE_as_transcript_2nd = re.compile('transcript_id ".*?,(PB\.\d+\.\d+)')
    run = IdentifyDomainChange(sys.argv[1], './domain_name_output_run.txt')
    equal, change, add_sub = run.cmp_domain()
    os.system('echo "{0}" >> Domain_change_profiling.txt'.format(os.path.basename(sys.argv[1]).split('.')[0]))
    os.system('echo "equal\t{0}\nchange\t{1}\nadd_sub\t{2}\n\n" >> Domain_change_profiling.txt'.format(equal, change, add_sub))
    print('equal\t{0}\nchange\t{1}\nadd_sub\t{2}\n'.format(equal, change, add_sub))
