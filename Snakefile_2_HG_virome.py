from snakemake.utils import report
import glob, os, re

configfile : "config.yaml"

output_storage=config['pipeline_output']

##DIR
IN_DIR = output_storage + '03_trimmed/'
OUT_DIR = output_storage + '04_align_HG/'
REF_DIR = '/srv/nfs/ngs-stockage/NGS_Virologie/CCUB/GENOME/GRCh38/'
SCRIPT_DIR = '/srv/nfs/ngs-stockage/NGS_Virologie/CCUB/NGS_script'
BIN_DIR = '/srv/nfs/ngs-stockage/NGS_Virologie/BINARIES'

SAMPLES = [os.path.basename(f) for f in glob.glob(IN_DIR + '*_R1.fastq.gz')]
SAMPLES = [re.sub(r'_R1.fastq.gz', '',  i) for i in SAMPLES]

REFERENCES = ["GRCh38.p2_all"]

# Fichiers en sortie du pipeline 
rule all:
	input:
		expand(REF_DIR + '{genome}.fa.bwt', genome=REFERENCES),
		expand(OUT_DIR + '{genome}/unalign/{sample}_R1.fastq', sample=SAMPLES, genome=REFERENCES),
		expand(OUT_DIR + '{genome}/report_align_{genome}.html', genome=REFERENCES)
		
## Index 
rule bwa_index:
	input:
		db = REF_DIR + '{genome}.fa' #2) cherche {wildcards.genome}.fa"
	output:
		REF_DIR + '{genome}.fa.bwt' #1) cree la variable wildcards.genome.
	message:
		"Index du genome de reference :{wildcards.genome}"
	shell: #3) lance la commande
		"bwa index {input.db}" #"{input}"="{wildcards.genome}.fa"

# alignement PE
rule bwa_mem:
	input:
		bw = REF_DIR + '{genome}.fa.bwt',
		fasta = REF_DIR + '{genome}.fa',
		fq1 = IN_DIR + '{sample}_R1.fastq.gz', 
		fq2 = IN_DIR + '{sample}_R2.fastq.gz'
	output:
		temp(OUT_DIR + '{genome}/{sample}.bam')
	log:
		OUT_DIR+ '{genome}/{sample}_bwa.log'
	threads: 2
	message:
		"PE : sai --> bam ({wildcards.genome}/{wildcards.sample})"
	shell:
		"bwa mem  -k 45 -U 20 -L 20 "
		"-t {threads} "
		"{input.fasta} "
		"{input.fq1} {input.fq2} "
		"2>{log} | "
		"samtools view -bS - > {output}"

# stats alignment
rule flagstat:
	input:
		OUT_DIR + '{genome}/{sample}.bam'
	output:
		OUT_DIR + '{genome}/{sample}.flagstat'
	shell:
		"samtools flagstat {input} "
		">{output}"

## write unmapped PE reads BAM : attention ensuite seul les PE sont utilisee pour mapper...
rule unmappedBAM:
	input:
		OUT_DIR + '{genome}/{sample}.bam'
	output:
		temp(OUT_DIR + '{genome}/unalign/{sample}.bam')
	shell:
		"samtools view -f 4 -b {input} > {output}"
		
		
# > To extract unmapped reads whose mates are also unmapped:
# > samtools view -f 12 in.bam > uu.sam
# > To extract mapped reads whose mates are unmapped:
# > samtools view -F 4 -f 8 in.bam > mu.sam
# > To extract unmapped reads whose mates are mapped:
# > samtools view -f 4 -F 8 in.bam > um.sam

## write unmapped PE reads FASTQ
rule unmappedFASTQ:
	input:
		OUT_DIR + '{genome}/unalign/{sample}.bam'
	output:
		fq1 = OUT_DIR + '{genome}/unalign/{sample}_R1.fastq',
		fq2 = OUT_DIR + '{genome}/unalign/{sample}_R2.fastq'
	shell:
		"bamToFastq -i {input} "
		"-fq {output.fq1} "
		"-fq2 {output.fq2}"



## REPORT STAT ALIGNMENT	
rule mv_flagstat:
	input:
		expand(OUT_DIR + '{{genome}}/{sample}.flagstat', sample=SAMPLES)
	output:
		OUT_DIR + '{genome}/flagstat'
	shell:
		"if [ ! -d {output} ]; then mkdir {output}; fi; "
		"mv -t {output} {input}"

rule merge_flagstat:
	input:
		OUT_DIR + '{genome}/flagstat'
	output:
		OUT_DIR + '{genome}/summary_flagstat.txt'
	shell:
		"Rscript {SCRIPT_DIR}/merge_flagstats.R {input} {output}"
	
rule report:
	input:
		T1=OUT_DIR + '{genome}/summary_flagstat.txt'
	output:
		html=OUT_DIR + '{genome}/report_align_{genome}.html'
	run:
		report("""
		============================================
		RESUME DE L'ALIGNEMENT SUR {REFERENCES}
		============================================
		Voir le tableau T1_
		
		Total_Reads = Nombre de reads total apres alignement dans fichier bam
		
		Mapped = Nombre de reads qui s'alignent sur le genome de reference
		
		properly_paired = Nombre de reads qui s'alignent sur le genome de reference de maniere appariee (R1 et R2 alignees sur la meme ref)
		
		Attention pour avoir le nb de reads TOTALES passant QC  (nb de read en input) et le nb de reads qui s'alignent sur {REFERENCES} il faut soustraire les Supplementary et Secondary
		(reads qui s'alignent sur plusieurs refs et qui sont comptees plusieurs fois)
		
		""", output.html, metadata="Laurence Josset", **input)
	
