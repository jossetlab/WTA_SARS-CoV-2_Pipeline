### cov_ngs

## Quick informations

Pour lancer l'analyse editer le snakemake.sh dans la section CONFIG:
-output_dir : chemin ou créer les fichiers/dossiers du pipeline.
-path_to_fastq : lien disnap ou trouver les fastq pour l'analyse.

lancher une analyse complete:
k5start -U -f /home/chu-lyon.fr/regueex/login.kt -- nohup ./snakemake.sh > snakemake.out &

## Workflow

# Step 1

Removing adapters using cutadapt.
Version 1.12.
See more here : => https://cutadapt.readthedocs.io/en/stable/guide.html <=

# Step 2

Filtrate and remove human read using bwa.
Version 0.7.15-r1140.
See more here : => http://bio-bwa.sourceforge.net/ <=

# Step 3 (only for Amplicon/Sophia approach)

Remove Primers using fgbio.
Version 1.1.0.
Se more here : => https://github.com/fulcrumgenomics/fgbio <=

# Step 4 

Alignment on reference using bwa.
Processing BAM output using samtools and generating a preconcensus.
Version 1.3.1.
See more here: => http://www.htslib.org/ <=

# Step 5

Repeat step 4 using the previous preconsensus sequence.

# Step 6

Compute coverage using Bedtools.
Version v2.26.0.
See more here: => https://bedtools.readthedocs.io/en/latest/ <=


## Runs informations

capture: 
17/04 => /srv/nfs/ngs-stockage/NGS_Virologie/ncov_RUN_17042020
27/04 => /srv/nfs/ngs-stockage/NGS_Virologie/ncov_RUN_03052020

17:
/srv/nfs/ngs-stockage/NGS_Virologie/CGINEVRA/Capture_illumina/Covid_capture_illumina_fastq_run1/

27: 
/srv/nfs/ngs-stockage/NGS_commun/disnap/NgsWeb/FastQ/200430_NB501048_0720_AH2TY5AFX2_1588301402/ViroEst-Routine/VRES20-226-47_S22_R1.fastq.gz
cp /srv/nfs/ngs-stockage/NGS_commun/disnap/NgsWeb/FastQ/200430_NB501048_0720_AH2TY5AFX2_1588301402/ViroEst-Routine/VRES20-226-47_S22_R2.fastq.gz ./
cp /srv/nfs/ngs-stockage/NGS_commun/disnap/NgsWeb/FastQ/200430_NB501048_0720_AH2TY5AFX2_1588301402/ViroEst-Routine/VRES20-226-50_S23_R1.fastq.gz ./
cp /srv/nfs/ngs-stockage/NGS_commun/disnap/NgsWeb/FastQ/200430_NB501048_0720_AH2TY5AFX2_1588301402/ViroEst-Routine/VRES20-226-50_S23_R2.fastq.gz ./

WTA:
#### 200324_NB501048_0707_AH2K2CAFX2_1585161002 ####
#VRES20-95-88
ln -s /srv/nfs/ngs-stockage/NGS_commun/disnap/NgsWeb/FastQ/200324_NB501048_0707_AH2K2CAFX2_1585161002/ViroEst-Routine/VRES20-95-88_S6_R1.fastq.gz $output_dir/02_merged
ln -s /srv/nfs/ngs-stockage/NGS_commun/disnap/NgsWeb/FastQ/200324_NB501048_0707_AH2K2CAFX2_1585161002/ViroEst-Routine/VRES20-95-88_S6_R2.fastq.gz $output_dir/02_merged
#VRES20-101-70
ln -s /srv/nfs/ngs-stockage/NGS_commun/disnap/NgsWeb/FastQ/200324_NB501048_0707_AH2K2CAFX2_1585161002/ViroEst-Routine/VRES20-101-70_S8_R1.fastq.gz $output_dir/02_merged
ln -s /srv/nfs/ngs-stockage/NGS_commun/disnap/NgsWeb/FastQ/200324_NB501048_0707_AH2K2CAFX2_1585161002/ViroEst-Routine/VRES20-101-70_S8_R2.fastq.gz $output_dir/02_merged
#VRES20-109
ln -s /srv/nfs/ngs-stockage/NGS_commun/disnap/NgsWeb/FastQ/200324_NB501048_0707_AH2K2CAFX2_1585161002/ViroEst-Routine/VRES20-109-10_S21_R1.fastq.gz $output_dir/02_merged
ln -s /srv/nfs/ngs-stockage/NGS_commun/disnap/NgsWeb/FastQ/200324_NB501048_0707_AH2K2CAFX2_1585161002/ViroEst-Routine/VRES20-109-10_S21_R2.fastq.gz $output_dir/02_merged
#### 200417_NB501048_0716_AH2JLNAFX2_1587221401 ####
#VRES20-226-47
ln -s /srv/nfs/disnap/NGS/NgsWeb/FastQ/200417_NB501048_0716_AH2JLNAFX2_1587221401/ViroEst-Routine/VRES20-226-47_S5_R1.fastq.gz $output_dir/02_merged
ln -s /srv/nfs/disnap/NGS/NgsWeb/FastQ/200417_NB501048_0716_AH2JLNAFX2_1587221401/ViroEst-Routine/VRES20-226-47_S5_R2.fastq.gz $output_dir/02_merged
#VRES20-226-50
ln -s /srv/nfs/disnap/NGS/NgsWeb/FastQ/200417_NB501048_0716_AH2JLNAFX2_1587221401/ViroEst-Routine/VRES20-226-50_S8_R1.fastq.gz $output_dir/02_merged
ln -s /srv/nfs/disnap/NGS/NgsWeb/FastQ/200417_NB501048_0716_AH2JLNAFX2_1587221401/ViroEst-Routine/VRES20-226-50_S8_R2.fastq.gz $output_dir/02_merged
#### 200424_NB501048_0718_AH2VVTAFX2_1587828601 ####
#VRES20-101-94
ln -s /srv/nfs/disnap/NGS/NgsWeb/FastQ/200424_NB501048_0718_AH2VVTAFX2_1587828601/ViroEst-Routine/VRES20-101-94_S1_R1.fastq.gz $output_dir/02_merged
ln -s /srv/nfs/disnap/NGS/NgsWeb/FastQ/200424_NB501048_0718_AH2VVTAFX2_1587828601/ViroEst-Routine/VRES20-101-94_S1_R2.fastq.gz $output_dir/02_merged
#VRES20-102-18
ln -s /srv/nfs/disnap/NGS/NgsWeb/FastQ/200424_NB501048_0718_AH2VVTAFX2_1587828601/ViroEst-Routine/VRES20-102-18_S4_R1.fastq.gz $output_dir/02_merged
ln -s /srv/nfs/disnap/NGS/NgsWeb/FastQ/200424_NB501048_0718_AH2VVTAFX2_1587828601/ViroEst-Routine/VRES20-102-18_S4_R2.fastq.gz $output_dir/02_merged
#VRES20-102-59
ln -s /srv/nfs/disnap/NGS/NgsWeb/FastQ/200424_NB501048_0718_AH2VVTAFX2_1587828601/ViroEst-Routine/VRES20-102-59_S7_R1.fastq.gz $output_dir/02_merged
ln -s /srv/nfs/disnap/NGS/NgsWeb/FastQ/200424_NB501048_0718_AH2VVTAFX2_1587828601/ViroEst-Routine/VRES20-102-59_S7_R2.fastq.gz $output_dir/02_merged
#VRES20-104-41
ln -s /srv/nfs/disnap/NGS/NgsWeb/FastQ/200424_NB501048_0718_AH2VVTAFX2_1587828601/ViroEst-Routine/VRES20-104-41_S10_R1.fastq.gz $output_dir/02_merged
ln -s /srv/nfs/disnap/NGS/NgsWeb/FastQ/200424_NB501048_0718_AH2VVTAFX2_1587828601/ViroEst-Routine/VRES20-104-41_S10_R2.fastq.gz $output_dir/02_merged
#VRES20-104-44
ln -s /srv/nfs/disnap/NGS/NgsWeb/FastQ/200424_NB501048_0718_AH2VVTAFX2_1587828601/ViroEst-Routine/VRES20-104-44_S13_R1.fastq.gz $output_dir/02_merged
ln -s /srv/nfs/disnap/NGS/NgsWeb/FastQ/200424_NB501048_0718_AH2VVTAFX2_1587828601/ViroEst-Routine/VRES20-104-44_S13_R2.fastq.gz $output_dir/02_merged
#VRES20-105-80
ln -s /srv/nfs/disnap/NGS/NgsWeb/FastQ/200424_NB501048_0718_AH2VVTAFX2_1587828601/ViroEst-Routine/VRES20-105-80_S16_R1.fastq.gz $output_dir/02_merged
ln -s /srv/nfs/disnap/NGS/NgsWeb/FastQ/200424_NB501048_0718_AH2VVTAFX2_1587828601/ViroEst-Routine/VRES20-105-80_S16_R2.fastq.gz $output_dir/02_merged
#VRES20-108-5
ln -s /srv/nfs/disnap/NGS/NgsWeb/FastQ/200424_NB501048_0718_AH2VVTAFX2_1587828601/ViroEst-Routine/VRES20-108-5_S19_R1.fastq.gz $output_dir/02_merged
ln -s /srv/nfs/disnap/NGS/NgsWeb/FastQ/200424_NB501048_0718_AH2VVTAFX2_1587828601/ViroEst-Routine/VRES20-108-5_S19_R2.fastq.gz $output_dir/02_merged
#VRES20-108-21
ln -s /srv/nfs/disnap/NGS/NgsWeb/FastQ/200424_NB501048_0718_AH2VVTAFX2_1587828601/ViroEst-Routine/VRES20-108-21_S22_R1.fastq.gz $output_dir/02_merged
ln -s /srv/nfs/disnap/NGS/NgsWeb/FastQ/200424_NB501048_0718_AH2VVTAFX2_1587828601/ViroEst-Routine/VRES20-108-21_S22_R2.fastq.gz $output_dir/02_merged
#VRES20-108-36
ln -s /srv/nfs/disnap/NGS/NgsWeb/FastQ/200424_NB501048_0718_AH2VVTAFX2_1587828601/ViroEst-Routine/VRES20-108-36_S2_R1.fastq.gz $output_dir/02_merged
ln -s /srv/nfs/disnap/NGS/NgsWeb/FastQ/200424_NB501048_0718_AH2VVTAFX2_1587828601/ViroEst-Routine/VRES20-108-36_S2_R2.fastq.gz $output_dir/02_merged
#VRES20-108-63
ln -s /srv/nfs/disnap/NGS/NgsWeb/FastQ/200424_NB501048_0718_AH2VVTAFX2_1587828601/ViroEst-Routine/VRES20-108-63_S5_R1.fastq.gz $output_dir/02_merged
ln -s /srv/nfs/disnap/NGS/NgsWeb/FastQ/200424_NB501048_0718_AH2VVTAFX2_1587828601/ViroEst-Routine/VRES20-108-63_S5_R2.fastq.gz $output_dir/02_merged
#VRES20-111-67
ln -s /srv/nfs/disnap/NGS/NgsWeb/FastQ/200424_NB501048_0718_AH2VVTAFX2_1587828601/ViroEst-Routine/VRES20-111-67_S8_R1.fastq.gz $output_dir/02_merged
ln -s /srv/nfs/disnap/NGS/NgsWeb/FastQ/200424_NB501048_0718_AH2VVTAFX2_1587828601/ViroEst-Routine/VRES20-111-67_S8_R2.fastq.gz $output_dir/02_merged
#VRES20-112-5
ln -s /srv/nfs/disnap/NGS/NgsWeb/FastQ/200424_NB501048_0718_AH2VVTAFX2_1587828601/ViroEst-Routine/VRES20-112-5_S11_R1.fastq.gz $output_dir/02_merged
ln -s /srv/nfs/disnap/NGS/NgsWeb/FastQ/200424_NB501048_0718_AH2VVTAFX2_1587828601/ViroEst-Routine/VRES20-112-5_S11_R2.fastq.gz $output_dir/02_merged
#VRES20-112-28
ln -s /srv/nfs/disnap/NGS/NgsWeb/FastQ/200424_NB501048_0718_AH2VVTAFX2_1587828601/ViroEst-Routine/VRES20-112-28_S14_R1.fastq.gz $output_dir/02_merged
ln -s /srv/nfs/disnap/NGS/NgsWeb/FastQ/200424_NB501048_0718_AH2VVTAFX2_1587828601/ViroEst-Routine/VRES20-112-28_S14_R2.fastq.gz $output_dir/02_merged
#VRES20-112-31
ln -s /srv/nfs/disnap/NGS/NgsWeb/FastQ/200424_NB501048_0718_AH2VVTAFX2_1587828601/ViroEst-Routine/VRES20-112-31_S17_R1.fastq.gz $output_dir/02_merged
ln -s /srv/nfs/disnap/NGS/NgsWeb/FastQ/200424_NB501048_0718_AH2VVTAFX2_1587828601/ViroEst-Routine/VRES20-112-31_S17_R2.fastq.gz $output_dir/02_merged
#### 200319_NB501048_0706_AH22T7AFX2_1584724802 ####
#VRES20-60-42
ln -s /srv/nfs/disnap/NGS/NgsWeb/FastQ/200319_NB501048_0706_AH22T7AFX2_1584724802/ViroEst-Routine/VRES20-060-42_S1_R1.fastq.gz $output_dir/02_merged
ln -s /srv/nfs/disnap/NGS/NgsWeb/FastQ/200319_NB501048_0706_AH22T7AFX2_1584724802/ViroEst-Routine/VRES20-060-42_S1_R2.fastq.gz $output_dir/02_merged
#VRES20-60-56
ln -s /srv/nfs/disnap/NGS/NgsWeb/FastQ/200319_NB501048_0706_AH22T7AFX2_1584724802/ViroEst-Routine/VRES20-060-56_S5_R1.fastq.gz $output_dir/02_merged
ln -s /srv/nfs/disnap/NGS/NgsWeb/FastQ/200319_NB501048_0706_AH22T7AFX2_1584724802/ViroEst-Routine/VRES20-060-56_S5_R2.fastq.gz $output_dir/02_merged
#VRES20-63-91
ln -s /srv/nfs/disnap/NGS/NgsWeb/FastQ/200319_NB501048_0706_AH22T7AFX2_1584724802/ViroEst-Routine/VRES20-063-91_S9_R1.fastq.gz $output_dir/02_merged
ln -s /srv/nfs/disnap/NGS/NgsWeb/FastQ/200319_NB501048_0706_AH22T7AFX2_1584724802/ViroEst-Routine/VRES20-063-91_S9_R2.fastq.gz $output_dir/02_merged
#VRES20-66-25
ln -s /srv/nfs/disnap/NGS/NgsWeb/FastQ/200319_NB501048_0706_AH22T7AFX2_1584724802/ViroEst-Routine/VRES20-066-25_S13_R1.fastq.gz $output_dir/02_merged
ln -s /srv/nfs/disnap/NGS/NgsWeb/FastQ/200319_NB501048_0706_AH22T7AFX2_1584724802/ViroEst-Routine/VRES20-066-25_S13_R2.fastq.gz $output_dir/02_merged
#VRES20-68-20
ln -s /srv/nfs/disnap/NGS/NgsWeb/FastQ/200319_NB501048_0706_AH22T7AFX2_1584724802/ViroEst-Routine/VRES20-068-20_S8_R1.fastq.gz $output_dir/02_merged
ln -s /srv/nfs/disnap/NGS/NgsWeb/FastQ/200319_NB501048_0706_AH22T7AFX2_1584724802/ViroEst-Routine/VRES20-068-20_S8_R2.fastq.gz $output_dir/02_merged


sophia:
/srv/nfs/ngs-stockage/NGS_commun/disnap/NgsWeb/FastQ/200430_NB552333_0001_AH2GHHAFX2_1588625404/ViroEst-Routine/*
27/04 => /srv/nfs/ngs-stockage/NGS_Virologie/CoV_TESTV2_Sophia_200430

annecy:
path_to_fastq="/srv/nfs/ngs-stockage/NGS_Virologie/HadrienR/sophia-annecy-20052020/FASTQ/fastq_merged/"

