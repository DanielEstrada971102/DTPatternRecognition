"""" Plotting script """
import os
from optparse import OptionParser
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

def make_eff_plot_perWheel(
        file,
        histo_name,
        plot_name,
        legend="",
        legend_pos=(0.62, 0.37, 0.70, 0.45),
        outfolder = "results/plots",
    ):
    """ Make a plot of the efficiency per wheel - histo_name must contain MBX indentifier"""
    # --- Define metadata for the plot
    nBins = 20
    binFirst = 0
    binLast = 20
    maxY = 1.05  

    total_num = r.TH1D( f"{plot_name}_num", "", 20, 0, 20)
    total_den = r.TH1D( f"{plot_name}_den", "", 20, 0, 20)

    f = r.TFile.Open( file )
    pre, pos = histo_name.split("MB")
    nums = [ deepcopy( f.Get( f"{pre}MB{ist}{pos[1:]}_num")) for ist in range(1, 5) ]    
    dens = [ deepcopy( f.Get(f"{pre}MB{ist}{pos[1:]}_total")) for ist in range(1, 5) ]    

    f.Close()

    for iWheel in range(1, 6):
        for iStation in range(1, 5):
            iBin = 4 * (iStation-1) + iWheel + (iStation != 1)*(iStation - 1) 
            total_num.SetBinContent( iBin, nums[ iStation - 1 ].GetBinContent(iWheel))
            total_den.SetBinContent( iBin, dens[ iStation - 1 ].GetBinContent(iWheel))
    
    effgr = get_eff(total_num, total_den)
    graphs = [ (effgr, legend) ]
    f.Close()
        
    # Now plot the graphs
    plot_graphs(
        graphs = graphs, 
        name = plot_name, 
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
        legend_pos = legend_pos,
        outfolder = outfolder
    )

    return graphs


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

    if "root" in inpath:
        color_msg(f"Opening input file {inpath}", "blue")
        maxfiles = 1
        Files.append(inpath)

    else:
        color_msg(f"Opening input files from {inpath}", "blue")
        allFiles = os.listdir(inpath)
        nFiles = len(allFiles) if maxfiles==-1 else min(len(allFiles), maxfiles)
        maxfiles = nFiles

        for iF in range( nFiles ):
            if "root" not in allFiles[iF]: continue
            color_msg(f"File {allFiles[iF]} added", indentLevel=1)
            Files.append( os.path.join(inpath, allFiles[iF]))

    color_msg("Making plots...", color="purple")
    for file in Files:
        outfolder = "results/plots_"+ file.split("_")[-1][:-4]
        # --- Plot for segment matching efficiency --- #
        _=make_eff_plot_perWheel( 
            file=file,
            histo_name="Eff_MBX_AM",
            plot_name="eff_segment_AM",
            legend="AM",
            outfolder = outfolder,
        )
        # --- Efficienct plot for segments that match with a shower when gemmuon is showered
        _=make_eff_plot_perWheel( 
            file=file,
            histo_name="Seg_m_shower_tprgm_MBX",
            plot_name="eff_seg_shower_tprgm",
            legend="#frac{showered genmuon's segments that match with any shower}{showered genmuon's segments}",
            legend_pos=(0.15, 0.87, 0.70, 0.75),
            outfolder = outfolder,
        )
        # --- Efficienct plot for segments that match with a shower when gemmuon is not showered
        _=make_eff_plot_perWheel( 
            file=file,
            histo_name="Seg_m_shower_fprgm_MBX",
            plot_name="eff_seg_shower_fprgm",
            legend="#frac{no showered genmuon's segments that match with any shower}{no showered genmuon's segments}",
            legend_pos=(0.15, 0.87, 0.70, 0.75),
            outfolder = outfolder,
        )
    color_msg("Done!", color="green")
