#! /usr/bin/env python

# PBS cluster job submission in Python
# Stacks ustacks
# By Jean P. Elbers
# jean.elbers@gmail.com
# Last modified 6 Sep 2017
###############################################################################
Usage = """

03-cstacks.py - version 1.0

Command:
1.Runs cstacks on all samples
    ~/bin/stacks-1.44/cstacks -p 16 -n 4 -b batch \
    -s Sample1 \
    -s Sample2 \
    -s Sample3 \
    -s SampleN \
    -o ./ 
Directory info:
InDir = /work/jelber2/radseq/processed

Usage (execute following code in InDir):

python ~/scripts/sesp_radseq/03-cstacks.py --barcodes barcodes.txt --batch 1

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
            description="""\nRuns Stacks cstacks on allsamples in barcodes.txt file""")
    parser.add_argument(
            "--barcodes",
            required=True,
            action=FullPaths,
            help="""barcodes file in form Barcode1tabBarcode2tabSample"""
        )
    parser.add_argument(
            "--batch",
            required=True,
            type=int,
            help="""batch number (1 for SESP, 2 for BACS)"""
        )
    return parser.parse_args()

def main():
    args = get_args()
    barcodes = args.barcodes
    batch = args.batch
    InDir = os.getcwd()
    OutDir = InDir
    InFile = open(barcodes, 'r')
    rawdatalist = []
    for line in InFile:
        x = line.strip("\n").split("\t")
        rawdatalist.append(x)
    InFile.close()
    Samples = []
    for item in rawdatalist:
        Sample = item[2]
        SampleString = "    -s "+Sample+" \\"
        Samples.append(SampleString)
    SamplesString = '\n'.join(Samples)
    # Customize your options here
    Queue = "workq"
    Allocation = "hpc_sesp"
    Processors = "nodes=1:ppn=16"
    WallTime = "04:00:00"
    LogOut = OutDir
    LogMerge = "oe"
    JobName = """cstacks-batch_%s""" % (batch)
    Command = """
    ~/bin/stacks-1.44/cstacks -p 16 -n 4 -b %s \
    %s
    -o ./ """ % (batch, SamplesString)

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
