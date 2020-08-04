#!/bin/bash 
set -e

## require python 3 
export PATH=$PATH:/usr/bin/python3
export PATH=$PATH:/usr/bin/samtools
export PATH=$PATH:/usr/bin/bwa
export PATH=$PATH:/usr/bin/cutadapt
export PATH=$PATH:/usr/bin/bedtools

################# CONFIG ########################
output_dir="/srv/nfs/ngs-stockage/NGS_Virologie/PROTO_sars-cov2/WTA/coro20200724/"
path_to_fastq="/srv/nfs/ngs-stockage/NGS_commun/disnap/NgsWeb/FastQ/200724_NB552333_0011_AHHWK2BGXF_1595695201/ViroEst-Routine/*"
#################################################
################ PRE-PROCESS ####################

################ PIPELINE #######################
mkdir -p ${output_dir}02_merged
ln -s $path_to_fastq $output_dir/02_merged

snakemake -s Snakefile_1_cutadapt2.py \
            --cores 10 \
            --config pipeline_output=$output_dir
snakemake s Snakefile_1_cutadapt2.py \
            --cores 10 \
            --config pipeline_output=$output_dir

snakemake -s Snakefile_2_HG_virome.py \
            --cores 10 \
            --config pipeline_output=$output_dir

snakemake -s Snakefile_3_nCoV_min3X.py \
            --cores 10 \
            --config pipeline_output=$output_dir

snakemake -s Snakefile_4_consensus_noclips.py \
            --cores 10 \
            --config pipeline_output=$output_dir

chmod -R 777 $output_dir

rm -r ${output_dir}/02_merged
