from snakemake.utils import report
import glob, os, re

configfile : "config.yaml"

output_storage=config['pipeline_output']

## BWA database
REF_DIR = '/srv/nfs/ngs-stockage/NGS_Virologie/CCUB/GENOME/virus/'
REFERENCES = ['nCoV_noA']

##DIR
IN_DIR = output_storage + '04_align_HG/GRCh38.p2_all/unalign/'
ALN_DIR = output_storage + '05_align_Virus_min3X/'
SCRIPT_DIR = '/srv/nfs/ngs-stockage/NGS_Virologie/CCUB/NGS_script'
BIN_DIR = '/srv/nfs/ngs-stockage/NGS_Virologie/BINARIES'


SAMPLES = [os.path.basename(f) for f in glob.glob(IN_DIR + '*_R1.fastq')]
SAMPLES = [re.sub(r'_R1.fastq', '',  i) for i in SAMPLES]

# Fichiers en sortie du pipeline
rule all:
	input:
		expand(REF_DIR + '{genome}.fasta.bwt', genome=REFERENCES),
		# expand(ALN_DIR + '{genome}/align/{sample}_R1.fastq', sample=SAMPLES, genome=REFERENCES),
		expand(ALN_DIR + '{genome}/{sample}_ref.fasta', genome=REFERENCES, sample=SAMPLES),
		expand(ALN_DIR+ '{genome}/report_align_{genome}.html', genome=REFERENCES)

## Index du genome de reference avant l'alignement des reads
rule bwa_index:
	input:
		db = REF_DIR + '{genome}.fasta' #2) cherche {wildcards.genome}.fa"
	output:
		REF_DIR + '{genome}.fasta.bwt'
	shell: #3) lance la commande
		"bwa index {input.db}"

## alignement PE
rule bwa_mem:
	input:
		REF_DIR + '{genome}.fasta.bwt' ,
		fasta = REF_DIR + '{genome}.fasta',
		fq1 = IN_DIR+ '{sample}_R1.fastq',
		fq2 = IN_DIR+ '{sample}_R2.fastq'
	output:
		temp(ALN_DIR+ '{genome}/{sample}.bam')
	log:
		ALN_DIR+ '{genome}/{sample}_bwa.log'
	threads: 2
	message:
		"PE : sai --> bam ({wildcards.genome}/{wildcards.sample})"
	shell:
		"bwa mem -M "
		#"bwa mem -O 10 -E 2 "
		"-t {threads} "
		"{input.fasta} "
		"{input.fq1} {input.fq2} "
		"2>{log} | "
		"samtools view -bS - > {output}"

## idxstat and consensus
rule sort:
	input:
		ALN_DIR+ '{genome}/{sample}.bam'
	output:
		ALN_DIR+ '{genome}/{sample}_sorted.bam'
	shell:
		"samtools sort -o {output} {input} "

rule mpileup:
	input:
		bam = ALN_DIR+ '{genome}/{sample}_sorted.bam',
		ref_fasta = REF_DIR + '{genome}.fasta'
	output:
		ALN_DIR+ '{genome}/{sample}_pileup.txt'
	shell:
		"samtools mpileup -q 10 -d 100000 -f {input.ref_fasta} {input.bam} > {output}"

rule consensus:
	input:
		ALN_DIR+ '{genome}/{sample}_pileup.txt'
	output:
		ALN_DIR+ '{genome}/{sample}_ref.fasta'
	shell:
		"perl {SCRIPT_DIR}/pathogen_varcaller_lowtreshold.pl {input} 0.5 {output}"

# stats alignment
rule flagstat:
	input:
		ALN_DIR + '{genome}/{sample}_sorted.bam'
	output:
		ALN_DIR+ '{genome}/{sample}.flagstat'
	shell:
		"samtools flagstat {input} "
		">{output}"

## DEPTH
rule depth:
	input:
		ALN_DIR+ '{genome}/{sample}_sorted.bam'
	output:
		ALN_DIR+ '{genome}/{sample}.depth'
	shell:
		"bedtools genomecov -ibam {input} -d > {output} "

## merge files
rule mv_flagstat:
	input:
		expand(ALN_DIR + '{{genome}}/{sample}.flagstat', sample=SAMPLES)
	output:
		touch(ALN_DIR + '{genome}/flagstat')
	shell:
		"if [ ! -d {output} ]; then mkdir {output}; fi; "
		"mv -t {output} {input}"

rule merge_flagstat:
	input:
		ALN_DIR + '{genome}/flagstat'
	output:
		ALN_DIR + '{genome}/summary_flagstat.txt'
	shell:
		"Rscript {SCRIPT_DIR}/merge_flagstats.R {input} {output}"

rule mv_depth:
	input:
		expand(ALN_DIR + '{{genome}}/{sample}.depth', sample=SAMPLES)
	output:
		touch(ALN_DIR + '{genome}/depth')
	shell:
		"if [ ! -d {output} ]; then mkdir {output}; fi; "
		"mv -t {output} {input}"

rule merge_depth:
	input:
		ALN_DIR + '{genome}/depth'
	output:
		f=ALN_DIR + '{genome}/summary_depth.txt',
		g=ALN_DIR + '{genome}/cov.pdf',
	shell:
		"Rscript {SCRIPT_DIR}/merge_depth_target.R {input} {output.f} {output.g}"

## write mapped PE reads BAM 
rule unmappedBAM:
	input:
		ALN_DIR + '{genome}/{sample}_trimm.bam'
	output:
		temp(ALN_DIR + '{genome}/align/{sample}.bam')
	shell:
		"samtools view -F 4 -b {input} > {output}"

rule unmappedFASTQ:
	input:
		ALN_DIR + '{genome}/align/{sample}.bam'
	output:
		fq1 = ALN_DIR + '{genome}/align/{sample}_R1.fastq',
		fq2 = ALN_DIR + '{genome}/align/{sample}_R2.fastq'
	shell:
		"bamToFastq -i {input} "
		"-fq {output.fq1} "
		"-fq2 {output.fq2}"

## REPORT STAT ALIGNMENT
rule report:
	input:
		T1=ALN_DIR+ '{genome}/summary_flagstat.txt',
		F1=ALN_DIR + '{genome}/cov.pdf',
		T2=ALN_DIR+ '{genome}/summary_depth.txt'
	output:
		html=ALN_DIR+ '{genome}/report_align_{genome}.html'
	run:
		report("""
		============================================
		RESUME DE L'ALIGNEMENT SUR {REFERENCES}
		============================================
		Analyse des reads NE S'ALIGNANT PAS SUR lE GENOME HUMAIN

		Voir le tableau T1_

		Nombre de reads total passant QC

		Mapped = Nombre de reads qui s'alignent sur le genome de reference

		properly_paired = Nombre de reads qui s'alignent sur le genome de reference de maniere appariee (R1 et R2 alignees sur le genome)

		Attention pour avoir le nb de reads TOTALES et le nb de reads qui s'alignent sur {REFERENCES} il faut soustraire les Supplementary et Secondary
		(reads qui s'alignent sur plusieurs refs et qui sont comptees plusieurs fois)

		Tableau T2_ : depth of coverage at each position

		Figure F1_ : coverage. A VERIFIER POUR VALIDATION DES ECHANTILLONS

		""", output.html, metadata="Laurence Josset", **input)