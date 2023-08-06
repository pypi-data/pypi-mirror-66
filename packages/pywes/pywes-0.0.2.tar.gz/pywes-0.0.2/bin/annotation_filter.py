#!/usr/bin/env python3
#coding:utf-8

import re


class Filter(object):
    def __init__(self,info_dict,rsid):
        self.info_dict=info_dict
        self.rsid=rsid #self.rsid用于排查错误原因

    def filter_arg(self):
        clinvar = self.info_dict['CLINSIG'].split('|')
        clinvar = list(set(clinvar))
        freq1 = self.info_dict['gnomAD_exome_EAS']
        freq2 = self.info_dict['ExAC_EAS']
        Func_refGene = self.info_dict['Func.refGene']
        # true代表过滤，false代表保留
        if self.clinvar_filter(clinvar):# true意味着仅有benign
            return True  # 仅有benign，过滤，否则下一个判断
        elif self.Pathogenic(clinvar):  # true代表是致病的
            return False  # 致病的不能过滤，否则进行下一个判断
        elif self.population_freq(freq1, freq2):  # true意味着大于0.01
            return True  # 大于0.01就过滤，否则下一个判断
        elif self.Func(Func_refGene):  # true意味着是属于UTR3,intronic
            return True  # 属于UTR3等过滤，否则保留
        else:
            return False  # benign不是唯一值,又不是致病的，但是频率小于0.01，又不属于UTR3等，这些位点保留

    def clinvar_filter(self, clinvar):  # 删除仅有benign或者likely_benign
            """other|Benign"""
            """Pathogenic或Likely Pathogenic"""
            length = len(clinvar)
            if length == 1 and (clinvar[0] == 'Benign' or clinvar[0] == 'Likely_benign'):
                return True
            elif length == 2 and ((clinvar[0] == 'Benign' or clinvar[1] == 'Likely_benign') or (clinvar[0] == 'Likely_benign' or clinvar[1] == 'Benign')):
                return True
            else:
                False

    def Pathogenic(self, clinvar):
        clinvar_re=re.findall(r'Pathogenic','|'.join(clinvar))
        if len(clinvar_re) >= 1: # >=1意味着是致病的，['Pathogenic']
            return True
        else:
            return False


    def population_freq(self, freq1, freq2):
        if freq1 == '.':
            freq1 = 0
        if freq2 == '.':
            freq2 = 0
        freq = max(float(freq1), float(freq2))
        if freq < 0.01:
            return False
        else:
            return True

    def Func(self, Func_refGene):
        if Func_refGene == 'UTR3' or Func_refGene == 'UTR5' or Func_refGene == 'ncRNA':
            return True
        else:
            return False

    

    
