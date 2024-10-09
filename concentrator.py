''' Script to make concentrator studies '''
import os
import sys
from optparse import OptionParser
import ROOT as r
import numpy as np

from utils.ntuple_reader import Ntuple
from utils.event_builder import Event
from utils.functions import color_msg
import filters
from utils.baseHistos import histos
from multiprocessing import cpu_count, Pool

def addConcentratorOptions(pr):
    pr.add_option('--inpath', '-i', type="string", dest = "inpath", default = ".")

    # Additional
    pr.add_option("--outfolder", "-o", type="string", dest = "outfolder", default = "./results")
    pr.add_option('--outfilename', type=str, dest = "outfilename", default = '')
    pr.add_option('--maxfiles', type=int, dest = "maxfiles", default = -1)
    pr.add_option('--maxevents', type=int, dest = "maxevents", default = -1)

    pr.add_option('--dumpmode', type=str, dest = "dumpmode", default = "root")


if __name__ == "__main__":
    pr = OptionParser(usage="%prog [options]")
    addConcentratorOptions(pr)
    (options, args) = pr.parse_args()

    inpath = options.inpath
    outfolder = options.outfolder
    maxfiles = options.maxfiles
    maxevents = options.maxevents
    dumpmode = options.dumpmode
    outfilename = options.outfilename

    # Analyses to be run
    # (postfix, filters)
    run_over = [
    ("_AM_withShowers", [filters.baseline]),
    #("_AM_vetoShowers", [filters.baseline, filters.removeShower])
    ]

    # Process pool

    for parameters in run_over:
        color_msg(f"Shower performance analyzer: {parameters[0]} ", "green")
        ntuplizer = Ntuple(
            inputFolder = inpath, 
            selectors = parameters[1],
            histograms = histos,
            outfolder = outfolder, 
            outfilename = outfilename,
            maxfiles = maxfiles,
            postfix = parameters[0]
        )

        t = ntuplizer.tree
        _maxevents = maxevents if maxevents > 0 and maxevents < t.GetEntries() else t.GetEntries()

        if dumpmode == "root":
            color_msg(f"Filling histograms...", color="purple")

            for ev in ntuplizer.events:
                if ev.iev%(_maxevents/10) == 0: 
                    color_msg("Event: %d"%ev.iev, "yellow")
                if ev.iev >= _maxevents: break # A programmer cries when seeing this :)

                ntuplizer.fill_histograms(ev)

            color_msg(f"Saving histograms...", color="purple")
            ntuplizer.save_histograms()

        color_msg(f"Done!", color="green")