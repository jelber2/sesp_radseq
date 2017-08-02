#! /usr/bin/env python

# PBS cluster job submission in Python
# Stacks ustacks
# By Jean P. Elbers
# jean.elbers@gmail.com
# Last modified 1 May 2017
###############################################################################
Usage = """

05-populations.py - version 1.1

Command:
1.Runs populations on all samples
    ~/bin/stacks-1.44/populations -P ./ -b 1 -p 1 --max_obs_het 0.5 \
    -M popmap.txt -t 16 -m 6 -r 0.74 --fasta --vcf
Directory info:
InDir = /work/jelber2/radseq/processed

Usage (execute following code in InDir):

python ~/scripts/sesp_radseq/05-populations.py --popmap popmap.txt

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
            description="""\nRuns Stacks populations on allsamples in popmap.txt file""")
    parser.add_argument(
            "--popmap",
            required=True,
            action=FullPaths,
            help="""popmap file in form SampletabPopulationNumber"""
        )
    return parser.parse_args()

def main():
    args = get_args()
    popmap = args.popmap
    InDir = os.getcwd()
    OutDir = InDir
    # Customize your options here
    Queue = "workq"
    Allocation = "hpc_sesp"
    Processors = "nodes=1:ppn=16"
    WallTime = "04:00:00"
    LogOut = OutDir
    LogMerge = "oe"
    JobName = "populations"
    Command = """
    ~/bin/stacks-1.44/populations -P ./ -b 1 -p 1 --max_obs_het 0.5 \
    -M %s -t 16 -m 6 -r 0.74 --fasta --vcf""" % (popmap)

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
