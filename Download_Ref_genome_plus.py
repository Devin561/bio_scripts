#!/usr/bin/env python3
# coding: utf-8
# Author: Devin561
# E-Mail: zengzhen561@163.com

import re
import os
import sys
import requests
import requests_ftp


class Download_Ref_Genome_Ensembl_plant():
    """Download Ref_Genome information from Ensembl_plant"""

    def __init__(self, species):
        self.species = species

    def get_genome_url(self):
        """genome"""
        TOPLEVEL = re.compile('{0}.*?.dna.toplevel.fa.gz'.format(self.species.capitalize()))
        url_1st = "ftp://ftp.ensemblgenomes.org/"
        url_2nd = "ftp://ftp.ensemblgenomes.org/pub/plants/release-45/fasta/"
        url_3rd_page = url_2nd + self.species.lower() + "/dna/"
        requests_ftp.monkeypatch_session()
        s = requests.Session()
        url_page = s.list(
            "ftp://ftp.ensemblgenomes.org/pub/plants/release-45/fasta/{0}/dna".format(self.species.lower()))
        url_page.encoding = 'utf-8'
        download_url = re.findall(TOPLEVEL, url_page.text)
        download_url = "".join(download_url)
        url = url_3rd_page + download_url
        print(url)
        return url

    def get_cds_url(self):
        """cds"""
        TOPLEVEL = re.compile('{0}.*?.cds.all.fa.gz'.format(self.species.capitalize()))
        url_1st = "ftp://ftp.ensemblgenomes.org/"
        url_2nd = "ftp://ftp.ensemblgenomes.org/pub/plants/release-45/fasta/"
        url_3rd_page = url_2nd + self.species.lower() + "/cds/"
        requests_ftp.monkeypatch_session()
        s = requests.Session()
        url_page = s.list(
            "ftp://ftp.ensemblgenomes.org/pub/plants/release-45/fasta/{0}/cds".format(self.species.lower()))
        url_page.encoding = 'utf-8'
        download_url = re.findall(TOPLEVEL, url_page.text)
        download_url = "".join(download_url)
        url = url_3rd_page + download_url
        print(url)
        return url

    def get_gff3_url(self):
        """gff"""
        TOPLEVEL = re.compile('{0}.*?.gff3.gz'.format(self.species.capitalize()))
        url_1st = "ftp://ftp.ensemblgenomes.org/"
        url_2nd = "ftp://ftp.ensemblgenomes.org/pub/plants/release-45/gff3/"
        url_3rd_page = url_2nd + self.species.lower()
        requests_ftp.monkeypatch_session()
        s = requests.Session()
        url_page = s.list(
            "ftp://ftp.ensemblgenomes.org/pub/plants/release-45/gff3/{0}".format(self.species.lower()))
        url_page.encoding = 'utf-8'
        download_url = re.findall(TOPLEVEL, url_page.text)[-1]
        print (download_url)
        download_url = "".join(download_url)
        url = url_3rd_page + "/" + download_url
        print(url)
        return url

    def download_all(self):
        """Download genome, cds, gff"""
        os.system('echo "{0} is beginning to download, please wait patiently..."'.format(self.species + " Ref_genome"))
        os.mkdir('./{0}'.format(self.species))
        try:
            os.system("axel -n 4 {0} -o ./{1}".format(self.get_genome_url(), self.species))
            os.system("axel -n 4 {0} -o ./{1}".format(self.get_cds_url(), self.species))
            os.system("axel -n 4 {0} -o ./{1}".format(self.get_gff3_url(), self.species))
            os.system('echo "{0} has been in {1}"'.format(self.species + "Ref_genome, cds, gff", os.getcwd()))
            os.system('echo ---------------------------------------------------\n')
        except:
            os.system('echo "{0} was failed to download"'.format(self.species + "_Ref_genome, cds, gff"))
            os.system('echo ---------------------------------------------------\n')

    def download_genome(self):
        """Download genome"""
        os.system('echo "{0} is beginning to download, please wait patiently..."'.format(self.species + " Ref_genome"))
        os.mkdir('./{0}'.format(self.species))
        try:
            os.system("axel -n 4 {0} -o ./{1}".format(self.get_genome_url(), self.species))
            os.system('echo "{0} has been in {1}"'.format(self.species + "Ref_genome", os.getcwd()))
            os.system('echo ---------------------------------------------------\n')
        except:
            os.system('echo "{0} was failed to download"'.format(self.species + "_Ref_genome"))
            os.system('echo ---------------------------------------------------\n')

    def download_cds(self):
        """Download cds"""
        os.system('echo "{0} is beginning to download, please wait patiently..."'.format(self.species + " Ref_genome"))
        os.mkdir('./{0}'.format(self.species))
        try:
            os.system("axel -n 4 {0} -o ./{1}".format(self.get_cds_url(), self.species))
            os.system('echo "{0} has been in {1}"'.format(self.species + " cds", os.getcwd()))
            os.system('echo ---------------------------------------------------\n')
        except:
            os.system('echo "{0} was failed to download"'.format(self.species + " cds"))
            os.system('echo ---------------------------------------------------\n')

    def download_gff(self):
        """Download gff"""
        os.system('echo "{0} is beginning to download, please wait patiently..."'.format(self.species + " Ref_genome"))
        os.mkdir('./{0}'.format(self.species))
        try:
            os.system("axel -n 4 {0} -o ./{1}".format(self.get_gff3_url(), self.species))
            os.system('echo "{0} has been in {1}"'.format(self.species + " gff", os.getcwd()))
            os.system('echo ---------------------------------------------------\n')
        except:
            os.system('echo "{0} was failed to download"'.format(self.species + " gff"))
            os.system('echo ---------------------------------------------------\n')


# def main():
#
#     species = str(input("Latin name for species (eg.Arabidopsis_thaliana): "))
#     # # get_download_url('Amborella_trichopoda')
#     species = re.sub(' ', '_', species)
#     t = Download_Ref_Genome(species)
#     t.get_gff3_url()
#     # t.download()

if __name__ == '__main__':
    # species = str(input("Latin name for species (eg.Arabidopsis_thaliana): "))
    # # get_download_url('Amborella_trichopoda')
    list = ['Beta vulgaris']
    for species in list:
        species = re.sub(' ', '_', species)
        t = Download_Ref_Genome_Ensembl_plant(species)
    # t.get_gff3_url()
        t.download_all()
