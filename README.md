### cov_ngs

## Quick informations
-output_dir : analysis output folder.
-path_to_fastq : path to paired fastq.

Launch the pipeline:
./snakemake.sh > snakemake.out &

## Workflow

# Step 1

Removing adapters using cutadapt.
Version 1.12.
See more here : => https://cutadapt.readthedocs.io/en/stable/guide.html <=

# Step 2

Filtrate and remove human read using bwa.
Version 0.7.15-r1140.
See more here : => http://bio-bwa.sourceforge.net/ <=

# Step 3

Alignment on reference using bwa.
Processing BAM output using samtools and generating a preconcensus.
Version 1.3.1.
See more here: => http://www.htslib.org/ <=

# Step 4

Repeat step 4 using the previous preconsensus sequence.

# Step 5

Compute coverage using Bedtools.
Version v2.26.0.
See more here: => https://bedtools.readthedocs.io/en/latest/ <=


