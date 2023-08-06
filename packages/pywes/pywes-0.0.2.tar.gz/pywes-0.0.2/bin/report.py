#!/usr/bin/env python3
#coding:utf-8
import sys
import os
import pandas as pd

pos_list=[0,2,3,4,5,6,7,8,9,12,20,21,22,23,24,26,27,28,29,34,36,37,38,39,40]
def report(path):
    r_list=[]
    path=os.path.join(path,'coverage.report')
    with open(path,'r') as f:
        for i in f:
            if i.startswith('#'):
                continue
            else:
                line=i.strip()
                r_list.append(line)
    f_list=[r_list[i] for i in pos_list]
    return f_list


def write_cov(f_list):
    output=os.path.basename(path)
    with open(output+'_simple_covreport.txt','w') as f:
        for line in f_list:
            f.write(line + '\n')
    output=os.path.join(path,'depth.tsv.gz')
    df=pd.read_table(output,header=0)
    out=df['Raw Depth'].describe()
    out.to_csv(path+'_describe.txt')


if __name__ == '__main__':
    path=sys.argv[1]
    path=os.path.abspath(path)
    f_list=report(path)
    write_cov(f_list)



