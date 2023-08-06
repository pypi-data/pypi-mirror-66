#!/usr/bin/env python3
# coding:utf-8
import json
import sys
import pandas as pd
import os


class Gene(object):
    dirpath=os.path.dirname(sys.argv[0])
    package_dirpath=os.path.dirname(dirpath)
    
    def __init__(self, hpo, csv_list):
        self.hpo = hpo
        self.csv_list = csv_list
        self.samples = self.get_csvs()

    def omim_gene(self):  # omim表型编号和基因对应关系
        omim_gene_json=os.path.join(self.package_dirpath,'data/omim_gene.json')
        assert os.path.exists(omim_gene_json),'{} does not exist,it should locate in parent package/data directory'.format(omim_gene_json)
        with open(omim_gene_json, 'r') as f:
            for i in f:
                omim = json.loads(i)
        return omim

    def hpo_phe(self):  # hpo表型编号和omim表型编号对应关系
        omim_phe_hpo_phe_json=os.path.join(self.package_dirpath,'data/omim.phe_hpo.phe.json')
        assert os.path.exists(omim_phe_hpo_phe_json),'{} does not exist,it should locate in parent package/data directory'.format(omim_phe_hpo_phe_json)
        with open(omim_phe_hpo_phe_json, 'r') as f:
            for i in f:
                omim_hpo = json.loads(i)
        return omim_hpo

    def get_hpo(self):  # 获取hpo编号列表
        hpo_list = []
        with open(self.hpo, 'r') as f:
            for i in f:
                line = i.strip().split(':')[-1]
                hpo_list.append(line)
        return hpo_list

    def get_gene(self):
        hpo_list = self.get_hpo()
        omim = self.omim_gene()
        omim_hpo = self.hpo_phe()
        genes = []
        for hpo in hpo_list:
            omim_number_list = omim_hpo.get(hpo, 'no_hpo_number')  # 根据hpo编号获得omim表型编号列表
            if omim_number_list == 'no_hpo_number':
                gene = hpo+'\t'+'no_hpo_number'
                genes.append(gene)
            else:
                for omim_num in omim_number_list:
                    gene_list = omim.get(omim_num, 'no_omim_number')  # 根据omim表型编号获得gene列表
                    if gene_list == 'no_omim_number':
                        gene = hpo+'\t'+omim_num+'\t'+'no_omim_number'
                        genes.append(gene)
                    else:
                        for g in gene_list:
                            gene = hpo+'\t'+omim_num+'\t'+g
                            genes.append(gene)

        genes=list(set(genes))#去重复
        genes=sorted(genes,key=lambda x:int(x.split()[0]))
        return genes

    def write_gene(self):
        self.genes = self.get_gene()
        with open('gene.txt', 'w') as f:
            for i in self.genes:
                f.write(i+'\n')

    def get_csvs(self):
        samples = []
        with open(self.csv_list, 'r') as f:
            for i in f:
                samples.append(i.strip())
        return samples

    def csv_filter(self):
        self.genes = [i.split()[-1] for i in self.genes]
        print (self.genes)
        for sample in self.samples:
            print ('panel.'+sample)
            df = pd.read_csv(sample, header=0,low_memory=False)
            df = df[df['Gene.refGene'].isin(self.genes)]#根据基因列表进行筛选
            out = os.path.basename(sample)
            df.to_csv('panel.'+out, index=False, header=True)


def main(p_dict):
    hpo = p_dict['hpo']
    csv_list = p_dict['csv']
    result = Gene(hpo, csv_list)
    result.write_gene()
    result.csv_filter()
