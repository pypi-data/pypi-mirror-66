#!/usr/bin/env python3
# coding:utf-8

import os
import time
import sys
import subprocess
from collections import defaultdict


class Wes(object):

    trimmomatic = "/share/data1/local/bin/trimmomatic-0.38.jar"
    gatk = "/share/data1/src/gatk/gatk"
    seqtk = "/share/data1/src/bwa/bwakit/seqtk"
    alt = "/share/data1/genome/hs38DH.fa.alt"
    annovar = "/share/data1/src/annovar"
    Intervar = "/share/data3/lianlin/soft/InterVar-master/Intervar2.py"
    bamdst = "/share/data3/lianlin/soft/bamdst/bamdst"
    dbsnp = "/share/data1/PublicProject/GATK_bundle/dbsnp150_chr.vcf.gz"
    indel = "/share/data1/PublicProject/GATK_bundle/Mills_and_1000G_gold_standard.indels.hg38.vcf.gz"
    snp = "/share/data1/PublicProject/GATK_bundle/1000G_phase1.snps.high_confidence.hg38.vcf.gz"
    bed = "/share/data2/leon/exom_bed/S07084713_Regions.bed"
    interval = "/share/data2/leon/exom_bed/list.interval_list"
    reference = "/share/data1/genome/hs38DH.fa"
    ip = 100

    def __init__(self, input):
        self.input = input
        self.group()

    def create_working_space(self):
        try:
            if not os.path.exists(self.working_space):
                os.mkdir(self.working_space)
                sys.stdout.write('mkdir {}  directory\n'.format(
                    self.working_space))
            else:
                os.removedirs(self.working_space)
                os.mkdir(self.working_space)
                sys.stdout.write('delete this empty directory {}\n'.format(
                    self.working_space))
        except OSError:
            sys.stdout.write('mkdir {}  directory.\n'.format(
                self.working_space))
            sys.stdout.write('directory is not empty,make sure first:{}.\nexit!\n'.format(
                self.working_space))
            sys.exit()

    def group(self):
        self.groups = defaultdict(list)
        self.working_space = ''
        row_line = 0
        with open(self.input, 'r') as f:
            for i in f:
                if row_line > 0:
                    row_line += 1
                    line = i.strip().split()
                    if len(line) == 5:
                        sample = line[4]
                        self.groups[sample].append(line)
                    else:
                        sys.stdout.write('it seem has less or more than five items in the {} row,it may be a blank row,so pass it and continue\n'.format(
                            row_line))
                else:
                    self.working_space = i.strip().split()
                    assert len(
                        self.working_space) == 1, 'please use batch number,e.g. gmb1,gmb2 ...'
                    self.working_space = self.working_space[0]
                    self.create_working_space()
                    self.working_space = os.path.abspath(self.working_space)
                    row_line += 1

    def info_list_by_sample(self):
        for sample in self.groups:
            info_list = self.groups[sample]
            # each sample may contain more than one library id,these sample will be merge in markduplicate step.
            yield info_list

    def trim(self):
        for info_list in self.info_list_by_sample():
            part = []
            for parallel_sample in info_list:
                fq1, fq2, adapter, library, sample = parallel_sample
                # only accept nextera or truseq adapter
                if adapter.lower() == 'truseq':
                    trim = 'java -jar {tool} PE -threads 14 -phred33 {fq1} {fq2} {library}.{sample}_r1.fq.gz {library}.{sample}_r1_unpaired.fq.gz {library}.{sample}_r2.fq.gz {library}.{sample}_r2_unpaired.fq.gz ILLUMINACLIP:{trimmomatic_dir}/adapters/TruSeq3-PE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36 &'.format(
                        tool=self.trimmomatic, trimmomatic_dir=os.path.dirname(self.trimmomatic), fq1=fq1, fq2=fq2, library=library, sample=sample)
                elif adapter.lower() == 'nextera':
                    trim = 'java -jar {tool} PE -threads 14 -phred33 {fq1} {fq2} {library}.{sample}_r1.fq.gz {library}.{sample}_r1_unpaired.fq.gz {library}.{sample}_r2.fq.gz {library}.{sample}_r2_unpaired.fq.gz ILLUMINACLIP:{trimmomatic_dir}/adapters/NexteraPE-PE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36 &'.format(
                        tool=self.trimmomatic, trimmomatic_dir=os.path.dirname(self.trimmomatic), fq1=fq1, fq2=fq2, library=library, sample=sample)
                else:
                    sys.stdout.write('{} :\nadaptor error, only Nextera or Truseq accept,lower or upper dose not matter\n'.format(
                        adapter))
                    sys.exit()
                part.append(trim)
            part.append('wait ;')
            yield part, info_list

    def bwa(self):
        for part, info_list in self.trim():
            for parallel_sample in info_list:
                *_, library, sample = parallel_sample
                bwa = 'mergeps.o {library}.{sample}_r1.fq.gz {library}.{sample}_r2.fq.gz |bwa mem -p -t 14 -R"@RG\\tID:{batch_library}\\tLB:{library}\\tSM:{sample}\\tPU:flowcell\\tPL:Illumina" {reference} - 2>{library}.{sample}.log.bwamem |k8 {bwa_dir}/bwa-postalt.js -p {library}.hla {alt} | samtools sort -@ 2 -m8g - -o {library}.{sample}.aln.bam ;'.format(
                    reference=self.reference, bwa_dir=os.path.dirname(self.seqtk), alt=self.alt, library=library, batch_library=os.path.basename(self.working_space)+'_'+library, sample=sample)
                part.append(bwa)
            yield part, info_list

    def MarkDup(self):
        for part, info_list in self.bwa():
            bams = []
            for parallel_sample in info_list:
                *_, library, sample = parallel_sample
                bams.append("{library}.{sample}.aln.bam".format(
                    library=library, sample=sample))
            MarkDuplicates = '{tool} MarkDuplicates -I {bams}  -O {sample}.dedup.bam -M {sample}.dedup.log -PG null --TMP_DIR ~/tmp/{sample} ;'.format(
                tool=self.gatk, bams=' -I '.join(bams), sample=bams[0].split('.')[1])
            part.append(MarkDuplicates)
            yield part, info_list

    def trim_bwa_dedup(self):
        for part, info_list in self.MarkDup():
            *_, sample = info_list[0]
            index = 'samtools index -@ 4 {sample}.dedup.bam ;'.format(
                sample=sample)
            CollectHsMetrics = '{tool} CollectHsMetrics -I {sample}.dedup.bam -O {sample}_hs_metrics.txt -BI {interval} -TI {interval} -R {reference} &'.format(
                tool=self.gatk, sample=sample, interval=self.interval, reference=self.reference)
            os.mkdir(os.path.join(self.working_space, sample))
            bamdst = '{tool} -p {bed} -o {sample} {sample}.dedup.bam &'.format(
                tool=self.bamdst, bed=self.bed, sample=sample)
            part.append(index)
            part.append(CollectHsMetrics)
            part.append(bamdst)
            sge = "#$ -N {sample}\n#$ -pe smp 16\n#$ -q all.q\n#$ -cwd\nset -e\ncd {working_space}\nsource ~/.bash_profile\n".format(
                sample=sample, working_space=self.working_space)
            with open(os.path.join(self.working_space, '{sample}.trim_bwa_dedup.bat'.format(sample=sample)), 'w') as f:
                f.write(sge)
                f.write('\n'.join(part)+'\n')
                f.write('wait ;')

    def bqsr(self):
        bams = ['{sample}.dedup.bam'.format(
            sample=sample) for sample in self.groups]
        BaseRecalibrator = '{tool} BaseRecalibrator -I {bams} -O recal.table --known-sites {snp} --known-sites {indel} -L {bed} -ip {ip} -R {reference} ;'.format(
            tool=self.gatk, bams=' -I '.join(bams), bed=self.bed, ip=self.ip, snp=self.snp, indel=self.indel, reference=self.reference)
        ApplyBQSR = '{tool} ApplyBQSR -I {bams} -O combined_bqsr.bam -bqsr recal.table -L {bed} -ip {ip} -R {reference} ;'.format(
            tool=self.gatk, bams=' -I '.join(bams), bed=self.bed, ip=self.ip, reference=self.reference)
        part = [BaseRecalibrator, ApplyBQSR]
        sge = "#$ -N {batch}\n#$ -pe smp 16\n#$ -q all.q\n#$ -cwd\nset -e\ncd {working_space}\nsource ~/.bash_profile\n".format(
            working_space=self.working_space, batch=os.path.basename(self.working_space))
        with open(os.path.join(self.working_space, 'bqsr.bat'), 'w') as f:
            f.write(sge)
            f.write('\n'.join(part)+'\n')
            f.write('wait ;')

    def gvcf(self):
        for sample in self.groups:
            HaplotypeCaller = '{tool} HaplotypeCaller -I combined_bqsr.bam --sample-name {sample} -O {sample}.HC.g.vcf.gz --emit-ref-confidence GVCF --dbsnp {dbsnp} -L {bed} -ip {ip} -R {reference} ;'.format(
                tool=self.gatk, sample=sample, bed=self.bed, ip=self.ip, dbsnp=self.dbsnp, reference=self.reference)
            sge = "#$ -N {batch}\n#$ -pe smp 8\n#$ -q all.q\n#$ -cwd\nset -e\ncd {working_space}\nsource ~/.bash_profile\n".format(
                working_space=self.working_space, batch=os.path.basename(self.working_space))
            with open(os.path.join(self.working_space, '{sample}.gvcf.bat'.format(sample=sample)), 'w') as f:
                f.write(sge)
                f.write(HaplotypeCaller+'\n')
                f.write('wait ;')

    def genotype(self):
        cram = "samtools view -C -T {reference} -@ 4 -o {batch}_combined_bqsr.cram combined_bqsr.bam &".format(
            reference=self.reference, batch=os.path.basename(self.working_space))
        gvcfs = [sample+'.HC.g.vcf.gz' for sample in self.groups]
        CombineGVCFs = '{tool} CombineGVCFs -V {gvcfs} -O cohort.g.vcf.gz -R {reference} ;'.format(
            tool=self.gatk, reference=self.reference, gvcfs=' -V '.join(gvcfs))
        GenotypeGVCFs = '{tool} GenotypeGVCFs -V cohort.g.vcf.gz -O han.vcf.gz -R {reference} --dbsnp {dbsnp} -L {bed} -ip {ip} ;'.format(
            tool=self.gatk, dbsnp=self.dbsnp, bed=self.bed, ip=self.ip, reference=self.reference)
        my_snp_Filter = '{tool} SelectVariants -select-type SNP -V han.vcf.gz -O han.snp.vcf.gz ;'.format(
            tool=self.gatk)
        my_snp_Filter2 = '{tool} VariantFiltration -V han.snp.vcf.gz --filter-expression "QD < 2.0 || MQ < 40.0 || FS > 60.0 || SOR > 3.0 || MQRankSum < -12.5 || ReadPosRankSum < -8.0" --filter-name "my_snp_Filter" -O han.snp.hardfilter.vcf.gz ;'.format(
            tool=self.gatk)
        my_indel_Filter = '{tool} SelectVariants -select-type INDEL -V han.vcf.gz -O han.indel.vcf.gz ;'.format(
            tool=self.gatk)
        my_indel_Filter2 = '{tool} VariantFiltration -V han.indel.vcf.gz --filter-expression "QD < 2.0 || FS > 200.0 || ReadPosRankSum < -20.0" --filter-name "my_indel_Filter" -O han.indel.hardfilter.vcf.gz ;'.format(
            tool=self.gatk)
        MergeVcfs = '{tool} MergeVcfs -R {reference} -I han.snp.hardfilter.vcf.gz -I han.indel.hardfilter.vcf.gz -O {batch}.snp.indel.hardfilter.vcf.gz ;'.format(
            tool=self.gatk, batch=os.path.basename(self.working_space), reference=self.reference)
        annotation = 'perl {tool}/table_annovar.pl {batch}.snp.indel.hardfilter.vcf.gz {tool}/humandb/ -buildver hg38 -out {batch} -otherinfo -remove -protocol refGene,cytoBand,exac03,gnomad_exome,clinvar_20170905,dbnsfp33a, -operation g,r,f,f,f,f --vcfinput -nastring . -polish -thread 30'.format(
            tool=self.annovar, batch=os.path.basename(self.working_space))
        self.InterVar_config()
        convert2avinput = 'perl {tool}/convert2annovar.pl -format vcf4old {batch}.snp.indel.hardfilter.vcf.gz >variant.avinput ;'.format(
            tool=self.annovar, batch=os.path.basename(self.working_space))
        ACMG_Intervar = 'python {tool} -c config.ini ;'.format(
            tool=self.Intervar)
        sge = "#$ -N annotation\n#$ -pe smp 16\n#$ -q all.q\n#$ -cwd\nset -e\ncd {working_space}\nsource ~/.bash_profile\n".format(
            working_space=self.working_space)
        part = [cram, CombineGVCFs, GenotypeGVCFs, my_indel_Filter,
                my_indel_Filter2, my_snp_Filter, my_snp_Filter2, MergeVcfs, annotation, convert2avinput, ACMG_Intervar]
        with open(os.path.join(self.working_space, 'genotype.bat'), 'w') as f:
            f.write(sge)
            f.write('\n'.join(part)+'\n')
            f.write('wait ;')

    def InterVar_config(self):
        config = []
        with open('{config}/config.ini'.format(config=os.path.dirname(self.Intervar)), 'r') as f:
            for i in f:
                config.append(i.strip())
        config[3] = 'inputfile=variant.avinput'
        config[6] = 'inputfile_type=avinput'
        config[8] = 'outfile=variant'
        with open('{working_space}/config.ini'.format(working_space=self.working_space), 'w') as f:
            f.write('\n'.join(config))

    def ssh_check(self):
        p = subprocess.Popen('hostname', shell=True, stdout=subprocess.PIPE)
        hostname = p.communicate()[0].strip().decode()
        return hostname

    def run_qsub_step1_step2(self):
        assert self.ssh_check() == 'guomai1', 'please login to guomai1 firstly'
        job_ID = []
        os.chdir(self.working_space)
        sys.stdout.write('changing working directory to your provide {}\n'.format(
            self.working_space))
        if os.path.exists('gm.log'):
            os.remove('gm.log')
        subprocess.call(
            'date +"%Y-%m-%d %H:%M:%S" >> gm.log', shell=True)
        subprocess.call(
            'echo begin all samples trim_bwa_dedup>> gm.log', shell=True)
        for sample in self.groups:
            cmd = 'qsub {sample}.trim_bwa_dedup.bat ;'.format(
                sample=sample)
            print(cmd)
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            step1_ID = p.communicate()[0].split()[2]
            job_ID.append(step1_ID)
        while 1:
            qstat_ID = self.run_check_by_time()
            _ = set(job_ID) & set(qstat_ID)
            if len(_) == 0:
                subprocess.call(
                    'date +"%Y-%m-%d %H:%M:%S" >> gm.log', shell=True)
                subprocess.call(
                    'echo end all samples trim_bwa_dedup>> gm.log', shell=True)
                cmd = 'qsub bqsr.bat ;'
                sys.stdout.write(cmd+'\n')
                p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
                step2_ID = p.communicate()[0].split()[2]
                subprocess.call(
                    'date +"%Y-%m-%d %H:%M:%S" >> gm.log', shell=True)
                subprocess.call('echo begin bqsr>> gm.log', shell=True)
                break
            else:
                time.sleep(60)
        return step2_ID

    def run_pbs_step3(self, step2_ID):
        while 1:
            qstat_ID = self.run_check_by_time()
            if step2_ID not in qstat_ID:
                subprocess.call(
                    'date +"%Y-%m-%d %H:%M:%S" >> gm.log', shell=True)
                subprocess.call('echo end bqsr>> gm.log', shell=True)
                files = os.listdir('./')
                pbs = [i for i in files if i.endswith('.gvcf.bat')]
                pbs_job_ID = []
                for sample in pbs:
                    cmd = 'qsub {sample} ;'.format(sample=sample)
                    p = subprocess.Popen(
                        cmd, shell=True, stdout=subprocess.PIPE)
                    ID = p.communicate()[0].split()[2]
                    pbs_job_ID.append(ID)
                    print(cmd)
                subprocess.call(
                    'date +"%Y-%m-%d %H:%M:%S" >> gm.log', shell=True)
                subprocess.call('echo begin gvcf>> gm.log', shell=True)
                break
            else:
                time.sleep(60)
        return pbs_job_ID

    def run_merge_step4(self, pbs_job_ID):
        while 1:
            qstat_ID = self.run_check_by_time()
            _ = set(pbs_job_ID) & set(qstat_ID)
            if len(_) == 0:
                subprocess.call(
                    'date +"%Y-%m-%d %H:%M:%S" >> gm.log', shell=True)
                subprocess.call(
                    'echo completed gvcf and merge vcf,genotyping now>> gm.log', shell=True)
                subprocess.call('qsub genotype.bat', shell=True)
                break
            else:
                time.sleep(60)

    def run_check_by_time(self):
        cmd = "qstat|sed -n '3,$p'|cut -d ' ' -f3"
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        qstat_ID = p.communicate()[0].split(b'\n')
        return qstat_ID


def main(p_dict):
    job = p_dict['input']
    result = Wes(job)
    result.trim_bwa_dedup()
    result.bqsr()
    result.gvcf()
    result.genotype()
    if p_dict['run'] == 'on':
        sys.stdout.write('auto qsub will be running in guomai1 right now.\n')
        step2_ID = result.run_qsub_step1_step2()
        pbs_job_ID = result.run_pbs_step3(step2_ID)
        result.run_merge_step4(pbs_job_ID)
    elif p_dict['run'] == 'off':
        sys.stdout.write('cause you choose run off,all job bat will be in {}.\n'.format(
            result.working_space))
    else:
        raise SystemError('only on or off\n')
