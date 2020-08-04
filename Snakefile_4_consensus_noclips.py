from snakemake.utils import report
import glob, os, re
from pathlib import Path

configfile : "config.yaml"

output_storage=config['pipeline_output']

## BWA database
REF_DIR = output_storage + '05_align_Virus_min3X/nCoV_noA/'

##DIR
IN_DIR = output_storage + '04_align_HG/GRCh38.p2_all/unalign/'
ALN_DIR = output_storage + '06_align_Ref_noclips/'
SCRIPT_DIR = '/srv/nfs/ngs-stockage/NGS_Virologie/CCUB/NGS_script'

SAMPLES = [os.path.basename(f) for f in glob.glob(IN_DIR + '*_R1.fastq')]
SAMPLES = [re.sub(r'_R1.fastq', '',  i) for i in SAMPLES]

#Filtrate bad ref.fasta
SAMPLES_FILTER=[]
for sample in SAMPLES:
    test_sample=sample
    size_file=Path(output_storage + '05_align_Virus_min3X/nCoV_noA/'+test_sample+'_ref.fasta').stat().st_size
    if (size_file>0):
        SAMPLES_FILTER.append(test_sample)

SAMPLES=SAMPLES_FILTER		

# Fichiers en sortie du pipeline
rule all:
	input:
		#expand(REF_DIR + '{sample}_ref.fasta.bwt', sample=SAMPLES),
		expand(ALN_DIR + 'align/{sample}_R1.fastq', sample=SAMPLES),
		expand(ALN_DIR + '{sample}_consensus_min10x_noclips.fasta', sample=SAMPLES),
		expand(ALN_DIR + '{sample}_consensus_min50x_noclips.fasta', sample=SAMPLES),
		expand(ALN_DIR + '{sample}_consensus_min100x_noclips.fasta', sample=SAMPLES),
		expand(ALN_DIR + '{sample}_consensus_min200x_noclips.fasta', sample=SAMPLES),
		expand(ALN_DIR+ 'report_align_ref.html'),
		expand(ALN_DIR+ 'mean_coverage.txt'),
		ALN_DIR + 'fasta',
		expand(ALN_DIR+ '{sample}.bam', sample=SAMPLES),
		#expand(ALN_DIR+ 'coverage/{sample}.depth',sample=SAMPLES)

## alignement PE
rule bwa_mem:
	input:
		#REF_DIR + '{sample}_ref.fasta.bwt' ,
		fasta = REF_DIR + '{sample}_ref.fasta',
		fq1 = IN_DIR+ '{sample}_R1.fastq',
		fq2 = IN_DIR+ '{sample}_R2.fastq'
	output:
		ALN_DIR+ '{sample}.bam'
	log:
		ALN_DIR+ '{sample}_bwa.log'
	threads: 2
	message:
		"PE : sai --> bam ({wildcards.sample}/{wildcards.sample})"
	shell:
		"""
		bwa index {input.fasta}
		bwa mem -M -t {threads} {input.fasta} {input.fq1} {input.fq2} 2>{log} | samtools view -bS - > {output}
		"""

## remove hard and soft clipped?!! and sort
rule remove_clipped:
	input:
		ALN_DIR+ '{sample}.bam'
	output:
		ALN_DIR+ '{sample}_sorted_noclips.bam'
	shell:
		"samtools view -h {input} | awk '$6 !~ /H|S/{{print}}' | samtools view -bS - | samtools sort -o {output} - "

## consensus
rule mpileup:
	input:
		bam = ALN_DIR+ '{sample}_sorted_noclips.bam',
		ref_fasta = REF_DIR + '{sample}_ref.fasta'
	output:
		ALN_DIR+ '{sample}_pileup_noclips.txt'
	shell:
		"samtools mpileup -q 10 -d 200000 -f {input.ref_fasta} {input.bam} > {output}"

rule consensus_10x:
	input:
		ALN_DIR+ '{sample}_pileup_noclips.txt'
	output:
		ALN_DIR+ '{sample}_consensus_min10x_noclips.fasta'
	shell:
		"perl {SCRIPT_DIR}/pathogen_varcaller_10x.pl {input} 0.5 {output}"

rule consensus_50x:
	input:
		ALN_DIR+ '{sample}_pileup_noclips.txt'
	output:
		ALN_DIR+ '{sample}_consensus_min50x_noclips.fasta'
	shell:
		"perl {SCRIPT_DIR}/pathogen_varcaller_50x.pl {input} 0.5 {output}"
		
rule consensus_100x:
	input:
		ALN_DIR+ '{sample}_pileup_noclips.txt'
	output:
		ALN_DIR+ '{sample}_consensus_min100x_noclips.fasta'
	shell:
		"perl {SCRIPT_DIR}/pathogen_varcaller_100x.pl {input} 0.5 {output}"

rule consensus_200x:
	input:
		ALN_DIR+ '{sample}_pileup_noclips.txt'
	output:
		ALN_DIR+ '{sample}_consensus_min200x_noclips.fasta'
	shell:
		"perl {SCRIPT_DIR}/pathogen_varcaller_200x.pl {input} 0.5 {output}"
		
# stats alignment
rule flagstat:
	input:
		ALN_DIR+ '{sample}_sorted_noclips.bam'
	output:
		ALN_DIR+ '{sample}.flagstat'
	shell:
		"samtools flagstat {input} "
		">{output}"

## DEPTH_BEDTOOLS
rule get_coverage:
	input:
		ALN_DIR+ '{sample}_sorted_noclips.bam'
	output:
		ALN_DIR+ '{sample}.depth'
	shell:
		"bedtools genomecov -ibam {input} -d > {output} "


## merge files
rule mv_flagstat:
	input:
		expand(ALN_DIR + '{sample}.flagstat', sample=SAMPLES)
	output:
		touch(ALN_DIR + 'flagstat')
	shell:
		"if [ ! -d {output} ]; then mkdir {output}; fi; "
		"mv -t {output} {input}"

rule merge_flagstat:
	input:
		ALN_DIR + 'flagstat'
	output:
		ALN_DIR + 'summary_flagstat.txt'
	shell:
		"Rscript {SCRIPT_DIR}/merge_flagstats.R {input} {output}"

rule mv_depth:
	input:
		expand(ALN_DIR + '{sample}.depth', sample=SAMPLES)
	output:
		touch(ALN_DIR + 'coverage')
	shell:
		"if [ ! -d {output} ]; then mkdir {output}; fi; "
		"mv -t {output} {input}"

rule merge_depth:
	input:
		ALN_DIR + 'coverage'
	output:
		f=ALN_DIR + 'summary_depth.txt',
		g=ALN_DIR + 'cov.pdf',
	shell:
		"Rscript {SCRIPT_DIR}/merge_depth_target.R {input} {output.f} {output.g}"

## write mapped PE reads BAM 
rule unmappedBAM:
	input:
		ALN_DIR + '{sample}.bam'
	output:
		temp(ALN_DIR + 'align/{sample}.bam')
	shell:
		"samtools view -F 4 -b {input} > {output}"

rule unmappedFASTQ:
	input:
		ALN_DIR + 'align/{sample}.bam'
	output:
		fq1 = ALN_DIR + 'align/{sample}_R1.fastq',
		fq2 = ALN_DIR + 'align/{sample}_R2.fastq'
	shell:
		"bamToFastq -i {input} "
		"-fq {output.fq1} "
		"-fq2 {output.fq2}"

rule depth_mean:
	input:
		T2=ALN_DIR+ 'summary_depth.txt'
	output:
		depth = ALN_DIR+ 'mean_coverage.txt'
	shell:
		"Rscript scripts/mean_depth.R {input} {output} "

rule regroup_fasta:
	input:
		expand(ALN_DIR+ '{sample}_consensus_min10x_noclips.fasta',sample=SAMPLES),
	output:		
		ALN_DIR + 'fasta'
	params:
		path=ALN_DIR		
	shell:
		"if [ ! -d {output} ]; then mkdir {output}; fi; "
		"scripts/concatenate_fasta.py {params.path} "

## REPORT STAT ALIGNMENT
rule report:
	input:
		T1=ALN_DIR+ 'summary_flagstat.txt',
		F1=ALN_DIR + 'cov.pdf',
		T2=ALN_DIR+ 'mean_coverage.txt'
	output:
		html=ALN_DIR+ 'report_align_ref.html'
	run:
		REFERENCES = ['nCoV_noA']
		report("""
		============================================
		RESUME DE L'ALIGNEMENT SUR {REFERENCES}
		============================================
		Analyse des reads NE S'ALIGNANT PAS SUR lE GENOME HUMAIN

		Voir le tableau T1_

		Nombre de reads total passant QC

		Mapped = Nombre de reads qui s'alignent sur le sample de reference

		properly_paired = Nombre de reads qui s'alignent sur le sample de reference de maniere appariee (R1 et R2 alignees sur le sample)

		Attention pour avoir le nb de reads TOTALES et le nb de reads qui s'alignent sur {REFERENCES} il faut soustraire les Supplementary et Secondary
		(reads qui s'alignent sur plusieurs refs et qui sont comptees plusieurs fois)

		Tableau T2_ : depth of coverage at each position

		Figure F1_ : coverage. A VERIFIER POUR VALIDATION DES ECHANTILLONS

		""", output.html, metadata="Laurence Josset", **input)        