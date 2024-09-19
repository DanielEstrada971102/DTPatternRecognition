"""" Plotting script """
import os
from optparse import OptionParser
import ROOT as r
import numpy as np
from utils.functions import color_msg, plot_graphs
import ROOT as r
from copy import deepcopy

def get_eff(num, den):
    eff = r.TEfficiency(num,  den)
    effgr = eff.CreateGraph()
    for ibin in range(effgr.GetN()):
        effgr.SetPointEXhigh(ibin, 0)
        effgr.SetPointEXlow(ibin, 0)
    return effgr

def make_segment_eff_perWheel( files, outfolder = "results/plots"):
    """ Make a plot of the AM efficiency """
    # --- Define metadata for the plot
    name = "eff_segment_AM" 
    nBins = 20
    binFirst = 0
    binLast = 20
    maxY = 1.05  

    graphs = []
    for iFile, fileInfo in enumerate(files):
        total_num = r.TH1D( f"{name}_{iFile}_num", "", 20, 0, 20)
        total_den = r.TH1D( f"{name}_{iFile}_den", "", 20, 0, 20)

        f = r.TFile.Open( fileInfo[0] )
        nums = [ deepcopy( f.Get(f"Eff_MB{ist}_AM_matched")) for ist in range(1, 5) ]    
        dens = [ deepcopy( f.Get(f"Eff_MB{ist}_total")) for ist in range(1, 5) ]    
        f.Close()

        for iWheel in range(1, 6):
            for iStation in range(1, 5):
                iBin = 4 * (iStation-1) + iWheel + (iStation != 1)*(iStation - 1) 
                total_num.SetBinContent( iBin, nums[ iStation - 1 ].GetBinContent(iWheel))
                total_den.SetBinContent( iBin, dens[ iStation - 1 ].GetBinContent(iWheel))
        
        effgr = get_eff(total_num, total_den)
        graphs.append( (effgr, fileInfo[1]))
        f.Close()
        
    # Now plot the graphs
    plot_graphs(
        graphs = graphs, 
        name = name, 
        nBins = nBins, 
        firstBin = binFirst, 
        lastBin = binLast,
        xMin = -0.1, 
        xMax = 20.1,
        labels = ["-2", "-1", "0", "+1", "+2"]*4,
        maxY = maxY,
        notes =  [
            ("#bf{CMS} Phase-2 Simulation", (.08, .90, .5, .95), 0.05),
            ("200 PU", (.75, .90, .89, .95), 0.05),
            ("MB1",    (.14, .2,  .29, .40), 0.05),
            ("MB2",    (.34, .2,  .49, .40), 0.05),
            ("MB3",    (.54, .2,  .69, .40), 0.05),
            ("MB4",    (.74, .2,  .89, .40), 0.05),      
        ],
        lines = [
            (5, 0, 5, maxY),
            (10, 0, 10, maxY),
            (15, 0, 15, maxY)
        ],
        titleX = "DT Local Trigger Efficiency", 
        titleY = "Wheel",
        legend_pos = (0.62, 0.37, 0.70, 0.45),
        outfolder = outfolder
    )

    return graphs

# copied from previoud function - modified to plot shower efficiency
def make_shower_eff_perWheel( files, outfolder = "results/plots"):
    """ Make a plot of the shower algorithm efficiency """
    # --- Define metadata for the plot
    name = "eff_shower" 
    nBins = 20
    binFirst = 0
    binLast = 20
    maxY = 1.05  

    graphs = []
    for iFile, fileInfo in enumerate(files):
        total_num = r.TH1D( f"{name}_{iFile}_num", "", 20, 0, 20)
        total_den = r.TH1D( f"{name}_{iFile}_den", "", 20, 0, 20)

        f = r.TFile.Open( fileInfo[0] )
        nums = [ deepcopy( f.Get(f"Shower_eff_MB{ist}_shower_matched")) for ist in range(1, 5) ]    
        dens = [ deepcopy( f.Get(f"Shower_eff_MB{ist}_total")) for ist in range(1, 5) ]    
        f.Close()

        for iWheel in range(1, 6):
            for iStation in range(1, 5):
                iBin = 4 * (iStation-1) + iWheel + (iStation != 1)*(iStation - 1) 
                total_num.SetBinContent( iBin, nums[ iStation - 1 ].GetBinContent(iWheel))
                total_den.SetBinContent( iBin, dens[ iStation - 1 ].GetBinContent(iWheel))
        
        effgr = get_eff(total_num, total_den)
        graphs.append( (effgr, fileInfo[1]))
        f.Close()
        
    # Now plot the graphs
    plot_graphs(
        graphs = graphs, 
        name = name, 
        nBins = nBins, 
        firstBin = binFirst, 
        lastBin = binLast,
        xMin = -0.1, 
        xMax = 20.1,
        labels = ["-2", "-1", "0", "+1", "+2"]*4,
        maxY = maxY,
        notes =  [
            ("#bf{CMS} Phase-2 Simulation", (.08, .90, .5, .95), 0.05),
            ("200 PU", (.75, .90, .89, .95), 0.05),
            ("MB1",    (.14, .2,  .29, .40), 0.05),
            ("MB2",    (.34, .2,  .49, .40), 0.05),
            ("MB3",    (.54, .2,  .69, .40), 0.05),
            ("MB4",    (.74, .2,  .89, .40), 0.05),      
        ],
        lines = [
            (5, 0, 5, maxY),
            (10, 0, 10, maxY),
            (15, 0, 15, maxY)
        ],
        titleX = "DT Local Trigger Efficiency", 
        titleY = "Wheel",
        legend_pos = (0.20, 0.87, 0.70, 0.75),
        outfolder = outfolder
    )

    return graphs

def make_shower_fp_perWheel( files, outfolder = "results/plots"):
    """ Make a plot of the shower fake positive ratio """
    # --- Define metadata for the plot
    name = "eff_shower_fp" 
    nBins = 20
    binFirst = 0
    binLast = 20
    maxY = 1.05  

    graphs = []
    for iFile, fileInfo in enumerate(files):
        total_num = r.TH1D( f"{name}_{iFile}_num", "", 20, 0, 20)
        total_den = r.TH1D( f"{name}_{iFile}_den", "", 20, 0, 20)

        f = r.TFile.Open( fileInfo[0] )
        nums = [ deepcopy( f.Get(f"Shower_fp_MB{ist}_shower_fp")) for ist in range(1, 5) ]    
        dens = [ deepcopy( f.Get(f"Shower_fp_MB{ist}_shower_total")) for ist in range(1, 5) ]    
        f.Close()

        for iWheel in range(1, 6):
            for iStation in range(1, 5):
                iBin = 4 * (iStation-1) + iWheel + (iStation != 1)*(iStation - 1) 
                total_num.SetBinContent( iBin, nums[ iStation - 1 ].GetBinContent(iWheel))
                total_den.SetBinContent( iBin, dens[ iStation - 1 ].GetBinContent(iWheel))
        
        effgr = get_eff(total_num, total_den)
        graphs.append( (effgr, fileInfo[1]))
        f.Close()
        
    # Now plot the graphs
    plot_graphs(
        graphs = graphs, 
        name = name, 
        nBins = nBins, 
        firstBin = binFirst, 
        lastBin = binLast,
        xMin = -0.1, 
        xMax = 20.1,
        labels = ["-2", "-1", "0", "+1", "+2"]*4,
        maxY = maxY,
        notes =  [
            ("#bf{CMS} Phase-2 Simulation", (.08, .90, .5, .95), 0.05),
            ("200 PU", (.75, .90, .89, .95), 0.05),
            ("MB1",    (.14, .2,  .29, .40), 0.05),
            ("MB2",    (.34, .2,  .49, .40), 0.05),
            ("MB3",    (.54, .2,  .69, .40), 0.05),
            ("MB4",    (.74, .2,  .89, .40), 0.05),      
        ],
        lines = [
            (5, 0, 5, maxY),
            (10, 0, 10, maxY),
            (15, 0, 15, maxY)
        ],
        titleX = "DT Loca Trigger - FP shower's ratio", 
        titleY = "Wheel",
        legend_pos = (0.62, 0.37, 0.70, 0.45),
        outfolder = outfolder
    )

    return graphs

def make_shower_neff_perWheel( files, outfolder = "results/plots"):
    """ Make a plot of the shower algorithm efficiency """
    # --- Define metadata for the plot
    name = "neff_shower" 
    nBins = 20
    binFirst = 0
    binLast = 20
    maxY = 1.05  

    graphs = []
    for iFile, fileInfo in enumerate(files):
        total_num = r.TH1D( f"{name}_{iFile}_num", "", 20, 0, 20)
        total_den = r.TH1D( f"{name}_{iFile}_den", "", 20, 0, 20)

        f = r.TFile.Open( fileInfo[0] )
        nums = [ deepcopy( f.Get(f"Shower_neff_MB{ist}_shower_matched")) for ist in range(1, 5) ]    
        dens = [ deepcopy( f.Get(f"Shower_neff_MB{ist}_total")) for ist in range(1, 5) ]    
        f.Close()

        for iWheel in range(1, 6):
            for iStation in range(1, 5):
                iBin = 4 * (iStation-1) + iWheel + (iStation != 1)*(iStation - 1) 
                total_num.SetBinContent( iBin, nums[ iStation - 1 ].GetBinContent(iWheel))
                total_den.SetBinContent( iBin, dens[ iStation - 1 ].GetBinContent(iWheel))
        
        effgr = get_eff(total_num, total_den)
        graphs.append( (effgr, fileInfo[1]))
        f.Close()
        
    # Now plot the graphs
    plot_graphs(
        graphs = graphs, 
        name = name, 
        nBins = nBins, 
        firstBin = binFirst, 
        lastBin = binLast,
        xMin = -0.1, 
        xMax = 20.1,
        labels = ["-2", "-1", "0", "+1", "+2"]*4,
        maxY = maxY,
        notes =  [
            ("#bf{CMS} Phase-2 Simulation", (.08, .90, .5, .95), 0.05),
            ("200 PU", (.75, .90, .89, .95), 0.05),
            ("MB1",    (.14, .2,  .29, .40), 0.05),
            ("MB2",    (.34, .2,  .49, .40), 0.05),
            ("MB3",    (.54, .2,  .69, .40), 0.05),
            ("MB4",    (.74, .2,  .89, .40), 0.05),      
        ],
        lines = [
            (5, 0, 5, maxY),
            (10, 0, 10, maxY),
            (15, 0, 15, maxY)
        ],
        titleX = "DT Local Trigger Efficiency", 
        titleY = "Wheel",
        legend_pos = (0.15, 0.87, 0.70, 0.75),
        outfolder = outfolder
    )

    return graphs

if __name__ == "__main__":

    outfolder = "results/plots"
    # --- Plot for segment matching efficiency --- #
    make_segment_eff_perWheel( 
        [("results/histograms_AM_withShowers_histos.root", "AM")],
        outfolder = outfolder,
    )
    # --------------------------
    make_shower_eff_perWheel(
        [("results/histograms_AM_withShowers_histos.root", "#frac{showered genmuon's segments that match with any shower}{showered genmuon's segments}")],
        outfolder = outfolder,
    )
    make_shower_fp_perWheel(
        [("results/histograms_AM_withShowers_histos.root", "shower_fp")],
        outfolder = outfolder,
    )
    make_shower_neff_perWheel(
        [("results/histograms_AM_withShowers_histos.root", "#frac{no showered genmuon's segments that match with any shower}{no showered genmuon's segments}")],
        outfolder = outfolder,
    )