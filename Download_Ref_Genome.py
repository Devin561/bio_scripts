#!/usr/bin/env python3
# coding: utf-8
# Author: Devin561
# E-Mail: zengzhen561@163.com

import re
import os
import sys
import requests
import requests_ftp


def get_genome_url(species):
    TOPLEVEL = re.compile('{0}.*?.dna.toplevel.fa.gz'.format(species.capitalize()))
    url_1st = "ftp://ftp.ensemblgenomes.org/"
    url_2nd = "ftp://ftp.ensemblgenomes.org/pub/plants/release-45/fasta/"
    url_3rd_page = url_2nd + species.lower() + "/dna/"
    requests_ftp.monkeypatch_session()
    s = requests.Session()
    url_page = s.list("ftp://ftp.ensemblgenomes.org/pub/plants/release-45/fasta/{0}/dna".format(species.lower()))
    url_page.encoding = 'utf-8'
    download_url = re.findall(TOPLEVEL, url_page.text)
    download_url = "".join(download_url)
    url = url_3rd_page + download_url
    print (url)
    return url


def download(species):
    os.system('echo "{0} is beginning to download, please wait patiently..."'.format(species + " Ref_genome"))
    try:
        os.system("axel -n 4 {0}".format(get_genome_url(species)))
        os.system('echo "{0} has been in {1}"'.format(species + "Ref_genome", os.getcwd()))
        os.system('echo ---------------------------------------------------\n')
    except:
        os.system('echo "{0} was failed to download"'.format(species + "_Ref_genome"))
        os.system('echo ---------------------------------------------------\n')


if __name__ == '__main__':
    species = str(input("Latin name for species (eg.Arabidopsis_thaliana): "))
    # get_download_url('Amborella_trichopoda')
    species = re.sub(' ', '_', species)
    download(species)
