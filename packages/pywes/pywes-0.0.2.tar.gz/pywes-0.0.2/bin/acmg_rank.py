#!/usr/bin/env python3
#coding:utf-8

from collections import defaultdict
import re


class Rank(object):
    def __init__(self,intervar):
        self.intervar=intervar


    def variant_rank_auto(self):
        rank_dict=defaultdict(dict)
        with open(self.intervar,'rt') as f:
            next(f)
            for i in f:
                line=i.split('\t')
                chr=line[0]
                start=line[1]
                rank=line[13].replace(',','\t')
                rank=re.sub(r'^\s+InterVar:\s+','',rank)
                rank_dict['chr'+chr][start]=rank
                #print(rank)
        #print(rank_dict['chr1']['1043223'])
        return rank_dict
