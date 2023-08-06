#!/usr/bin/env python3
# coding:utf-8

import pysam
import os
import re
import sys
from collections import defaultdict
from collections import OrderedDict
from hg38Tohg19 import Hg38ToHg19
from hgvs import AA_change
from annotation_filter import Filter
import json
from acmg_rank import Rank
#import pysnooper
#from stat_check import Stat
import logging


class VCFSplit(object):
    title1 = ['chr', 'hg38_position', 'hg19_position', 'rsid', 'ref', 'alt', 'qual', 'filter',
              'GT', 'RefDepth', 'Alt1Depth', 'Alt2Depth', 'totalDP', 'genotype_quality', 'match_transcript', 'inheritance', 'phenotype', 'ACMG_rank']

    def __init__(self, vcf:'VariantFile', rank_dict:dict,variant_type = 'snp'):
        self.vcf = vcf
        self.rank_dict = rank_dict
        self.variant_type = variant_type
        self.hg38_hg19 = self.coordinate()
        self.title2 = self.get_title2()
        self.title = self.title1 + self.title2
        print(self.title,sep='\t')
        self.gene_phe = self.gene_phenotype()


    def coordinate(self) -> dict:
        if not hasattr(self, "hg38_hg19"):
            hg38_hg19 = Hg38ToHg19(self.vcf).hg19_position()
        return hg38_hg19

    def get_title2(self) -> list :
        # title2=[]# 对应下面输出文件表头的第二部分
        # title2(Func.refGene->MutationAssessor_pred)
        vcf = pysam.VariantFile(self.vcf)
        # self.vcf_header=re.findall(r'(#CHROM.*)',str(vcf.header))[0]
        if not hasattr(self, 'title2'):
            for rec in vcf.fetch():
                info = rec.info.keys()
                start, end = info.index('Func.refGene'), info.index(
                    'MutationAssessor_pred')
                title2 = info[start:end+1]
                break
        vcf.close()
        return title2

    def snp_or_indel(self, ref:str, alt:tuple) -> str:
        # infer variant type
        #alt = alt.split('/')
        alt = sorted(alt, key=lambda x: len(x), reverse=False)[-1]
        if len(ref) > 1 or len(alt) > 1:
            return 'indel'
        else:
            return 'snp'

    def indel_pos_allele(self, pos:int, ref:str, alt:tuple) -> str:
        # there could be more than two alternative allele
        # get indel true position,return type is string
        alt = re.split(r'([^\/]+)\/([\w\/]+)', '/'.join(alt))
        if '' in alt:
            alt.remove('')
        alt = alt[0]
        if len(ref) > len(alt):
            head = ref[0:len(alt)]
            if head == alt:
                start = str(pos+len(head))
            else:
                start = pos
        else:
            head = alt[0:len(ref)]
            if head == ref:
                start = str(pos+len(ref)-1)
            else:
                start = pos
        return str(start)

    #@pysnooper.snoop('test.log')
    def parse_vcf(self, cut=True) -> None:
        # get sample_dict,contain samples record
        #self.rsid用于排查错误原因
        #tt=time.clock()
        self.sample_dict = defaultdict(list)
        vcf = pysam.VariantFile(self.vcf)
        for rec in vcf.fetch():
            chr, pos, self.rsid, ref, alt, qual = rec.chrom, rec.pos, rec.id, rec.ref, rec.alts, rec.qual
            hg19_position = self.hg38_hg19[chr].get(str(pos), 'delete')
            if self.variant_type == self.snp_or_indel(ref, alt):
                if self.variant_type == 'indel':
                    start = self.indel_pos_allele(pos, ref, alt)
                else:
                    start = str(pos)
                ACMG_rank = self.rank_dict.get(chr,{}).get(start, '.')
                filter_ = rec.filter.keys()[0]
                if filter_ == 'PASS':
                    basic_data = [chr, pos, hg19_position,
                                  self.rsid, ref, '/'.join(alt), qual, filter_]
                    info = rec.info.keys()
                    # 寻找Func.refGene作为开始点，MutationAssessor_pred作为终止点
                    start, end = info.index('Func.refGene'), info.index('MutationAssessor_pred')
                    info = info[start:end+1]
                    info_dict = OrderedDict()
                    for key in info:
                        value = '/'.join(rec.info[key]).replace(',', '/')
                        info_dict[key] = str(value)
                    info_dict_OrderedValues = list(info_dict.values())
                    AA_value = info_dict['AAChange.refGene']
                    match_transcript = AA_change(AA_value, self.variant_type).std_AA()
                    gene = info_dict['Gene.refGene']
                    inheritance, phenotype = self._gene_phe(gene)
                    omim = [match_transcript, inheritance, phenotype, ACMG_rank]
                    if cut:  # true代表对文件过滤，false表示不过滤
                        # 为真就过滤掉不符合条件的变异结果，反之结果保留，判断语句在annotation_filter.py中
                        __filter = Filter(info_dict,self.rsid)
                        if __filter.filter_arg():
                            # if self.rsid == 'rs1799983':
                            #     print(1)
                            continue
                        else:
                            self.sample_record_filter(
                                rec, basic_data, omim, info_dict_OrderedValues)
                    else:
                        self.sample_record_filter(
                            rec, basic_data, omim, info_dict_OrderedValues)

        vcf.close()
        print(self.variant_type,'filter={}'.format(cut))
        return None
        #ee=time.clock()
        #print(ee-tt)

    def sample_record_filter(self, rec:'VariantFileRecord', basic_data:list, omim:list, info_dict_OrderedValues:list) :
        #  update self.sample_dict
        for sampleRecord in rec.samples.values():
            try:
                GT = sampleRecord['GT']
                AD = sampleRecord['AD']
                genotype_quality = sampleRecord['GQ'] #int
                totalDP = sampleRecord['DP']
                if GT.__eq__((0, 0)) or GT.__eq__((None, None)) or GT.__eq__((None,)):
                    continue
                else:
                    try:
                        RefDepth = AD[0]
                        Alt1Depth = AD[1]
                    except IndexError:
                        continue
                    if totalDP == None or genotype_quality == None or genotype_quality < 20:
                        continue
                    else:
                        Alt2Depth = int(totalDP)-int(RefDepth)-int(Alt1Depth)
                    sample_data = ['/'.join(str(s) for s in GT), RefDepth, Alt1Depth,
                                   Alt2Depth, totalDP, genotype_quality]
                    all = basic_data+sample_data+omim+info_dict_OrderedValues
                    self.sample_dict[sampleRecord.name].append(all)

            except KeyError:
                continue
                
    def gene_phenotype(self) -> dict:  # 匹配基因对应的表型和遗传方式，AD,AR,XL
        # gene:[inheritance,phenotype]
        dirpath = os.path.dirname(sys.argv[0])
        package_dirpath = os.path.dirname(dirpath)
        inh_gene_phenotype_json = os.path.join(
            package_dirpath, 'data/inh_gene_phenotype.json')
        assert os.path.exists(
            inh_gene_phenotype_json), '{} does not exist,it should locate in parent package/data directory'.format(inh_gene_phenotype_json)
        if not hasattr(self, 'gene_phe'):
            with open(inh_gene_phenotype_json, 'r') as f:
                for i in f:
                    gene_phe = json.loads(i)
        return gene_phe

    def _gene_phe(self, gene) -> tuple:
        inh_phe = self.gene_phe.get(gene, '.')
        if inh_phe == '.':
            inheritance, phenotype = '.', '.'
        else:
            inheritance, phenotype = inh_phe
        inheritance = inheritance.replace(',', '/')
        phenotype = phenotype.replace(',', '_')
        return inheritance, phenotype

    def output_name(self, cut=True) -> str:
        if cut:
            output = '.{}.annovar.filter.csv'.format(self.variant_type)
        else:
            output = '.{}.annovar.withoutfilter.csv'.format(self.variant_type)
        return output

    #@pysnooper.snoop('test.log')
    def sample_split(self, cut=True):
        self.module = sys.argv[1]
        self.parse_vcf(cut)
        now_path=os.path.abspath('./')
        try:
            print('you can find the csv result in {} directory'.format(self.module))
            os.mkdir('{}'.format(self.module))
        except OSError:
            print('carrier exists,reuse it')
            pass
        os.chdir('{}'.format(self.module))
        for sample in self.sample_dict:
            try:
                os.mkdir(sample)
            except OSError:
                print('{} exists,reuse it'.format(sample))
                pass
            output = self.module + '.' + sample + self.output_name(cut)
            print('create {}'.format(output))
            with open(os.path.join(sample,output), 'wt') as f:
                f.write(','.join(self.title)+'\n')
                for sample_list in self.sample_dict[sample]:
                    sample_list = map(str, sample_list)
                    f.write(','.join(sample_list)+'\n')
        os.chdir(now_path)


def main(p_dict:dict):
    logging.basicConfig(level=logging.CRITICAL,filename='carrier.log')
    logging.critical('')
    #Stat().stat()
    vcf = p_dict['vcf']
    intervar = p_dict['rank']
    if intervar == None:
        rank_dict = defaultdict(dict)
    else:
        rank = Rank(intervar)  # 实例化Intervar分级结果
        rank_dict = rank.variant_rank_auto()
    variant = ['snp', 'indel']
    result = VCFSplit(vcf, rank_dict)
    for variant_type in variant:
        result.variant_type = variant_type
        result.sample_split()
        result.sample_split(cut=False)
    del result.sample_dict
    #Stat().stat()
    


