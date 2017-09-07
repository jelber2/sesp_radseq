#! /usr/bin/env python

# PBS cluster job submission in Python
# Stacks pstacks
# By Jean P. Elbers
# jean.elbers@gmail.com
# Last modified 1 August 2017
###############################################################################
Usage = """

02b-pstacks.py - version 1.0

Command:
1.Runs pstacks on each sample
        ~/bin/stacks-1.44/pstacks -t bam -p 8 -f Sample.bam -o ./ -i X -m 3
         mv pstacks.log pstacks.Sample.log
Directory info:
InDir = /work/jelber2/radseq/processed
Input Files = Sample.fq.gz

Usage (execute following code in InDir):

python ~/scripts/sesp_radseq/02b-pstacks.py --barcodes barcodes.txt

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
            description="""\nRuns Stacks pstacks on each sample in barcodes.txt file""")
    parser.add_argument(
            "--barcodes",
            required=True,
            action=FullPaths,
            help="""barcodes file in form Barcode1tabBarcode2tabSample"""
        )
    return parser.parse_args()

def main():
    args = get_args()
    barcodes = args.barcodes
    InDir = os.getcwd()
    OutDir = InDir
    InFile = open(barcodes, 'r')
    rawdatalist = []
    X = 0
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
        WallTime = "01:00:00"
        LogOut = OutDir
        LogMerge = "oe"
        JobName = "pstacks-%s" % (Sample)
        Command = """
        ~/bin/stacks-1.44/pstacks -t bam -p 1 -f %s.bam -o ./ -i %d -m 3
         mv pstacks.log pstacks.%s.log""" % (Sample, X, Sample)

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
        X += 1

if __name__ == '__main__':
    main()
