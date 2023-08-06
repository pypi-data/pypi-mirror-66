#!/usr/bin/env python3
# coding:utf-8


import os
import sys
import pysam


class Trio(object):
    # child:father:mother:genetic_pattern
    t0 = {0: {0: {0: 'anyway', 1: 'anyway', 2: 'back_mutation'}, 1: {0: 'anyway', 1: 'anyway',
                                                                     2: 'back_mutation'}, 2: {0: 'back_mutation', 1: 'back_mutation', 2: 'back_mutation'}}}
    t1 = {1: {0: {0: 'denovo', 1: 'M_HET', 2: 'M_HOM'}, 1: {0: 'F_HET',
                                                            1: 'Unknown', 2: 'M_HOM'}, 2: {0: 'F_HOM', 1: 'F_HOM', 2: 'back_mutation'}}}
    t2 = {2: {0: {0: 'denovo', 1: 'denovo', 2: 'denovo'}, 1: {0: 'denovo', 1: 'F_HET_M_HET',
                                                              2: 'F_HET_M_HOM'}, 2: {0: 'denovo', 1: 'F_HOM_M_HET', 2: 'F_HOM_M_HOM'}}}
    trio = {}
    trio.update(t0)
    trio.update(t1)
    trio.update(t2)

    def __init__(self, vcf, child, father, mother):
        self.vcf = vcf
        self.child = child
        self.father = father
        self.mother = mother

    def get_child_father_mother_GT(self, rec):
        for sampleRecorde in rec.samples.values():
            if sampleRecorde.name == self.father:
                father_gt = '/'.join(str(s) for s in sampleRecorde['GT'])
            elif sampleRecorde.name == self.mother:
                mother_gt = '/'.join(str(s) for s in sampleRecorde['GT'])
            else:
                child_gt = '/'.join(str(s) for s in sampleRecorde['GT'])

        return child_gt, father_gt, mother_gt

    def parse_vcf(self):
        _tran = {'0/0': 0, '0/1': 1, '1/1': 2, '0|0': 0, '0|1': 1, '1|1': 2}
        vcf = pysam.VariantFile(self.vcf)
        vcf.header.info.add('genetic_pattern', '.', 'String',
                            "genetic pattern made by lianlin")
        sample_list = list(vcf.header.samples)
        assert len(
            sample_list) == 3, 'only support trio sample,the number of sample should equal to 3'
        assert self.child in sample_list and self.father in sample_list and self.mother in sample_list, 'child,father,mother mismatch'
        for rec in vcf.fetch():
            child_gt, father_gt, mother_gt = self.get_child_father_mother_GT(
                rec)
            child_gt = _tran.get(child_gt, 'invalid')
            father_gt = _tran.get(father_gt, 'invalid')
            mother_gt = _tran.get(mother_gt, 'invalid')
            if child_gt == 'invalid' or father_gt == 'invalid' or mother_gt == 'invalid':
                # 大写Unknown代表三人都是杂合情况，小写unknown代表基因型无法判断的情况
                genetic_pattern = 'unknown'
                rec.info['genetic_pattern'] = genetic_pattern
            else:
                genetic_pattern = self.trio.get(child_gt, {}).get(
                    father_gt, {}).get(mother_gt, 'unknown')
                rec.info['genetic_pattern'] = genetic_pattern
            print(genetic_pattern)
            yield rec
        vcf.close()

    def vcf_out(self):
        module = sys.argv[1]
        outprefix = module + '.' + os.path.basename(self.vcf)
        vcf_in = pysam.VariantFile(self.vcf)
        vcf_in.header.add_line(
            '##INFO=<ID=genetic_pattern,Number=.,Type=String,Description="genetic pattern made by lianlin">')
        vcf_in.header.add_line('##Conmand={}>'.format(' '.join(sys.argv)))
        vcf_out = pysam.VariantFile(outprefix, 'w', header=vcf_in.header)
        for rec in self.parse_vcf():
            vcf_out.write(rec)
        print('the result is {}'.format(outprefix))
        vcf_in.close()
        vcf_out.close()


def main(p_dict):
    vcf = p_dict['vcf']
    child = p_dict['child']
    father = p_dict['father']
    mother = p_dict['mother']
    result = Trio(vcf, child, father, mother)
    result.vcf_out()
