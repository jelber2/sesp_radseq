#!/bin/bash
#
###############################################################################
#
# "000-make-bwa-index.sh" SuperMikeII script 
# created by Jean P. Elbers
# jean.elbers@gmail.com
# last edited 1 August 2017
#
###############################################################################
#
#PBS -q single
#PBS -A hpc_sesp
#PBS -l nodes=1:ppn=1
#PBS -l walltime=02:00:00
#PBS -o /work/jelber2/radseq
#PBS -j oe
#PBS -N 000-make-bwa-index.sh

# Let's mark the time things get started with a date-time stamp.

date

# Set work directory

export WORK_DIR=/work/jelber2/radseq/

# makes bwa index

cd $WORK_DIR
~/bin/bwa-0.7.15/bwa index -a bwtsw \
-p 44394_ref_Zonotrichia_albicollis-1.0.1_chrUn \
44394_ref_Zonotrichia_albicollis-1.0.1_chrUn.fa.gz
