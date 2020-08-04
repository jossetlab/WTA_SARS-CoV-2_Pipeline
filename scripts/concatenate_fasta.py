#!/usr/bin/env python3
import glob
import os
import sys

#path = "/srv/nfs/ngs-stockage/NGS_Virologie/HadrienR/nCOV_RUN_TEST/06_align_Ref_noclips/"
path=sys.argv[1]

list_x10=glob.glob(path + '*_consensus_min10x_noclips.fasta')
list_x50=glob.glob(path + '*_consensus_min50x_noclips.fasta')
list_x100=glob.glob(path + '*_consensus_min100x_noclips.fasta')
list_x200=glob.glob(path + '*_consensus_min200x_noclips.fasta')

#function for store fasta in a dictionary
def read_fasta_x10(mylist):   
    fastas={}
    for path in mylist:
        fasta_file=open(path,"r")
        for line in fasta_file:
            if (line[0]=='>'):
                header=os.path.basename(path)
                header=header[:-len("_consensus_min10x_noclips.fasta")]
                fastas[header]=''
            else:
                fastas[header]+=line
        fasta_file.close()
    return fastas

def read_fasta_x50(mylist):   
    fastas={}
    for path in mylist:
        fasta_file=open(path,"r")
        for line in fasta_file:
            if (line[0]=='>'):
                header=os.path.basename(path)
                header=header[:-len("_consensus_min50x_noclips.fasta")]
                fastas[header]=''
            else:
                fastas[header]+=line
        fasta_file.close()
    return fastas

def read_fasta_x100(mylist):   
    fastas={}
    for path in mylist:
        fasta_file=open(path,"r")
        for line in fasta_file:
            if (line[0]=='>'):
                header=os.path.basename(path)
                header=header[:-len("_consensus_min100x_noclips.fasta")]
                fastas[header]=''
            else:
                fastas[header]+=line
        fasta_file.close()
    return fastas

def read_fasta_x200(mylist):   
    fastas={}
    for path in mylist:
        fasta_file=open(path,"r")
        for line in fasta_file:
            if (line[0]=='>'):
                header=os.path.basename(path)
                header=header[:-len("_consensus_min200x_noclips.fasta")]
                fastas[header]=''
            else:
                fastas[header]+=line
        fasta_file.close()
    return fastas        


fasta_x10=read_fasta_x10(list_x10) 
fasta_x50=read_fasta_x50(list_x50) 
fasta_x100=read_fasta_x100(list_x100) 
fasta_x200=read_fasta_x200(list_x200) 


def write_fastas_x10(fastas_dic):
    fasta_file=open(path+'fasta/sequences_x10_noclip.fasta','w')
    for header,sequence in fastas_dic.items():
        fasta_file.write(">"+header.rstrip("\n")+"\n")
        fasta_file.write(sequence.rstrip("\n")+"\n")
    fasta_file.close()        

def write_fastas_x50(fastas_dic):
    fasta_file=open(path+'fasta/sequences_x50_noclip.fasta','w')
    for header,sequence in fastas_dic.items():
        fasta_file.write(">"+header.rstrip("\n")+"\n")
        fasta_file.write(sequence.rstrip("\n")+"\n")
    fasta_file.close()  

def write_fastas_x100(fastas_dic):
    fasta_file=open(path+'fasta/sequences_x100_noclip.fasta','w')
    for header,sequence in fastas_dic.items():
        fasta_file.write(">"+header.rstrip("\n")+"\n")
        fasta_file.write(sequence.rstrip("\n")+"\n")
    fasta_file.close()  

def write_fastas_x200(fastas_dic):
    fasta_file=open(path+'fasta/sequences_x200_noclip.fasta','w')
    for header,sequence in fastas_dic.items():
        fasta_file.write(">"+header.rstrip("\n")+"\n")
        fasta_file.write(sequence.rstrip("\n")+"\n")
    fasta_file.close()  

write_fastas_x10(fasta_x10)
write_fastas_x50(fasta_x50)
write_fastas_x100(fasta_x100)
write_fastas_x200(fasta_x200)