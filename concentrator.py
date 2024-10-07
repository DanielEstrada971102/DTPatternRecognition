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
import pickle

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
            histograms = None,
            outfolder = outfolder, 
            outfilename = outfilename,
            maxfiles = maxfiles,
            postfix = parameters[0]
        )

        t = ntuplizer.tree
        _maxevents = maxevents if maxevents > 0 and maxevents < t.GetEntries() else t.GetEntries()

        color_msg(f"Scanning events", "purple")
        for iev, root_ev in enumerate(ntuplizer.tree):
            if iev%(_maxevents/10) == 0: 
                color_msg("Event: %d"%iev, "yellow")
            if iev >= _maxevents: break # A programmer cries when seeing this :)

            ev = Event(root_ev, iev)

            if (r := ntuplizer.run(ev)) is not None:
                ntuplizer.events.append(r)

        color_msg("Events scan done!", color="blue")
        color_msg(f"After filter,  there are {len(ntuplizer.events)} events", color="blue")

        if dumpmode == "pickle" or dumpmode == "both":
            color_msg(f"Dumping ntuple into a pickleable file...", color="blue")
            with open(f"{outfolder}/ntuplizer{parameters[0]}{outfilename}.pkl", "wb") as file:
                pickle.dump(ntuplizer, file)

        if dumpmode == "root" or dumpmode == "both":
            color_msg(f"Filling histograms...", color="purple")
            ntuplizer.histograms = histos

            for iev, ev in enumerate(ntuplizer.events):
                ntuplizer.fill_histograms(ev)

            color_msg(f"Saving histograms...", color="purple")
            ntuplizer.save_histograms()

        color_msg(f"Done!", color="green")