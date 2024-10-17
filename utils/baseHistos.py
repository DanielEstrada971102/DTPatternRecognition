""" Histograms to be stored in the output rootfiles """
import ROOT as r
import utils.functions as fcns
from utils.functions import color_msg
dummyVal = -9999
# Make Iterators for when we want to iterate over different subdetectors
wheels   = range(-2, 3)
sectors  = range(1, 15)
stations = range(1, 5)
# -- These are computed using the baseline selection
histos = {}

# Efficiencies per station
histos.update({
    "seg_eff_MB1" :  {  
      "type" : "eff",
      "histoDen" : r.TH1D(f"Eff_MB1_AM_total", r';Wheel; Events', 5, -2.5 , 2.5),
      "histoNum" : r.TH1D(f"Eff_MB1_AM_num", r';Wheel; Events', 5, -2.5 , 2.5),
      "func"     : lambda reader: [seg.wh for seg in fcns.get_best_matches( reader, station = 1 )], # These are the values to fill with
      # These are the conditions on whether to fill numerator also. Imitating Jaime's code:
      # https://github.com/jaimeleonh/DTNtuples/blob/unifiedPerf/test/DTNtupleTPGSimAnalyzer_Efficiency.C#L443
      # Basically, for a best matching segment, if there's a bestTP candidate, fill the numerator.
      "numdef"   : lambda reader: [len(seg.matches) > 0 for seg in fcns.get_best_matches( reader, station = 1 ) ] 
  },
  "seg_eff_MB2" :  {  
      "type" : "eff",
      "histoDen" : r.TH1D(f"Eff_MB2_AM_total", r';Wheel; Events', 5, -2.5 , 2.5),
      "histoNum" : r.TH1D(f"Eff_MB2_AM_num", r';Wheel; Events', 5, -2.5 , 2.5),
      "func"     : lambda reader: [seg.wh for seg in fcns.get_best_matches( reader, station = 2 )], # These are the values to fill with
      # These are the conditions on whether to fill numerator also. Imitating Jaime's code:
      # https://github.com/jaimeleonh/DTNtuples/blob/unifiedPerf/test/DTNtupleTPGSimAnalyzer_Efficiency.C#L443
      # Basically, for a best matching segment, if there's a bestTP candidate, fill the numerator.
      "numdef"   : lambda reader: [len(seg.matches) > 0 for seg in fcns.get_best_matches( reader, station = 2 ) ] 
  },
  "seg_eff_MB3" :  {  
      "type" : "eff",
      "histoDen" : r.TH1D(f"Eff_MB3_AM_total", r';Wheel; Events', 5, -2.5 , 2.5),
      "histoNum" : r.TH1D(f"Eff_MB3_AM_num", r';Wheel; Events', 5, -2.5 , 2.5),
      "func"     : lambda reader: [seg.wh for seg in fcns.get_best_matches( reader, station = 3 )], # These are the values to fill with
      # These are the conditions on whether to fill numerator also. Imitating Jaime's code:
      # https://github.com/jaimeleonh/DTNtuples/blob/unifiedPerf/test/DTNtupleTPGSimAnalyzer_Efficiency.C#L443
      # Basically, for a best matching segment, if there's a bestTP candidate, fill the numerator.
      "numdef"   : lambda reader: [len(seg.matches) > 0 for seg in fcns.get_best_matches( reader, station = 3 ) ] 
  },
  "seg_eff_MB4" :  {  
      "type" : "eff",
      "histoDen" : r.TH1D(f"Eff_MB4_AM_total", r';Wheel; Events', 5, -2.5 , 2.5),
      "histoNum" : r.TH1D(f"Eff_MB4_AM_num", r';Wheel; Events', 5, -2.5 , 2.5),
      "func"     : lambda reader: [seg.wh for seg in fcns.get_best_matches( reader, station = 4 )], # These are the values to fill with
      # These are the conditions on whether to fill numerator also. Imitating Jaime's code:
      # https://github.com/jaimeleonh/DTNtuples/blob/unifiedPerf/test/DTNtupleTPGSimAnalyzer_Efficiency.C#L443
      # Basically, for a best matching segment, if there's a bestTP candidate, fill the numerator.
      "numdef"   : lambda reader: [len(seg.matches) > 0 for seg in fcns.get_best_matches( reader, station = 4 ) ] 
  },
})

# ------------------------------ strange definitions (?) -----------------------------------------

histos.update({
  "shower_eff_muon_pt" :  {  
      "type" : "eff",
      "histoDen" : r.TH1D("Shower_eff_muon_pt_total", r';Wheel; Events', 20, 0 , 1000),
      "histoNum" : r.TH1D("Shower_eff_muon_pt_num", r';Wheel; Events', 20, 0 , 1000),
      "func"     : lambda reader: [gm.pt for gm in reader.genmuons if gm.did_shower()], 
      "numdef"   : lambda reader: [ len(reader.showers) > 0 ] 
  },
  "shower_eff_muon_eta" :  {  
      "type" : "eff",
      "histoDen" : r.TH1D("Shower_eff_muon_eta_total", r';Wheel; Events', 20, -1 , 1),
      "histoNum" : r.TH1D("Shower_eff_muon_eta_num", r';Wheel; Events', 20, -1 , 1),
      "func"     : lambda reader: [gm.eta for gm in reader.genmuons if gm.did_shower()], 
      "numdef"   : lambda reader: [ len(reader.showers) > 0 ] 
  }
})
# -----------------------------------------------------------------------------------------------
histos.update({
  # --- Leading muon properties
  "LeadingMuon_pt" : {
    "type" : "distribution",
    "histo" : r.TH1D("LeadingMuon_pt", r';Leading muon p_T; Events', 20, 0 , 1000),
    "func" : lambda reader: reader.genmuons[0].pt,
  },
  "LeadingMuon_eta" : {
    "type" : "distribution",
    "histo" : r.TH1D("LeadingMuon_eta", r';Leading muon #eta; Events', 10, -3 , 3),
    "func" : lambda reader: reader.genmuons[0].eta,
  },
  "LeadingMuon_maxDPhi" : {
    "type" : "distribution",
    "histo" : r.TH1D("LeadingMuon_maxDPhi", r';Leading muon maximum #Delta#phi (with matched segments); Events', 20, 0 , 0.6),
    "func" : lambda reader: reader.genmuons[0].get_max_dphi()
  },
  "LeadingMuon_maxDEta" : {
    "type" : "distribution",
    "histo" : r.TH1D("LeadingMuon_Max_dEta", r';Leading muon maximum #Delta#eta (with matched segments); Events', 20, 0 , 1),
    "func" : lambda reader: reader.genmuons[0].get_max_deta()
  },
  
  # --- Subleading muon properties
  "SubLeadingMuon_pt" : {
    "type" : "distribution",
    "histo" : r.TH1D("SubLeadingMuon_pt", r';Subleading muon p_T; Events', 20, 0 , 1000),
    "func" : lambda reader: reader.genmuons[1].pt if len(reader.genmuons) > 1 else dummyVal,
  },
  "SubLeadingMuon_eta" : {
    "type" : "distribution",
    "histo" : r.TH1D("SubLeadingMuon_eta", r';Subleading muon #eta; Events', 10, -3 , 3),
    "func" : lambda reader: reader.genmuons[1].eta if len(reader.genmuons) > 1 else dummyVal,
  },
  "SubLeadingMuon_maxDPhi" : {
    "type" : "distribution",
    "histo" : r.TH1D("SubLeadingMuon_maxDPhi", r';Subleading muon maximum #Delta#phi (with matched segments); Events', 20, 0 , 0.6),
    "func" : lambda reader: reader.genmuons[1].get_max_dphi() if len(reader.genmuons) > 1 else dummyVal
  },
  "SubLeadingMuon_maxDEta" : {
    "type" : "distribution",
    "histo" : r.TH1D("SubLeadingMuon_Max_dEta", r';Subleading muon maximum #Delta#eta (with matched segments); Events', 20, 0 , 1),
    "func" : lambda reader: reader.genmuons[1].get_max_deta() if len(reader.genmuons) > 1 else dummyVal
  },
  
  # --- Muon relations
  "muon_DR" : {
    "type" : "distribution",
    "histo" : r.TH1D("muon_DR", r';#DeltaR both muons; Events', 20, 1 , 6),
    "func" : lambda reader: fcns.deltaR( reader.genmuons[0], reader.genmuons[1] ) if len(reader.genmuons) > 1 else dummyVal,
  },
  "nGenMuons" : {
    "type" : "distribution",
    "histo" : r.TH1D("nGenMuons", r';Number of generator muons; Events', 20, -3 , 3),
    "func" : lambda reader: len(reader.genmuons),
  },
})

# --- Showering muon properties
histos.update({
    "dphimax_seg_showering_muon" : {
      "type" : "distribution",
      "histo" : r.TH1D("dphimax_showering_muon", r';Max #Delta#phi Seg showering muon; Events', 60, 0 , 0.3),
      "func" : lambda reader: [gm.get_dphimax_segments() for gm in reader.genmuons if gm.did_shower()],
    },
    "dphimax_seg_non_showering_muon" : {
      "type" : "distribution",
      "histo" : r.TH1D("dphimax_non_showering_muon", r';Max #Delta#phi Seg non-showering muon; Events', 60, 0 , 0.3),
      "func" : lambda reader: [gm.get_dphimax_segments() for gm in reader.genmuons if not gm.did_shower()],
    },
    "dphimax_tp_showering_muon" : {
      "type" : "distribution",
      "histo" : r.TH1D("dphimax_tp_showering_muon", r';Max #Delta#phi TP showering muon; Events', 60, 0 , 0.3),
      "func" : lambda reader: [gm.get_dphimax_tp() for gm in reader.genmuons if gm.did_shower()],
    },
    "dphimax_tp_non_showering_muon" : {
      "type" : "distribution",
      "histo" : r.TH1D("dphimax_tp_non_showering_muon", r';Max #Delta#phi TP non-showering muon; Events', 60, 0 , 0.3),
      "func" : lambda reader: [gm.get_dphimax_tp() for gm in reader.genmuons if not gm.did_shower()],
    },
    "dphi_seg_showering_muon" : {
      "type" : "distribution",
      "histo" : r.TH1D("dphi_showering_muon", r';#Delta#phi Seg showering muon; Events', 60, 0 , 0.3),
      "func" : lambda reader: [gm.get_dphi_segments() for gm in reader.genmuons if gm.did_shower()],
    },
    "dphi_seg_non_showering_muon" : {
      "type" : "distribution",
      "histo" : r.TH1D("dphi_non_showering_muon", r';#Delta#phi Seg non-showering muon; Events', 60, 0 , 0.3),
      "func" : lambda reader: [gm.get_dphi_segments() for gm in reader.genmuons if not gm.did_shower()],
    },
    "dphi_tp_showering_muon" : {
      "type" : "distribution",
      "histo" : r.TH1D("dphi_tp_showering_muon", r';#Delta#phi TP showering muon; Events', 60, 0 , 0.3),
      "func" : lambda reader: [gm.get_dphi_tp() for gm in reader.genmuons if gm.did_shower()],
    },
    "dphi_tp_non_showering_muon" : {
      "type" : "distribution",
      "histo" : r.TH1D("dphi_tp_non_showering_muon", r';#Delta#phi TP non-showering muon; Events', 60, 0 , 0.3),
      "func" : lambda reader: [gm.get_dphi_tp() for gm in reader.genmuons if not gm.did_shower()],
    },
})

# --------------------- destrada (.)_(.) ----------------------
# number of showers
histos.update({
  "nTrueShowers" : {
    "type" : "distribution",
    "histo" : r.TH1D("nTrueShowers", r'; n;', 2, 0 , 2),
    "func" : lambda reader: [gm.did_shower() for gm in reader.genmuons],
  },
  "nEmuShowers" : {
    "type" : "distribution",
    "histo" : r.TH1D("nEmuShowers", r'; n;', 2, 0 , 2),
    "func" : lambda reader: [1 for shower in reader.showers],
  },
  "nShowers2Comp" : {
    "type" : "distribution",
    "histo" : r.TH1D("nShowers2Comp", r'; n;', 2, 0 , 2),
    "func" : lambda reader: [1 for shower in reader.showers2comp],
  },
  "nPyShowers" : {
    "type" : "distribution",
    "histo" : r.TH1D("nPyShowers", r'; n;', 2, 0 , 2),
    "func" : lambda reader: [1 for shower in reader.pyshowers],
  },
})

vars = {
  "nDigis": (50, 0, 500),
  "avg_pos": (50, 0, 400),
  "avg_time": (50, 0, 4000),
  "wh": (5, -2.5, 2.5),
  "st": (4, 0, 4),
  "sc": (14, 0, 14),
}
# emuShowers => showers built on cmssw emulator
histos.update({
  "emuShowers_n4ev":{
    "type": "distribution",
    "histo" : r.TH1D("emuShowers_n4ev", r'; emuShowers_n; Events', 50, 0 , 50),
    "func" : lambda reader: size if (size := len(reader.showers)) > 0 else None,
  },
})
for var, range_ in vars.items():
  histos.update({
    "emuShowers_" + var:{
      "type": "distribution",
      "histo" : r.TH1D("emuShowers_" + var, r'; emuShowers_{0}; Events'.format(var), *range_),
      "func" : lambda reader, var=var: [getattr(shower, var) for shower in reader.showers],
    },
  })

# showers2comp => showers re-built in python to compare
histos.update({ 
  "showers2comp_n4ev":{
    "type": "distribution",
    "histo" : r.TH1D("showers2comp_n4ev", r'; showers2comp_n; Events', 50, 0 , 50),
    "func" : lambda reader: size if (size := len(reader.showers2comp)) > 0 else None,
  },
})
for var, range_ in vars.items():
  histos.update({
    "showers2comp_" + var:{
      "type": "distribution",
      "histo" : r.TH1D("showers2comp_" + var, r'; showers2comp_{0}; Events'.format(var), *range_),
      "func" : lambda reader, var=var: [getattr(shower, var) for shower in reader.showers2comp],
    },
  })

# pyShowers => built in python checking by SL
histos.update({
  "pyShower_n4ev":{
    "type": "distribution",
    "histo" : r.TH1D("pyShower_n4ev", r'; pyShower_n; Events', 50, 0 , 50),
    "func" : lambda reader: size if (size := len(reader.pyshowers)) > 0 else None,
  },
})
for var, range_ in vars.items():
  histos.update({
    "pyShower_" + var:{
      "type": "distribution",
      "histo" : r.TH1D("pyShower_" + var, r'; pyShower_{0}; Events'.format(var), *range_),
      "func" : lambda reader, var=var: [getattr(shower, var) for shower in reader.pyshowers],
    },
  })

# ------------- using emuShowers ---------------
# true positive ratio --> segments which loc matches with any shower / segments (relative to showered genmuons)
for st in stations:
  histos.update({ 
    "seg_m_emushower_tprgm_MB" + str(st):{ 
        "type": "eff",
        "histoDen" : r.TH1D(f"Seg_m_emushower_tprgm_MB{st}_total", r';Wheel; Events', 5, -2.5 , 2.5),
        "histoNum" : r.TH1D(f"Seg_m_emushower_tprgm_MB{st}_num", r';Wheel; Events', 5, -2.5 , 2.5),
        "func"     : lambda reader, st=st: [seg.wh for seg in fcns.get_best_matches( reader, station = st, _4showereds = True )],
        "numdef"   : lambda reader, st=st: [
            ((seg.sc, seg.wh) in fcns.get_shower_locs( reader, station = st))
            for seg in fcns.get_best_matches( reader, station = st, _4showereds = True )
          ],
    },
  })

# fake positive ratio --> segments which loc matches with any shower / segments (relative to non showered genmuons)
for st in stations:
  histos.update({ 
  "seg_m_emushower_fprgm_MB" + str(st):{
      "type": "eff",
      "histoDen" : r.TH1D(f"Seg_m_emushower_fprgm_MB{st}_total", r';Wheel; Events', 5, -2.5 , 2.5),
      "histoNum" : r.TH1D(f"Seg_m_emushower_fprgm_MB{st}_num", r';Wheel; Events', 5, -2.5 , 2.5),
      "func"     : lambda reader, st=st: [seg.wh for seg in fcns.get_best_matches( reader, station = st, _4showereds = False)],
      "numdef"   : lambda reader, st=st: [
          ((seg.sc, seg.wh) in fcns.get_shower_locs( reader, station = st))
          for seg in fcns.get_best_matches( reader, station = st, _4showereds = False)
        ],
    },
  })

  # ------------- using Showers2comp -------------------
# true positive ratio --> segments which loc matches with any shower / segments (relative to showered genmuons)
for st in stations:
  histos.update({ 
    "seg_m_shower2comp_tprgm_MB" + str(st):{ 
        "type": "eff",
        "histoDen" : r.TH1D(f"Seg_m_shower2comp_tprgm_MB{st}_total", r';Wheel; Events', 5, -2.5 , 2.5),
        "histoNum" : r.TH1D(f"Seg_m_shower2comp_tprgm_MB{st}_num", r';Wheel; Events', 5, -2.5 , 2.5),
        "func"     : lambda reader, st=st: [seg.wh for seg in fcns.get_best_matches( reader, station = st, _4showereds = True )],
        "numdef"   : lambda reader, st=st: [
            ((seg.sc, seg.wh) in fcns.get_shower_locs( reader, station = st, shower2comp = True))
            for seg in fcns.get_best_matches( reader, station = st, _4showereds = True )
          ],
    },
  })

# fake positive ratio --> segments which loc matches with any shower / segments (relative to non showered genmuons)
for st in stations:
  histos.update({ 
  "seg_m_shower2comp_fprgm_MB" + str(st):{
      "type": "eff",
      "histoDen" : r.TH1D(f"Seg_m_shower2comp_fprgm_MB{st}_total", r';Wheel; Events', 5, -2.5 , 2.5),
      "histoNum" : r.TH1D(f"Seg_m_shower2comp_fprgm_MB{st}_num", r';Wheel; Events', 5, -2.5 , 2.5),
      "func"     : lambda reader, st=st: [seg.wh for seg in fcns.get_best_matches( reader, station = st, _4showereds = False)],
      "numdef"   : lambda reader, st=st: [
          ((seg.sc, seg.wh) in fcns.get_shower_locs( reader, station = st, shower2comp = True))
          for seg in fcns.get_best_matches( reader, station = st, _4showereds = False)
        ],
    },
  })

# ------------- using pyShowers -------------------
# true positive ratio --> segments which loc matches with any shower / segments (relative to showered genmuons)
for st in stations:
  histos.update({ 
    "seg_m_pyshower_tprgm_MB" + str(st):{ 
        "type": "eff",
        "histoDen" : r.TH1D(f"Seg_m_pyshower_tprgm_MB{st}_total", r';Wheel; Events', 5, -2.5 , 2.5),
        "histoNum" : r.TH1D(f"Seg_m_pyshower_tprgm_MB{st}_num", r';Wheel; Events', 5, -2.5 , 2.5),
        "func"     : lambda reader, st=st: [seg.wh for seg in fcns.get_best_matches( reader, station = st, _4showereds = True )],
        "numdef"   : lambda reader, st=st: [
            ((seg.sc, seg.wh) in fcns.get_shower_locs( reader, station = st, pyshower = True))
            for seg in fcns.get_best_matches( reader, station = st, _4showereds = True )
          ],
    },
  })

# fake positive ratio --> segments which loc matches with any shower / segments (relative to non showered genmuons)
for st in stations:
  histos.update({ 
  "seg_m_pyshower_fprgm_MB" + str(st):{
      "type": "eff",
      "histoDen" : r.TH1D(f"Seg_m_pyshower_fprgm_MB{st}_total", r';Wheel; Events', 5, -2.5 , 2.5),
      "histoNum" : r.TH1D(f"Seg_m_pyshower_fprgm_MB{st}_num", r';Wheel; Events', 5, -2.5 , 2.5),
      "func"     : lambda reader, st=st: [seg.wh for seg in fcns.get_best_matches( reader, station = st, _4showereds = False)],
      "numdef"   : lambda reader, st=st: [
          ((seg.sc, seg.wh) in fcns.get_shower_locs( reader, station = st, pyshower = True))
          for seg in fcns.get_best_matches( reader, station = st, _4showereds = False)
        ],
    },
  })

# --------- for check how much differ from emulator shower those computed in python ----------------
for st in stations:
  histos.update({ 
  "eff_shower2comp_eq2Emu_MB" + str(st):{
      "type": "eff",
      "histoDen" : r.TH1D(f"eff_shower2comp_eq2Emu_MB{st}_total", r';Wheel; Events', 5, -2.5 , 2.5),
      "histoNum" : r.TH1D(f"eff_shower2comp_eq2Emu_MB{st}_num", r';Wheel; Events', 5, -2.5 , 2.5),
      "func"     : lambda reader, st=st: [shower.wh for shower in reader.showers2comp if shower.st == st],
      "numdef"   : lambda reader, st=st: [shower.eq2Emulator for shower in reader.showers2comp  if shower.st == st],
    },
  })
for st in stations:
  histos.update({ 
  "eff_pyshower_eq2Emu_MB" + str(st):{
      "type": "eff",
      "histoDen" : r.TH1D(f"eff_pyshower_eq2Emu_MB{st}_total", r';Wheel; Events', 5, -2.5 , 2.5),
      "histoNum" : r.TH1D(f"eff_pyshower_eq2Emu_MB{st}_num", r';Wheel; Events', 5, -2.5 , 2.5),
      "func"     : lambda reader, st=st: [shower.wh for shower in reader.pyshowers if shower.st == st],
      "numdef"   : lambda reader, st=st: [shower.eq2Emulator for shower in reader.pyshowers if shower.st == st],
    },
  })

# --------- Digi wire info for events with GenMuons That do Not Showered -> (gmtns) ---------------
# wire ocupancy 
for st in stations:
  histos.update({
      "digi_w_gmtns_MB" + str(st):{
      "type": "distribution2d",
      "histo" : r.TH2I(f"digi_w_gmtns_MB" + str(st), r';Wheel; Events', 5, -2.5, 2.5, 200, 0, 200),
      "func" : lambda reader, st = st: [
        (digi.wh, digi.w) for digi in fcns.get_digis_by_station(reader, station=st)
      ],
    },
  })

# wire distribution relative to mean --> (w - avg_w)
for st in stations:
  histos.update({
    "digi_wd_gmtns_MB" + str(st):{
      "type": "distribution2d",
      "histo" : r.TH2D(f"digi_wd_gmtns_MB" + str(st), r';Wheel; Events', 5, -2.5, 2.5, 200, -100, 100),
      "func" : lambda reader, st=st: [
        (digi.wh, digi.w - fcns.get_digis_mean(reader))
        for digi in fcns.get_digis_by_station(reader, station=st)
      ],
    },
  })  

# length of wires --> l = (w.min - wire.max)
for st in stations:
  histos.update({
    "digi_wl_gmtns_MB" + str(st):{
      "type": "distribution2d",
      "histo" : r.TH2D(f"digi_wl_gmtns_MB" + str(st), r';Wheel; Events', 5, -2.5, 2.5, 200, 0, 200),
      "func" : lambda reader, st=st: [
        (digi.wh, fcns.get_digis_length(reader)) for digi in fcns.get_digis_by_station(reader, station=st)
      ],
    },
  })  

# --------- Digi wire info for events with GenMmuons That Showered -> (gmts) ---------------

# digis wire ocupancy 
for st in stations:
  histos.update({
      "digi_w_gmts_MB" + str(st):{
      "type": "distribution2d",
      "histo" : r.TH2I(f"digi_w_gmts_MB" + str(st), r';Wheel; Events', 5, -2.5, 2.5, 200, 0, 200),
      "func" : lambda reader, st = st: [
        (digi.wh, digi.w) for digi in fcns.get_digis_by_station(reader, station=st, _4showereds=True)
      ],
    },
  })

# digis wire distribution relative to mean --> (w - avg_w)
for st in stations:
  histos.update({
    "digi_wd_gmts_MB" + str(st):{
      "type": "distribution2d",
      "histo" : r.TH2D(f"digi_wd_gmts_MB" + str(st), r';Wheel; Events', 5, -2.5, 2.5, 200, -100, 100),
      "func" : lambda reader, st=st: [
        (digi.wh, digi.w - fcns.get_digis_mean(reader)) 
        for digi in fcns.get_digis_by_station(reader, station=st, _4showereds=True)
      ],
    },
  })  

# digis length of wires --> l = (w.min - wire.max)
for st in stations:
  histos.update({
    "digi_wl_gmts_MB" + str(st):{
      "type": "distribution2d",
      "histo" : r.TH2D(f"digi_wl_gmts_MB" + str(st), r';Wheel; Events', 5, -2.5, 2.5, 200, 0, 200),
      "func" : lambda reader, st=st: [
        (digi.wh, fcns.get_digis_length(reader))
        for digi in fcns.get_digis_by_station(reader, station=st, _4showereds=True)
      ],
    },
  })  
