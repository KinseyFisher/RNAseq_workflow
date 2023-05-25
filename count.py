#!/usr/bin/python

import argparse, subprocess, os, re

parser = argparse.ArgumentParser(
    description="""  """)
    
parser.add_argument("infolder", type=str,
                    help="Directory where bam files are")
parser.add_argument("outfolder", type=str,
                    help="Directory to put the count files")
parser.add_argument("gtf", type=str,
                    help="Location of the GTF file")
parser.add_argument("-t", "--stranded", type=str,
                    default = "no",
                    help="Is the library stranded? (This is passed directly to the htseq-count script as its '-s' option)")
args = parser.parse_args()


### Testing

# class empty:
#     def __init__(self):
#         pass

# args = empty()
# args.infolder = "BAM"
# args.outfolder = "counts"
# args.gtf = "GTF/GFF_for_cuffdiff_clean.gtf"
# args.stranded = "no"
# args.samtools_location = "/home/cmaxwell/labhome.cmaxwell/local/samtools-1.1/samtools"
# aFile = os.listdir(args.infolder)[1]


try:
    os.mkdir(args.outfolder)
except OSError:
    pass


# Takes one string format arguments:
# 1) The name of the BAM file
# 2) The name of the output count file
pipeCommandHTSeq = " ".join([
    "python -m HTSeq.scripts.count",
    "-f bam", # Expects a bam file
    "-s %s" % args.stranded, # tell it what kind of strandedness you got
    "%s", # This is the filtered bam file
    args.gtf, # this is the GTF file    
    "> %s"]) # This is the file to write to

for aFile in os.listdir(args.infolder):
    if not re.search("\.bam$", aFile):
        continue
    print aFile
    fileName = os.path.join(args.infolder, aFile)
    baseName = os.path.splitext(aFile)[0]
    outName = os.path.join(args.outfolder, baseName + ".counts")
    # Format the string
    htseqCall = pipeCommandHTSeq % (fileName, outName)
    # Do the call
    subprocess.call(htseqCall, shell=True)

