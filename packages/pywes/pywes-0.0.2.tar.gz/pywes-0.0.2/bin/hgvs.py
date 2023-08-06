#!/usr/bin/env python3
# coding:utf-8


class AA_change(object):
    def __init__(self, value, variant_type):
        self.value = value
        self.variant_type = variant_type


    def std_AA(self):  # 修改AAChange.refGene栏中碱基替换的格式，如果是插入缺失则不改变，仅输出转录本号数值最小的那个
        if self.value == '.' or self.value == 'UNKNOWN':
            match_transcript = '.'
        else:
            value = self.value.split('/')
            if len(value) == 1:
                match_transcript = value[0].split(':')
                match_transcript = self.std(match_transcript)
            else:
                match_transcript = self.get_NM_min(value).split(':')
                match_transcript = self.std(match_transcript)

        return match_transcript

    def std(self, match_transcript):  # 输出标准格式，NM_013296(GPSM2):c.379C>T (p.R127*)
        if self.variant_type == 'snp':
            gene = match_transcript[0]
            transcipt_number = match_transcript[1]
            cDNA = match_transcript[3]
            protein = match_transcript[4]
            _ = cDNA.split('.')[1]
            ori = _[0]
            bed = _[1:-1]
            change = _[-1]
            cDNA = 'c.' + bed + ori + '>' + change
            match_transcript = transcipt_number + \
                '('+gene+')' + ':'+cDNA+'('+protein+')'
        else:
            gene = match_transcript[0]
            transcipt_number = match_transcript[1]
            if len(match_transcript) >= 5:
                cDNA = match_transcript[3]
                protein = match_transcript[4]
                match_transcript = transcipt_number + \
                    '('+gene+')' + ':'+cDNA+'('+protein+')'
            else:
                _ = ':'.join(match_transcript[2:])
                match_transcript = transcipt_number+'('+gene+')' + ':' + _
        return match_transcript

    def get_NM_min(self, value):  # 获得转录本号数值最小的那个转录本
        _ = []
        for nm in value:
            transcipts = nm.split(':')
            number = transcipts[1].split('_')[1]
            pos = [i for i, v in enumerate(number) if v != '0'][0]
            _.append(float(number[pos:]))
        nm_pos = _.index(min(_))
        match_transcript = value[nm_pos]
        return match_transcript

    
