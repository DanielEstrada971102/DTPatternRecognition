""" 
Module to produce single event class with respective particles (genmuons, segs, tps, ...).
"""

# -- Import modules -- #
from utils.functions import color_msg, flatten
from particles.segment import segment
from particles.gen_muon import gen_muon
from particles.shower import shower
from particles.ph2TriggerPrimitives import ph2tpg
from particles.digis import digi


class Event():
  __slot__=['iev', 'digis', 'segments', 'tps', 'showers', 'genmuons']
  def __init__(self, root_ev, iev=-1):
    self.iev = iev
    self.digis = []
    self.segments = []
    self.tps = []
    self.showers = []
    self.genmuons = []

    self.build_topology(root_ev)


  def analyze_matches(self):
    for gm in self.genmuons:
      # Match segments to generator muons
      for seg in self.segments:
        # gm.match_segment(seg, math.pi / 6., 0.8)
        gm.match_segment(seg, 0.1, 0.3)
      # Now re-match with TPs
      matched_segments = gm.matches
      for seg in matched_segments:
        for tp in self.tps:
          seg.match_offline_to_AM( tp, max_dPhi = 0.1 )


  def build_topology(self, ev):
    """
    ---------------------------------------------------------
            Event reconstruction method
    ---------------------------------------------------------
    This method reconstructs the information of the different
    DT related objects: digis, offline segments and TPs.
    ---------------------------------------------------------
    """

    # --------- Digis --------- #
    for idigi in range(ev.digi_nDigis):
      self.digis.append( digi(ev, idigi) )

    # --------- Offline segments --------- #
    for iseg in range(ev.seg_nSegments):
      if ev.seg_phi_t0[iseg] > -500: self.segments.append( segment(ev, iseg) ) # keep only good segments

    # --------- Ph2 TPs --------- #
    for itp in range(ev.ph2TpgPhiEmuAm_nTrigs):
      self.tps.append( ph2tpg(ev, itp) )
    
    # --------- Showers --------- #
    nShowerObj = len(ev.ph2Shower_station)
    for iShower in range(nShowerObj):
      self.showers.append( shower(ev, iShower) )

    # --------- Generator level muons --------- #
    for m in range(ev.gen_nGenParts):
      if abs(ev.gen_pdgId[m]) == 13:
        self.genmuons.append(
            gen_muon(m, ev.gen_pt[m], ev.gen_eta[m], ev.gen_phi[m], ev.gen_charge[m])
          )
    # Sort generator muons by pT
    if self.genmuons is not None: self.genmuons.sort( key = lambda m : m.pt, reverse = True) 


  def summarize(self):
    """ Method to show a small description of what has been recorded in this event """

    color_msg( f"------ Event {self.iev} info ------", indentLevel = 1)
    color_msg( f"Generator muons", color = "green", indentLevel = 2)
    for igm, gm in enumerate(self.genmuons):
      color_msg( f"Muon {igm}", indentLevel = 3)
      gm.summarize(3)
    
    color_msg( f"Offline segments", color = "green", indentLevel = 2)
    color_msg( f"Number of segments: {len(self.segments)}", indentLevel = 3) # There might be a lot of segments so don't print everything
    phiseg = [f"({seg.index:.2f}, {seg.phi:.2f}, {seg.eta:.2f})" for seg in self.segments]
    color_msg( f"(iSeg, Phi, eta): {phiseg}", indentLevel = 3) # There might be a lot of segments so don't print everything
    color_msg( f"Trigger primitives", color = "green", indentLevel = 2)
    color_msg( f"Number of TPs: {len(self.tps)}", indentLevel = 3) # There might be a lot of segments so don't print everything
    color_msg( f"Showers", color = "green", indentLevel = 2)
    color_msg( f"Number of showers: {len(self.showers)}", indentLevel = 3)
