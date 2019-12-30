#!/usr/bin/env python3
# coding:utf-8
# Author: Devin561
# E-Mail: zengzhen561@163.com

import os


def get_url(srr):
    """get url of SRR file"""
    first_six_str = srr[:6]
    last_one_num = "00" + srr[-1]
    download_url = "http://ftp.sra.ebi.ac.uk/vol1/fastq/{0}/{1}/{2}/{2}.fastq.gz".format(first_six_str, last_one_num,srr)
    print(download_url)
    return download_url


def download(srr):
    """download SRR from url"""
    os.system('echo "{0} is beginning to download, please wait patiently..."'.format(srr))
    try:
        os.system("axel -n 4 {0}".format(get_url(srr)))
        os.system('echo "{0} has been in {1}"'.format(srr + ".fastq.gz", os.getcwd()))
        os.system('echo ---------------------------------------------------\n')
    except:
        os.system('echo "{0} was failed to download"'.format(srr))
        os.system('echo ---------------------------------------------------\n')


if __name__ == '__main__':
    # srr = "SRR2190795"
    # http://ftp.sra.ebi.ac.uk/vol1/fastq/SRR219/005/SRR2190795/SRR2190795.fastq.gz
    # for i in range(2, 9):
    #     download('SRR224018{0}'.format(i))
    get_url('SRR2240183')