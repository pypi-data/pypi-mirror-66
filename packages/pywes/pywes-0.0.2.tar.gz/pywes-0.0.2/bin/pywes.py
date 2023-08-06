#!/usr/bin/env python3
# coding:utf-8

import argparse
import sys
import trio
import subprocess
import omim_match
import database_format
import vcf_split
import wes
import pedigree
import infer_gender

parser = argparse.ArgumentParser(
    description='whole exome analysis workflow made by lianlin')
subparsers = parser.add_subparsers(
    help='Select pywes action among the following options: ', dest='pygenetic_action')
parser_wes = subparsers.add_parser('wes', help='wes analysis pipeline.')
parser_carrier = subparsers.add_parser(
    'carrier', help='vcf file further annotation and filter.')
parser_trio = subparsers.add_parser(
    'trio', help='predict inheritance pattern when use trio vcf,should only contain three samples belong to the same family.')
parser_pedigree = subparsers.add_parser(
    'pedigree', help='pedigree vcf file further annotation and filter.')
parser_panel = subparsers.add_parser(
    'panel', help='annotation result filter according to gene panel.')
parser_infer_gender = subparsers.add_parser(
    'gender', help='sex prediction.')
parser_database = subparsers.add_parser(
    'database', help='database update.')

# wes argument
parser_wes.add_argument(
    '-i', '--input', help='configure file', required=True)
parser_wes.add_argument(
    '-r', '--run', choices={'on','off'},help='run on or run off,default off',default='off')

# carrier arguments

parser_carrier.add_argument(
    '-vcf', '--vcf', help='annoted vcf file from annovar software', required=True)
parser_carrier.add_argument(
    '-r', '--rank', help='variant rank according to ACMG guideline', required=False)
# parser_carrier.add_argument(
#     '-t', '--variant_type', help='SNP or INDEL', required=True)

# trio arguments
parser_trio.add_argument('-vcf', '--vcf', help='vcf file', required=True)
parser_trio.add_argument(
    '-c', '--child', help='child sample ID', required=True)
parser_trio.add_argument(
    '-f', '--father', help='father sample ID', required=True)
parser_trio.add_argument(
    '-m', '--mother', help='mother sample ID', required=True)
    
# pedigree arguments
parser_pedigree.add_argument(
    '-vcf', '--vcf', help='annoted vcf file from annovar software', required=True)
parser_pedigree.add_argument(
    '-rank', '--rank', help='variant rank according to ACMG guideline', required=False)
parser_pedigree.add_argument(
    '-c', '--child', help='child sampleID', required=True)
parser_pedigree.add_argument(
    '-f', '--father', help='father sampleID', required=True)
parser_pedigree.add_argument(
    '-m', '--mother', help='mother sampleID', required=True)

# panel arguments
parser_panel.add_argument(
    '-hpo', '--hpo', help='hpo phenotype code', required=True)
parser_panel.add_argument(
    '-c', '--csv', help='csv list,each csv each row', required=True)


# infeer_gender arguments
parser_infer_gender.add_argument(
    '-b', '--bam', help='bam files ,you can also use wildcard character,e.g dedup.bam', default='.bam')
parser_infer_gender.add_argument(
    '-w', '--working_space', help='bam files will be collected in provided working directory', required=True)
# database arguments
# actually,no argument


def main():
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    parameters = parser.parse_args()
    p_dict = vars(parameters)
    action = p_dict['pygenetic_action']
    if action == 'wes':
        wes.main(p_dict)
    elif action == 'carrier':
        vcf_split.main(p_dict)
    elif action == 'trio':
        trio.main(p_dict)
    elif action == 'pedigree':
        pedigree.main(p_dict)
    elif action == 'panel':
        omim_match.main(p_dict)
    elif action == 'gender':
        infer_gender.main(p_dict)
    elif action == 'database':
        database_format.main()


if __name__ == '__main__':
    main()
