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


histo_names = [
    # 'seg_eff_MB1',
    # 'seg_eff_MB2',
    # 'seg_eff_MB3',
    # 'seg_eff_MB4',
    # 'shower_eff_muon_pt',
    # 'shower_eff_muon_eta',
    'LeadingMuon_pt',
    'LeadingMuon_eta',
    'LeadingMuon_maxDPhi',
    'LeadingMuon_maxDEta',
    'SubLeadingMuon_pt',
    'SubLeadingMuon_eta',
    'SubLeadingMuon_maxDPhi',
    'SubLeadingMuon_maxDEta',
    # 'muon_DR',
    # 'nGenMuons',
    'nTrueShowers',
    'dphimax_seg_showering_muon',
    'dphimax_seg_non_showering_muon',
    'dphimax_tp_showering_muon',
    'dphimax_tp_non_showering_muon',
    'dphi_seg_showering_muon',
    'dphi_seg_non_showering_muon',
    'dphi_tp_showering_muon',
    'dphi_tp_non_showering_muon',
    'emuShowers_n',
    'emuShowers_nDigis',
    'emuShowers_avg_pos',
    'emuShowers_avg_time',
    'emuShowers_wh',
    'emuShowers_st',
    'emuShowers_sec',
    'showers2comp_n',
    'showers2comp_nDigis',
    'showers2comp_avg_pos',
    'showers2comp_avg_time',
    'showers2comp_wh',
    'showers2comp_st',
    'showers2comp_sec',
    'pyShower_n',
    'pyShower_nDigis',
    'pyShower_avg_pos',
    'pyShower_avg_time',
    'pyShower_wh',
    'pyShower_st',
    'pyShower_sec',
    # 'seg_m_shower_tprgm_MB1',
    # 'seg_m_shower_tprgm_MB2',
    # 'seg_m_shower_tprgm_MB3',
    # 'seg_m_shower_tprgm_MB4',
    # 'seg_m_shower_fprgm_MB1',
    # 'seg_m_shower_fprgm_MB2',
    # 'seg_m_shower_fprgm_MB3',
    # 'seg_m_shower_fprgm_MB4',
    "digi_w_MB1",
    "digi_w_MB2",
    "digi_w_MB3",
    "digi_w_MB4",
]


def addConcentratorOptions(pr):
    pr.add_option('--inpath',
    '-i', type="string", dest = "inpath", default = ".")

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
            histograms = {key: value for key, value in histos.items() if key in histo_names},
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