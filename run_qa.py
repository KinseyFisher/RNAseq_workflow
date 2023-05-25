#!/usr/bin/python

import argparse, subprocess, os, re, csv
from argparse import RawTextHelpFormatter


parser = argparse.ArgumentParser(
    description=""" This will run idxstats from samtools on a directory of indexed bam
    files. It also prints a summary of mapping efficiency computed
    from idxstats.  """, formatter_class=RawTextHelpFormatter)
    
parser.add_argument("infolder", type=str,
                    help="Directory where the indexed bam files are. Doesn't work with nested directories.")
parser.add_argument("outfolder", type=str,
                    help="Directory to put the reports")

args = parser.parse_args()


### Testing
### If you want to mess around with the script, you can uncomment these lines

# class empty:
#     def __init__(self):
#         pass

# args = empty()
# args.infolder = "/Users/cs/git/celegans_rnaseq/BAM"
# args.outfolder = "/Users/cs/git/celegans_rnaseq/qa"

### End Testing

try:
    os.mkdir(args.outfolder)
except OSError:
    pass


     
idxStatsCommand = "samtools idxstats %s > %s"


files = os.listdir( args.infolder )
bams = [ i for i in files if re.search('bam$', i)]
bams.sort()
mappingEfficiency = [("sample", "total_mapped", "total_unmapped", "efficiency")]
for bam in bams:
    print "Processing sample %s" % bam
    outNameBase = os.path.join(args.outfolder, os.path.splitext(bam)[0])
    inName = os.path.join( args.infolder, bam)
    idxCall = idxStatsCommand % (inName, outNameBase + "_stats.txt")
    subprocess.call(idxCall, shell=True )
    with open(outNameBase + "_stats.txt", "r") as f:
        totalMapped = 0
        totalUnmapped = 0
        for line in f:
            chrom, length, mapped, unmapped = line.split()
            totalMapped += int(mapped)
            totalUnmapped += int(unmapped)
        mappingEfficiency.append((bam, totalMapped, totalUnmapped, totalMapped/float(totalUnmapped+totalMapped)))

with open(os.path.join(args.outfolder, "mapping_summary.txt"), 'w') as out:
    outCSV = csv.writer(out, delimiter="\t")
    for samp in mappingEfficiency:
        outCSV.writerow(samp)
                     
                     
