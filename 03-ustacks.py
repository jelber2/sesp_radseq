#! /usr/bin/env python

# PBS cluster job submission in Python
# Stacks ustacks
# By Jean P. Elbers
# jean.elbers@gmail.com
# Last modified 1 August 2017
###############################################################################
Usage = """

03-ustacks.py - version 1.0

Command:
1.Runs ustacks on each sample
        ~/bin/stacks-1.44/ustacks -i x -t gzfastq \
        -f Sample.fq.gz -p 8 -M 3 -r -d -o ./
         mv ustacks.log ustacks.Sample.log
Directory info:
InDir = /work/jelber2/radseq/processed
Input Files = Sample.fq.gz

Usage (execute following code in InDir):

python ~/scripts/sesp_radseq/03-ustacks.py --barcodes barcodes.txt

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
            description="""\nRuns Stacks ustacks on each sample in barcodes.txt file""")
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
    OutDir = "ustacks"
    if not os.path.exists(OutDir):
        os.mkdir(OutDir) # if OutDir does not exist, then make it
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
        Queue = "workq"
        Allocation = "hpc_sesp"
        Processors = "nodes=1:ppn=8"
        WallTime = "01:00:00"
        LogOut = OutDir
        LogMerge = "oe"
        JobName = "ustacks-%s" % (Sample)
        Command = """
        ~/bin/stacks-1.44/ustacks -i %d -t gzfastq \
        -f %s.fq.gz -p 8 -M 3 -r -d -o ../%s/""" % (X, Sample, OutDir)

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
