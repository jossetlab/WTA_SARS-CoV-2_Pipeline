import glob, os, re

configfile : "config.yaml"

output_storage=config['pipeline_output']
cut1=config['adapter1']
cut2=config['adapter2']

##DIR
IN_DIR = output_storage + '02_merged/'
OUT_DIR = output_storage + '03_trimmed/'

SAMPLES = [os.path.basename(f) for f in glob.glob(IN_DIR + '*_R1.fastq.gz')]
SAMPLES = [re.sub(r'_R1.fastq.gz', '',  i) for i in SAMPLES]

# Fichiers en sortie du pipeline
rule all:
    input: expand(OUT_DIR+ '{sample}_R1.fastq.gz', sample=SAMPLES)

rule cutadapt:
	input:
		r1= IN_DIR + '{sample}_R1.fastq.gz',
		r2= IN_DIR + '{sample}_R2.fastq.gz'
	output:
		r1= OUT_DIR + '{sample}_R1.fastq.gz',
		r2= OUT_DIR + '{sample}_R2.fastq.gz'		
	shell:
		"""
		cutadapt -a CTGTCTCTTATACACATCTCCGAGCCCACGAGAC \
				 -A CTGTCTCTTATACACATCTGACGCTGCCGACGA \
				 -q 30 -m 50 -o {output.r1} -p {output.r2} {input.r1} {input.r2}
		"""
