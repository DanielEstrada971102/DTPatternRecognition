import os
from optparse import OptionParser

from utils.ntuple_reader import Ntuple
from utils.event_builder import Event
from utils.functions import color_msg
from utils.baseHistos import histos
import pickle
from tqdm import tqdm

def addConcentratorOptions(pr):
    pr.add_option('--inpath', '-i', type="string", dest = "inpath", default = ".")

    # Additional
    pr.add_option("--outfolder", "-o", type="string", dest = "outfolder", default = "./results")
    pr.add_option('--maxfiles', type=int, dest = "maxfiles", default = -1)


if __name__ == "__main__":
    pr = OptionParser(usage="%prog [options]")
    addConcentratorOptions(pr)
    (options, args) = pr.parse_args()

    inpath = options.inpath
    outfolder = options.outfolder
    maxfiles = options.maxfiles

    Files = []

    if "pkl" in inpath:
        color_msg(f"Opening input file {inpath}", "blue", 1)
        maxfiles = 1
        Files.append(inpath)

    else:
        color_msg(f"Opening input files from {inpath}", "blue", 1)
        allFiles = os.listdir(inpath)
        nFiles = len(allFiles) if maxfiles==-1 else min(len(allFiles), maxfiles)
        maxfiles = nFiles

        for iF in range( nFiles ):
            if "pkl" not in allFiles[iF]: continue
            color_msg(f"File {allFiles[iF]} added", indentLevel=2)
            Files.append( os.path.join(inpath, allFiles[iF]))

    for ntuple_file in Files:
        color_msg(f"Getting events...", color='blue', indentLevel=1)
        with open(ntuple_file, "rb") as loader:
            ntuplizer = pickle.load(loader)
        color_msg(f"{len(ntuplizer.events)} events were gotten from {ntuple_file}", color='purple', indentLevel=1)
        color_msg(f"Filling histogramas...", color='yellow', indentLevel=1)

        ntuplizer.histograms = histos
        for ev in tqdm(ntuplizer.events):
            ntuplizer.fill_histograms(ev)

        color_msg(f"Saving histogramas...", color='yellow', indentLevel=1)
        ntuplizer.outfilename = "_" + ntuple_file.split("_")[-1][:-4]
        ntuplizer.save_histograms()
        color_msg(f"Done!", color='purple', indentLevel=1)
    color_msg(f"End", color='green')

