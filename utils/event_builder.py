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
    # --------- Digis --------- #
    self.digis = [ digi(root_ev, idigi) for idigi in range(root_ev.digi_nDigis) ]
    # --------- Offline segments --------- #
    self.segments = [ segment( root_ev, iseg) for iseg in range(root_ev.seg_nSegments) if root_ev.seg_phi_t0[iseg] > -500 ] # keep only good segments
    # --------- Ph2 TPs --------- #
    self.tps = [ ph2tpg(root_ev, itp) for itp in range(root_ev.ph2TpgPhiEmuAm_nTrigs) ]
    # --------- Showers --------- #
    self.showers = [ shower(root_ev, ishower) for ishower in range(len(root_ev.ph2Shower_station)) ]
    # --------- Generator level muons --------- #
    self.genmuons = sorted(
      [
        gen_muon(m, root_ev.gen_pt[m], root_ev.gen_eta[m], root_ev.gen_phi[m], root_ev.gen_charge[m]) 
        for m in range(root_ev.gen_nGenParts) if abs(root_ev.gen_pdgId[m]) == 13
      ],
      key=lambda m: m.pt,
      reverse=True,
    )
    

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
