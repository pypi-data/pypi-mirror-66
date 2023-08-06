#!/usr/bin/env python3
# Script to check in WES whether the gender as determined from the bam
# (by counting mappings to chrY normalized to chrX) matches the one specified in gentli
# wdecoster

import sys
import os
import concurrent.futures as cfutures
import subprocess
import re


class Wes_sample(object):
    def __init__(self, samples):
        self.samples = samples
        self.infer_gender()

    def infer_gender(self):
        self.results = {}
        print('SampleName,yreads_count,xreads_count')
        print(self.samples)
        for sample in self.samples:
            # print(self.samples[sample])
            yreads, xreads = map(float, self.samples[sample])
            self.countratio = yreads / xreads
            if self.countratio <= 0.04:
                self.results[sample] = ','.join(
                    map(str, ['f', self.countratio]))
            else:
                self.results[sample] = ','.join(
                    map(str, ['m', self.countratio]))

        with open('infer_gender.txt','w') as f:
            for sample in self.results:
                f.write(sample+':'+self.results[sample])
                print('SampleName: gender,yreads_count/xreads_count')
                print(sample,self.results[sample],sep=':')

        #return self.results

def multi_fetch(bam, sample, bed):
    cmd = 'samtools view -@ 32 -q 5 -F 4 -R {read_group} {bam} {bed}|wc -l'.format(
        read_group=sample+'.txt', bam=bam, bed=bed)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    reads = p.communicate()[0]
    return int(reads)


def get_gender(bam):
    chrYregion = 'chrY:2649520-59034050'
    chrXregion = 'chrX:2699520-154931044'
    samples = {}
    '''Determine the gender of a bam file.
    Based on the reads mapping between but not in the PAR regions
    of the Y chromosome normalized to the counts on chromosome X'''
    assert os.path.exists(bam+'.bai') or os.path.exists(re.sub(r'.bam\b',
                                                               '.bai', bam)), 'build index for bam files firstly'
    cmd = "samtools view -H {}|grep '^@RG'|cut -f2|cut -d ':' -f2".format(bam)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    sample_list = p.communicate()[0].split(b'\n')
    for sample in sample_list:
        sample = sample.decode()
        if len(sample) != 0:
            #print(sample)
            cmd = 'echo {sample} >{sample}.txt'.format(sample=sample)
            subprocess.call(cmd, shell=True)
            xreads = multi_fetch(bam, sample, chrXregion)
            yreads = multi_fetch(bam, sample, chrYregion)
            cmd = 'rm {}.txt'.format(sample)
            subprocess.call(cmd, shell=True)
            samples[sample] = [yreads, xreads]

    return Wes_sample(samples)


def main(p_dict):
    working_space = p_dict['working_space']
    bamFiles = p_dict['bam']
    #bams = [os.path.realpath(path) for path in glob.glob(sys.argv[1] + '/*.bam')]
    bams = [file for file in os.listdir(
        working_space) if file.endswith(bamFiles)]
    # with cfutures.ProcessPoolExecutor() as executor:
    for bam in bams:
        get_gender(bam)
        #print(res.gender)
