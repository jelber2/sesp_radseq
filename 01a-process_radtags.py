#! /usr/bin/env python

# PBS cluster job submission in Python
# Stacks process_radtags on plates
# By Jean P. Elbers
# jean.elbers@gmail.com
# Last modified 24 Jan 2017
###############################################################################
Usage = """

01a-process_radtags.py - version 1.0

Command:
1.Processes plate barcodes
    ~/bin/stacks-1.44/process_radtags \
    -i gzfastq \
    -1 Read1 \
    -2 Read2 \
    -b i7barcodes \
    -r --index_null --disable_rad_check --retain_header
    mv process_radtags.log logname

Directory info:
InDir = /work/jelber2/radseq/fastq
Input Files = Undetermined_S0_R1_001.fastq.gz, Undetermined_S0_R2_001.fastq.gz
OutDir = InDir
Important Output Files = Plate.1.fq.gz, Plate.2.fq.gz

Usage (execute following code in InDir):

python ~/scripts/sesp_radseq/01a-process_radtags.py --Read1 R1.fastq.gz --Read2 R2.fastq.gz --i7barcodes barcodes.txt --logname process-radtags-plate1.log

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
            description="""\nRuns Stacks process_radtags on each plate in barcodes.txt file""")
    parser.add_argument(
            "--Read1",
            required=True,
            action=FullPaths,
            help="""Path to Read1 file"""
        )
    parser.add_argument(
            "--Read2",
            required=True,
            action=FullPaths,
            help="""Path to Read2 file"""
        )
    parser.add_argument(
            "--i7barcodes",
            required=True,
            action=FullPaths,
            help="""i7barcodes file in form i7barcodetabPlate"""
        )
    parser.add_argument(
            "--logname",
            required=True,
            help="""name of log file"""
        )
    return parser.parse_args()

def main():
    args = get_args()
    Read1 = args.Read1
    Read2 = args.Read2
    i7barcodes = args.i7barcodes
    logname = args.logname
    InDir = os.getcwd()
    OutDir = InDir
    # Customize your options here
    Queue = "single"
    Allocation = "hpc_sesp"
    Processors = "nodes=1:ppn=1"
    WallTime = "04:00:00"
    LogOut = OutDir
    LogMerge = "oe"
    JobName = "pradtags-plates"
    Command = """
    ~/bin/stacks-1.44/process_radtags \
    -i gzfastq \
    -1 %s \
    -2 %s \
    -b %s \
    -r --index_null --disable_rad_check --retain_header
    mv process_radtags.log %s""" % (Read1, Read2, i7barcodes, logname)

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
