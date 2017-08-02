#! /usr/bin/env python

# PBS cluster job submission in Python
# Stacks clone_filter
# By Jean P. Elbers
# jean.elbers@gmail.com
# Last modified 24 Jan 2017
###############################################################################
Usage = """

01c-clone_filter.py - version 1.0

Command:
1.Processes each set of R1 and R2 files for a sample
        ~/bin/stacks-1.44/clone_filter -i gzfastq --null_index --oligo_len_2 8 \
       -1 Sample.1.fq.gz \
       -2 Sample.2.fq.gz \
       -o OutDir

2.Combine fq.gz files
        cd OutDir
        cat Sample.1.1.fq.gz Sample.2.2.fq.gz > Sample.fq.gz

Directory info:
InDir = /work/jelber2/radseq/samplefastq
Input Files = Sample.1.fq.gz, Sample.2.fq.gz
OutDir = /work/jelber2/radseq/declonedfastq
Important Output Files = Sample.1.1.fq.gz, Sample.2.2.fq.gz

Usage (execute following code in InDir):

python ~/scripts/sesp_radseq/01c-clone_filter.py --barcodes barcodes.txt --OutDir OutDir

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
            description="""\nRuns Stacks process_radtags on each sample in barcodes.txt file""")
    parser.add_argument(
            "--barcodes",
            required=True,
            action=FullPaths,
            help="""barcodes file in form Barcode1tabBarcode2tabSample"""
        )
    parser.add_argument(
            "--OutDir",
            required=True,
            action=FullPaths,
            help="""Path to output directory, ex: /work/jelber2/declonedfastq/"""
        )
    return parser.parse_args()

def main():
    args = get_args()
    barcodes = args.barcodes
    InDir = os.getcwd()
    OutDir = args.OutDir
    os.chdir(InDir)
    if not os.path.exists(OutDir):
        os.mkdir(OutDir) # if OutDir does not exist, then make it
    InFile = open(barcodes, 'r')
    rawdatalist = []
    for line in InFile:
        x = line.strip("\n").split("\t")
        rawdatalist.append(x)

    InFile.close()

    for item in rawdatalist:
        Sample = item[2]
        # Customize your options here
        Queue = "single"
        Allocation = "hpc_sesp"
        Processors = "nodes=1:ppn=1"
        WallTime = "04:00:00"
        LogOut = OutDir
        LogMerge = "oe"
        JobName = "cfilter-%s" % (Sample)
        Command = """
        ~/bin/stacks-1.44/clone_filter -i gzfastq --null_index --oligo_len_2 8 \
       -1 %s.1.fq.gz \
       -2 %s.2.fq.gz \
       -o %s
        cd %s
        cat %s.1.1.fq.gz %s.2.2.fq.gz > %s.fq.gz""" % \
        (Sample, Sample, OutDir, OutDir, Sample, Sample, Sample)

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
