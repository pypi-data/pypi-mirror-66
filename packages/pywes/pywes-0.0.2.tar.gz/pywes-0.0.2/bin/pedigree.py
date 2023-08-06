#!/usr/bin/env python3
# coding:utf-8

import gzip
import os
from collections import defaultdict
from collections import OrderedDict
from annotation_filter import Filter
from hgvs import AA_change
from vcf_split import VCFSplit
import pandas as pd
import json
from acmg_rank import Rank
import pysam


class Pedigree(VCFSplit):

    def __init__(self, vcf, rank_dict, child, father, mother):
        super(Pedigree, self).__init__(vcf, rank_dict)
        self.child = child
        self.father = father
        self.mother = mother



    def get_father_mother_GT(self, rec:'VariantFileRecord') -> str:
        for sampleRecorde in rec.samples.values():
            if sampleRecorde.name == self.father:
                father_gt = '/'.join([str(s) for s in sampleRecorde['GT']])
            elif sampleRecorde.name == self.mother:
                mother_gt = '/'.join([str(s) for s in sampleRecorde['GT']])
            else:
                continue
        return father_gt+'|'+mother_gt


    def father_mother_gt_pattern(self) -> dict:
        # get father mother genotype and child genetic pattern
        vcf=pysam.VariantFile(self.vcf)
        sample_list=list(vcf.header.samples)
        assert len(sample_list) == 3,'only support trio sample,the number of sample should equal to 3'
        assert self.child in sample_list and self.father in sample_list and self.mother in sample_list,'child,father,mother mismatch'
        chr_pos_father_mother_GT = defaultdict(dict)
        genetic_pattern_dict = defaultdict(dict)
        for rec in vcf.fetch():
            chr= rec.chrom
            pos=str(rec.pos)
            try:
                genetic_pattern=rec.info['genetic_pattern'][0]
                #print(genetic_pattern)
            except KeyError:
                print('{} should be run with trio module firstly'.format(self.vcf))
            father_mother_GT = self.get_father_mother_GT(rec)
            chr_pos_father_mother_GT[chr][pos] = father_mother_GT
            genetic_pattern_dict[chr][pos] = genetic_pattern

        vcf.close()
        return chr_pos_father_mother_GT, genetic_pattern_dict
            

    def merge(self):
        chr_pos_father_mother_GT, genetic_pattern_dict =self.father_mother_gt_pattern()
        f = ['filter', 'withoutfilter']
        module_child_dir=os.path.join(self.module,self.child)
        print('mergy')
        for filter_type in f:
            child = pd.read_table(os.path.join(module_child_dir,'{module}.{child}.{variant_type}.annovar.{filter_type}.csv'.format(
                module=self.module,child=self.child, variant_type=self.variant_type, filter_type=filter_type)), sep=',', header=0, low_memory=False)

            # 孩子样本需要增加父母的基因型以及遗传模式（genetic pattern）
            col_name = child.columns.tolist()
            col_name.insert(col_name.index('GT')+1, 'father_mother_GT(f|m)')
            col_name.insert(col_name.index('phenotype')+1, 'genetic_pattern')
            child = child.reindex(columns=col_name)
            child['father_mother_GT(f|m)'] = child.apply(lambda x: chr_pos_father_mother_GT[x['chr']][str(x['hg38_position'])], axis=1)
            child['genetic_pattern'] = child.apply(lambda x: genetic_pattern_dict[x['chr']][str(x['hg38_position'])], axis=1)
            # 父母样本不需要genetic_pattern列,父母孩子在先前已经基因型过滤
            child.to_csv(os.path.join(module_child_dir,'{module}.{child}.{variant_type}.annovar.{filter_type}.csv'.format(
                module=self.module,child=self.child, variant_type=self.variant_type, filter_type=filter_type)), index=False, header=True)
            


def main(p_dict):
    vcf = p_dict['vcf']
    intervar = p_dict['rank']
    if intervar == None:
        rank_dict = defaultdict(dict)
    else:
        rank = Rank(intervar)  # 实例化Intervar分级结果
        rank_dict = rank.variant_rank_auto()
    child = p_dict['child']
    father = p_dict['father']
    mother = p_dict['mother']
    variant = ['snp', 'indel']
    result = Pedigree(vcf, rank_dict, child, father, mother)
    for variant_type in variant:
        result.variant_type = variant_type
        result.sample_split()
        result.sample_split(block=False)
        result.merge()
