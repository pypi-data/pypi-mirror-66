#!/usr/bin/env python2
# coding:utf-8

import subprocess
from collections import defaultdict
import gzip
import os,sys


class Hg38ToHg19(object):
    def __init__(self, vcf):
        self.vcf = vcf
        self.write_bed()
        self.liftOver()


    def write_bed(self):
        if self.vcf.endswith('.gz'):
            input = gzip.open(self.vcf, 'rt')
        else:
            input = open(self.vcf, 'rt')
        with open('hg38.bed', 'wt') as f:
            for i in input:
                if i.startswith('#'):
                    continue
                else:
                    line = i.split()
                    chr = line[0]
                    pos = line[1]
                    out = [chr, int(pos)-1, pos, chr, pos]
                    out = map(str, out)
                    f.write('\t'.join(out)+'\n')
        input.close()
        # cmd = "less  {vcf} |grep -v '^#'|awk '{arg}' >hg38.bed".format(
        #     vcf=self.vcf, arg='{print $1,$2-1,$2,$1,$2}')
        # subprocess.call(cmd, shell=True)
        return None

    def liftOver(self):
        dirpath=os.path.dirname(sys.argv[0])
        package_dirpath=os.path.dirname(dirpath)
        hg38ToHg19_over_chain=os.path.join(package_dirpath,'data/hg38ToHg19.over.chain.gz')
        assert os.path.exists(hg38ToHg19_over_chain),'{} does not exist,it should locate in parent package/data directory'.format(hg38ToHg19_over_chain)
        cmd = 'liftOver hg38.bed {} hg19.bed unmap'.format(hg38ToHg19_over_chain)
        subprocess.call(cmd, shell=True)
        return None

    def get_bed(self):
        with open('hg19.bed', 'rt') as f:
            for i in f:
                line = i.strip().split()
                yield line

    def hg19_position(self):
        hg38_hg19 = defaultdict(dict)
        for line in self.get_bed():
            chr = line[3]
            hg38_position = line[4]
            _hg19_position = line[2]
            hg38_hg19[chr][hg38_position] = _hg19_position
        return hg38_hg19
