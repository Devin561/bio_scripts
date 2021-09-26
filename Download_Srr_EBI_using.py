#!/usr/bin/env python3
# coding: utf-8
# Author: Devin561
# E-Mail: zengzhen561@163.com

import os


def get_url(srr):
    first_six_str = srr[:6]
    last_one_num = "00" + srr[-1]
    download_url = "http://ftp.sra.ebi.ac.uk/vol1/fastq/{0}/{1}/{2}/{2}.fastq.gz".format(first_six_str, last_one_num,
                                                                                         srr)
    download_url_1 = "http://ftp.sra.ebi.ac.uk/vol1/fastq/{0}/{1}/{2}/{2}_1.fastq.gz".format(first_six_str, last_one_num,
                                                                                         srr)
    download_ur_2 = "http://ftp.sra.ebi.ac.uk/vol1/fastq/{0}/{1}/{2}/{2}_2.fastq.gz".format(first_six_str, last_one_num,
                                                                                         srr)

    return download_url, download_url_1, download_ur_2


def download(srr):
    os.system('echo "{0} is beginning to download, please wait patiently..."'.format(srr))
    os.system('echo "\n"')
    os.system('echo "\n"')
    download_url, download_url_1, download_ur_2 = get_url(srr)
    print(download_url, download_url_1, download_ur_2)
    try:
        # try:
        #     os.system("axel -n 10 {0}".format(download_url))
        #     os.system('echo "\n"')
        #     os.system('echo "-------------------------------------------------------------\n"')
        #     os.system('echo "{0} has been in {1}"'.format(srr + ".fastq.gz", os.getcwd()))
        #     os.system('echo "-------------------------------------------------------------\n"')
        # except:
        os.system("axel -n 10 {0}".format(download_url_1))
        os.system('echo "\n"')
        os.system('echo "-------------------------------------------------------------\n"')
        os.system('echo "{0} has been in {1}"'.format(srr + "_1.fastq.gz", os.getcwd()))
        os.system('echo "-------------------------------------------------------------\n"')
        os.system("axel -n 10 {0}".format(download_ur_2))
        os.system('echo "\n"')
        os.system('echo "{0} has been in {1}"'.format(srr + "_2.fastq.gz", os.getcwd()))
        os.system('echo "-------------------------------------------------------------\n"')
    except:
        os.system('echo "---------------------------------------------------\n"')
        os.system('echo "{0} was failed to download"'.format(srr))
        os.system('echo "---------------------------------------------------\n"')


if __name__ == '__main__':
    # srr = "SRR2190795"
    # http://ftp.sra.ebi.ac.uk/vol1/fastq/SRR219/005/SRR2190795/SRR2190795.fastq.gz
    for i in range(31, 34):
        download('SRR96690{0}'.format(i))
    # download("SRR7986788")
    # get_url("SRR7986788")
