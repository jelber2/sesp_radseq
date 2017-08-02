#! /usr/bin/env python

# PBS cluster job submission in Python
# bcl2fastq
# By Jean P. Elbers
# jean.elbers@gmail.com
# Last modified 1 August 2017
###############################################################################
Usage = """

00-bcl2fastq.py - version 1.0

Command:
1.Processes bcl files and outputs Undetermined.R1.fastq.gz and Undetermined.R2.fastq.gz
    ~/bin/bcl2fastq/bin/bin/bcl2fastq --input-dir InDir \
    --output-dir OutDir --use-bases-mask y*,i*,i*,y* \
    --no-lane-splitting --create-fastq-for-index-reads \
    --sample-sheet Sample-sheet.csv

Directory info:
InDir = /work/jelber2/radseq/bcl
Input Files = *.bcl
OutDir = /work/jelber2/radseq/fastq
Important Output Files = Undetermined_S0_R1_001.fastq.gz
                         Undetermined_S0_R2_001.fastq.gz

Usage (execute following code in InDir):

python ~/scripts/sesp_radseq/00-bcl2fastq.py --InDir InDir --OutDir OutDir --SampleSheet SampleSheet.csv

"""
###############################################################################
import os, sys, subprocess, re , argparse

class FullPaths(argparse.Action):
    """Expand user- and relative-paths"""
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, os.path.abspath(os.path.expanduser(values)))

def is_dir(dirname):
    if not os.path.isdir(dirname):
        msg = "{0} is not a directory".format(dirname)
        raise argparse.ArgumentTypeError(msg)
    else:
        return dirname

def get_args():
    """Get arguments from CLI"""
    parser = argparse.ArgumentParser(
            description="""\nRuns bcl2fastq on NextSeq 3RAD with molecular tags libraries""")
    parser.add_argument(
            "--InDir",
            required=True,
            action=FullPaths,
            help="""Path to Input Directory of bcl files, ex: /work/jelber2/sesp_radseq/bcl/"""
        )
    parser.add_argument(
            "--OutDir",
            required=True,
            action=FullPaths,
            help="""Path to Output Directory for fastq.gz files, ex: /work/jelber2/sesp_radseq/fastq/"""
        )
    parser.add_argument(
            "--SampleSheet",
            required=True,
            action=FullPaths,
            help="""Path to Sample-Sheet.csv, ex: /work/jelber2/sesp_radseq/bcl/Sample-sheet.csv"""
        )
    return parser.parse_args()

def main():
    args = get_args()
    SampleSheet = args.SampleSheet
    InDir = args.InDir
    OutDir = args.OutDir
    os.chdir(InDir)
    if not os.path.exists(OutDir):
        os.mkdir(OutDir) # if OutDir does not exist, then make it
    # Customize your options here
    Queue = "workq"
    Allocation = "hpc_sesp"
    Processors = "nodes=1:ppn=16"
    WallTime = "04:00:00"
    LogOut = OutDir
    LogMerge = "oe"
    JobName = "bcl2fastq"
    Command = """
    ~/bin/bcl2fastq/bin/bin/bcl2fastq --input-dir %s \
    --output-dir %s --use-bases-mask y*,i*,i*,y* \
    --no-lane-splitting --create-fastq-for-index-reads \
    --sample-sheet %s""" % (InDir, OutDir, SampleSheet)

    JobString = """
    #!/bin/bash
    #PBS -q %s
    #PBS -A %s
    #PBS -l %s
    #PBS -l walltime=%s
    #PBS -o %s
    #PBS -j %s
    #PBS -N %s

    cd %s
    %s\n""" % (Queue, Allocation, Processors, WallTime, LogOut, LogMerge, JobName, InDir, Command)

    #Create pipe to qsub
    proc = subprocess.Popen(['qsub'], shell=True,
      stdin=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=True)
    (child_stdout, child_stdin) = (proc.stdout, proc.stdin)

    #Print JobString
    jobname = proc.communicate(JobString)[0]
    print JobString
    print jobname

if __name__ == '__main__':
    main()
