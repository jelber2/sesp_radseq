#! /usr/bin/env python

# PBS cluster job submission in Python
# Stacks process_radtags on samples
# By Jean P. Elbers
# jean.elbers@gmail.com
# Last modified 24 Jan 2017
###############################################################################
Usage = """

01b-process_radtags.py - version 1.0

Command:
1.Processes sample barcodes
    ~/bin/stacks-1.44/process_radtags \
    -i gzfastq \
    -1 Read1 \
    -2 Read2 \
    -b barcodes \
    -q -c --filter_illumina -r -t 140 \
    --inline_inline --renz_1 xbaI --renz_2 ecoRI --retain_header \
    -o OutDir
    mv OutDir/process_radtags.log OutDir/logname

Directory info:
InDir = /work/jelber2/radseq/platefastq
Input Files = Plate.1.fq.gz, Plate.2.fq.gz
OutDir = /work/jelber2/radseq/samplefastq
Important Output Files = Sample.1.fq.gz, Sample.2.fq.gz

Usage (execute following code in InDir):

python ~/scripts/sesp_radseq/01b-process_radtags.py --Read1 R1.fq.gz --Read2 R2.fq.gz --barcodes barcodes.txt --logname process-radtags-plate1.log --OutDir OutDir

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
            description="""\nRuns Stacks process_radtags on each sample in the barcodes file""")
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
            "--barcodes",
            required=True,
            action=FullPaths,
            help="""barcodes file in form Barcode1tabBarcode2tabSample"""
        )
    parser.add_argument(
            "--logname",
            required=True,
            help="""name of log file"""
        )
    parser.add_argument(
            "--OutDir",
            required=True,
            action=FullPaths,
            help="""Path to output directory, ex: /work/jelber2/samplefastq/"""
        )
    return parser.parse_args()

def main():
    args = get_args()
    Read1 = args.Read1
    Read2 = args.Read2
    barcodes = args.barcodes
    logname = args.logname
    InDir = os.getcwd()
    OutDir = args.OutDir
    os.chdir(InDir)
    if not os.path.exists(OutDir):
        os.mkdir(OutDir) # if OutDir does not exist, then make it
    # Customize your options here
    Queue = "single"
    Allocation = "hpc_sesp"
    Processors = "nodes=1:ppn=1"
    WallTime = "72:00:00"
    LogOut = OutDir
    LogMerge = "oe"
    JobName = "pradtags-plate-samples"
    Command = """
    ~/bin/stacks-1.44/process_radtags \
    -i gzfastq \
    -1 %s \
    -2 %s \
    -b %s \
    -q -c --filter_illumina -r -t 140 \
    --inline_inline --renz_1 xbaI --renz_2 ecoRI --retain_header \
    -o %s
    mv %s/process_radtags.log %s/%s""" % \
    (Read1, Read2, barcodes, OutDir, OutDir, OutDir, logname)

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
