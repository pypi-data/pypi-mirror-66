#!/usr/bin/env python3
# coding:utf-8
import os
import sys
import pandas as pd
import json
from collections import defaultdict

# 获得hpo和omim表型编号的对应关系：omim.phe_hpo.phe.json，hpo和omim表型编号的对应关系，一个hpo表型编号可能对应多个omim表型编号
# 获得omim表型编号和基因的对应关系：omim_gene.json,一个omim表型编号一般对应多个基因
# 获得基因和表型的对应关系：inh_gene_phenotype.json，基因对应的遗传方式和omim表型

dirpath = os.path.dirname(sys.argv[0])
package_dirpath = os.path.dirname(dirpath)
omim_phe_hpo_phe = os.path.join(package_dirpath, 'data/omim.phe_hpo.phe')
omim_phe_hpo_phe_json = os.path.join(package_dirpath, 'data/omim.phe_hpo.phe.json')
omimdata = os.path.join(package_dirpath, 'data/omimdata.xlsx')
omim2 = os.path.join(package_dirpath, 'data/omim2.csv')
omim3 = os.path.join(package_dirpath, 'data/omim3.txt')
genemap2 = os.path.join(package_dirpath, 'data/genemap2.txt')
inh_gene_phenotype_csv = os.path.join(package_dirpath, 'data/inh_gene_phenotype.csv')
inh_gene_phenotype_json = os.path.join(package_dirpath, 'data/inh_gene_phenotype.json')
omim_gene_json = os.path.join(package_dirpath, 'data/omim_gene.json')


def hpo():
    dic = defaultdict(list)
    with open(omim_phe_hpo_phe, 'r') as f:
        for i in f:
            line = i.strip().split()
            omim = line[0]
            hp = line[1].split(':')[1]
            dic[hp].append(omim)
    with open(omim_phe_hpo_phe_json, 'w') as f:  # hpo编号和omim编号对应关系,一对多
        json.dump(dic, f)


def omim():  # 获得基因和相应的omim表型号
    df = pd.read_excel(omimdata, sheet_name='Sheet1', header=0)
    col = list(df.columns)
    phe = [v for i, v in enumerate(col) if v.find('Phenotypes') != -1]
    phenotye = phe[:]
    phe.insert(0, 'Gene Symbols')
    df = df[phe]
    df = df.fillna('.')
    for i in range(len(df)):
        for j in phenotye:
            data = df.loc[i, j]
            if data == '.':
                continue
            else:
                data = data.split(',')
                if len(data) == 1:
                    df.loc[i, j] = '.'
                else:
                    data = data[-1].split(' ')[1]
                    if data.isdigit():
                        df.loc[i, j] = data
                    else:
                        df.loc[i, j] = '.'
    df.to_csv(omim2, index=False, header=True, sep='\t')


def ff():
    with open(omim2, 'r') as f:
        next(f)
        with open(omim3, 'w') as p:  # 基因与omim表型编号对应关系
            for i in f:
                line = i.strip().split('\t')
                gene = line[0].split(',')[0]
                omim = line[1:]
                for j in omim:
                    if j != '.':
                        p.write(gene+'\t'+j+'\n')


def final():
    dic = defaultdict(list)
    df = pd.read_table(omim3, header=None)
    df.columns = ['gene', 'omim_phe']
    df = df.applymap(str)
    for i in range(len(df)):
        omim = df.loc[i, 'omim_phe']
        gene = df.loc[i, 'gene']
        if gene not in dic[omim]:
            dic[omim].append(gene)  # omim编号和基因对应关系，一对多
    return dic


def ad_gene_phe():  # 得到gene:[inheritance,phenotype]对应关系，进行后面的omim数据注释
    df1 = pd.read_excel(omimdata, header=0, sheet_name='Sheet1')
    df1 = df1[['Gene Symbols', 'MOI']]
    df1['Approved Symbol'] = ''
    df1 = df1.fillna('.')
    df1['Approved Symbol'] = df1['Gene Symbols'].map(lambda x: x.split(',')[0])
    df1 = df1.drop('Gene Symbols', axis=1)
    df2 = pd.read_table(genemap2, header=3)
    df2 = df2[['Approved Symbol', 'Phenotypes']]
    df = pd.merge(df1, df2)
    df.columns = ['inheritance', 'gene', 'phenotype']
    df = df.fillna('.')
    df.to_csv(inh_gene_phenotype_csv, header=True,
              index=False, sep='\t', encoding='utf_8')


# 获得基因和表型的对应关系：inh_gene_phenotype.json
def gene_phe():  # 存成json格式
    dic = {}
    with open(inh_gene_phenotype_csv, 'r') as f:
        next(f)
        for i in f:
            line = i.strip().split('\t')
            gene = line[1]
            inheritance = line[0]
            phenotype = line[2]
            dic[gene] = [inheritance, phenotype]
    with open(inh_gene_phenotype_json, 'w') as f:
        json.dump(dic, f)


def main():
    hpo()
    omim()
    ff()
    dic = final()
    # 根据hpo号得到omim表型号，再根据omim表型号得到gene
    # omim.phe_hpo.phe.json->omim_gene.json
    with open(omim_gene_json, 'w') as f:
        json.dump(dic, f)
    ad_gene_phe()
    gene_phe()
