""" 
Module to read ntuples and produce flat root files from which to plot performance
"""

# -- Import libraries -- #
import ROOT as r
import os
import json
import math
from numpy import ndarray
from inspect import isgenerator
import re
from utils.event_builder import Event
from utils.functions import color_msg, flatten

class Ntuple(object):
  def __init__(self, 
              inputFolder, 
              selectors,
              histograms,
              outfolder = "results", 
              outfilename = "",
              maxevents = -1, 
              maxfiles = -1, 
              postfix = ""):
    # Save in attributes
    self.inputFolder = inputFolder
    self.selectors = selectors
    self.histograms = histograms
    self.outfolder = outfolder
    self.outfilename = outfilename
    self.maxfiles = maxfiles
    self.postfix = postfix

    # Prepare output
    self.create_outfolder(outfolder)

    # Prepare input
    self.load_tree(inputFolder)
    self.thr = int(re.findall(r'\d+', outfilename)[0])
    self.events = ( ev for iev, root_ev in enumerate(self.tree) if (ev := self.run(Event(root_ev, iev, thr=self.thr))) )


  def run(self, ev: Event):
    ev.analyze_matches()
    # Apply global selection
    if not self.passes_event(ev): pass
    else: return ev


  def passes_event(self, ev: Event):
    """ The selector is used to apply global cuts on the events """
    return all(selector(ev) for selector in self.selectors)


  def fill_histograms(self, ev: Event):
    """ Apply selections and fill histograms """
    for histo, histoinfo in self.histograms.items():
      hType = histoinfo["type"]

      # Distributions
      if hType == "distribution":
        h = histoinfo["histo"]
        func = histoinfo["func"]
        val = func(ev)

        # In case a function returns multiple results
        # and we want to fill for everything (e.g. there are multiple muons,
        # each of them with a matching segment. And we want to account for everything)
        
        if isinstance(val, (list, tuple, ndarray)) or isgenerator(val):
          val = flatten(val)
          for ival in val:
            h.Fill( ival )
        elif val:
          h.Fill(val)

      # Efficiencies
      elif hType == "eff":
        func = histoinfo["func"]
        num = histoinfo["histoNum"]
        den = histoinfo["histoDen"]
        numdef = histoinfo["numdef"]

        val = func(ev)
        numPasses = numdef(ev)

        for val, passes in zip(val, numPasses):
          den.Fill(val)
          if passes:
            num.Fill(val)  

      elif hType == "distribution2d":
        h = histoinfo["histo"]
        func = histoinfo["func"]
        val = func(ev)
        
        for ival in val:
          h.Fill( *ival )

  def load_tree(self, inpath):
    """ Simple function to retrieve a chain with all the trees to be analyzed """
    self.tree = r.TChain()

    if "root" in inpath:
      color_msg(f"Opening input file {inpath}", "blue", 1)
      self.tree.Add(inpath + "/dtNtupleProducer/DTTREE")
      self.maxfiles = 1

    else:
      color_msg(f"Opening input files from {inpath}", "blue", 1)
      allFiles = os.listdir(inpath)
      nFiles = len(allFiles) if self.maxfiles==-1 else min(len(allFiles), self.maxfiles)
      self.maxfiles = nFiles

      for iF in range( nFiles ):
        if "root" not in allFiles[iF]: continue
        color_msg(f"File {allFiles[iF]} added", indentLevel=2)
        self.tree.Add( os.path.join(inpath, allFiles[iF]) + "/dtNtupleProducer/DTTREE")


  def create_outfolder(self, outname):
    """ Create an output path where to store the histograms """
    if not(os.path.exists(outname)): 
      os.system("mkdir -p %s"%outname)
      os.system("cp utils/index.php %s/"%outname)


  def save_histograms(self):
    """ Method to store histograms in a rootfile """
    outname = os.path.join(self.outfolder, "histograms%s%s.root"%(self.postfix,self.outfilename))
    f = r.TFile.Open(outname, "RECREATE")
    for hname, histoinfo in self.histograms.items():
      hType = histoinfo["type"]
      if "distribution" in hType:
        histo = histoinfo["histo"]
        histo.Write(histo.GetName())

      elif hType == "eff":
        histoNum = histoinfo["histoNum"]
        histoDen = histoinfo["histoDen"]
        histoNum.Write(histoNum.GetName())
        histoDen.Write(histoDen.GetName())

    f.Close()