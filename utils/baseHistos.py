""" Histograms to be stored in the output rootfiles """
import ROOT as r
import utils.functions as fcns 
from utils.functions import color_msg
dummyVal = -9999
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
  
  # --- Leading muon properties
  "nTrueShowers" : {
    "type" : "distribution",
    "histo" : r.TH1D("nTrueShowers", r'; nTrueShowers; Events', 2, 0 , 2),
    "func" : lambda reader: [gm.did_shower() for gm in reader.genmuons],
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

  # ---- shower ---- (destrada (.)_(.)...)

histos.update({
  "nEvents":{
    "type": "distribution",
    "histo": r.TH1D("nEvents", r'; nDetectedShowers; Events', 1, 0.5 , 1.5),
    "func" : lambda reader: 1,
  }
})

histos.update({
  "nDetectedShowers":{
    "type": "distribution",
    "histo" : r.TH1D("nDetectedShowers", r'; nDetectedShowers; Events', 50, 0 , 50),
    "func" : lambda reader: len(reader.showers),
  },
  "nDigis_showers":{
    "type": "distribution",
    "histo" : r.TH1D("nDigis_showers", r'; nDigis_showers; Events', 50, 0 , 500),
    "func" : lambda reader: [shower.nDigis for shower in reader.showers],
  },
  "avg_pos_showers":{
    "type": "distribution",
    "histo" : r.TH1D("avg_pos_showers", r'; avg_pos_showers; Events', 50, 0 , 4000),
    "func" : lambda reader: [shower.avg_pos for shower in reader.showers],
  },
  "avg_time_showers":{
    "type": "distribution",
    "histo" : r.TH1D("avg_time_showers", r'; avg_time_showers; Events', 50, 0 , 4000),
    "func" : lambda reader: [shower.avg_time for shower in reader.showers],
  },
  "wh_showers":{
    "type": "distribution",
    "histo" : r.TH1D("wh_showers", r'; wh_showers; Events', 5, -2.5 , 2.5),
    "func" : lambda reader: [shower.wh for shower in reader.showers],
  },
  "st_showers":{
    "type": "distribution",
    "histo" : r.TH1D("st_showers", r'; st_showers; Events', 4, 0 , 4),
    "func" : lambda reader: [shower.st for shower in reader.showers],
  },
  "sec_showers":{
    "type": "distribution",
    "histo" : r.TH1D("sec_showers", r'; sec_showers; Events', 12, 0 , 12),
    "func" : lambda reader: [shower.sc for shower in reader.showers],
  },
})


histos.update({ # fake positive ratio --> fake showers / all showers (relative to showers)
  "shower_fprs_MB1":{
    "type": "eff",
    "histoDen" : r.TH1D(f"Shower_fprs_MB1_total", r';Wheel; Events', 5, -2.5 , 2.5),
    "histoNum" : r.TH1D(f"Shower_fprs_MB1_num", r';Wheel; Events', 5, -2.5 , 2.5),
    "func"     : lambda reader: [shower.wh for shower in fcns.get_shower_by_station(reader, station=1)],
    "numdef"   : lambda reader: [
      (shower.sc, shower.wh) in [(seg.sc, seg.wh) for seg in fcns.get_best_matches(reader, station = 1, _4showereds=False)] 
      for shower in fcns.get_shower_by_station(reader, station=1)
    ],
  },
  "shower_fprs_MB2":{
    "type": "eff",
    "histoDen" : r.TH1D(f"Shower_fprs_MB2_total", r';Wheel; Events', 5, -2.5 , 2.5),
    "histoNum" : r.TH1D(f"Shower_fprs_MB2_num", r';Wheel; Events', 5, -2.5 , 2.5),
    "func"     : lambda reader: [shower.wh for shower in fcns.get_shower_by_station(reader, station=2)],
    "numdef"   : lambda reader: [
      (shower.sc, shower.wh) in [(seg.sc, seg.wh) for seg in fcns.get_best_matches(reader, station = 2, _4showereds=False)] 
      for shower in fcns.get_shower_by_station(reader, station=2)
    ],
  },
  "shower_fprs_MB3":{
    "type": "eff",
    "histoDen" : r.TH1D(f"Shower_fprs_MB3_total", r';Wheel; Events', 5, -2.5 , 2.5),
    "histoNum" : r.TH1D(f"Shower_fprs_MB3_num", r';Wheel; Events', 5, -2.5 , 2.5),
    "func"     : lambda reader: [shower.wh for shower in fcns.get_shower_by_station(reader, station=3)],
    "numdef"   : lambda reader: [
      (shower.sc, shower.wh) in [(seg.sc, seg.wh) for seg in fcns.get_best_matches(reader, station = 3, _4showereds=False)] 
      for shower in fcns.get_shower_by_station(reader, station=3)
    ],
  },
  "shower_fprs_MB4":{
    "type": "eff",
    "histoDen" : r.TH1D(f"Shower_fprs_MB4_total", r';Wheel; Events', 5, -2.5 , 2.5),
    "histoNum" : r.TH1D(f"Shower_fprs_MB4_num", r';Wheel; Events', 5, -2.5 , 2.5),
    "func"     : lambda reader: [shower.wh for shower in fcns.get_shower_by_station(reader, station=4)],
    "numdef"   : lambda reader: [
      (shower.sc, shower.wh) in [(seg.sc, seg.wh) for seg in fcns.get_best_matches(reader, station = 4, _4showereds=False)] 
      for shower in fcns.get_shower_by_station(reader, station=4)
    ],
  },

  "seg_m_shower_tprgm_MB1":{ # true positive ratio --> segments which loc matches with any shower / segments (relative to showered genmuons)
      "type": "eff",
      "histoDen" : r.TH1D(f"Seg_m_shower_tprgm_MB1_total", r';Wheel; Events', 5, -2.5 , 2.5),
      "histoNum" : r.TH1D(f"Seg_m_shower_tprgm_MB1_num", r';Wheel; Events', 5, -2.5 , 2.5),
      "func"     : lambda reader: [seg.wh for seg in fcns.get_best_matches( reader, station = 1, _4showereds = True )],
      "numdef"   : lambda reader: [
          ((seg.sc, seg.wh) in fcns.get_shower_locs( reader, station = 1))
          for seg in fcns.get_best_matches( reader, station = 1, _4showereds = True )
        ],
  },
  "seg_m_shower_tprgm_MB2":{
      "type": "eff",
      "histoDen" : r.TH1D(f"Seg_m_shower_tprgm_MB2_total", r';Wheel; Events', 5, -2.5 , 2.5),
      "histoNum" : r.TH1D(f"Seg_m_shower_tprgm_MB2_num", r';Wheel; Events', 5, -2.5 , 2.5),
      "func"     : lambda reader: [seg.wh for seg in fcns.get_best_matches( reader, station = 2, _4showereds = True )],
      "numdef"   : lambda reader: [
          ((seg.sc, seg.wh) in fcns.get_shower_locs( reader, station = 2))
          for seg in fcns.get_best_matches( reader, station = 2, _4showereds = True )
        ],
  },
  "seg_m_shower_tprgm_MB3":{
      "type": "eff",
      "histoDen" : r.TH1D(f"Seg_m_shower_tprgm_MB3_total", r';Wheel; Events', 5, -2.5 , 2.5),
      "histoNum" : r.TH1D(f"Seg_m_shower_tprgm_MB3_num", r';Wheel; Events', 5, -2.5 , 2.5),
      "func"     : lambda reader: [seg.wh for seg in fcns.get_best_matches( reader, station = 3, _4showereds = True )],
      "numdef"   : lambda reader: [
          ((seg.sc, seg.wh) in fcns.get_shower_locs( reader, station = 3))
          for seg in fcns.get_best_matches( reader, station = 3, _4showereds = True )
        ],
  },
  "seg_m_shower_tprgm_MB4":{
      "type": "eff",
      "histoDen" : r.TH1D(f"Seg_m_shower_tprgm_MB4_total", r';Wheel; Events', 5, -2.5 , 2.5),
      "histoNum" : r.TH1D(f"Seg_m_shower_tprgm_MB4_num", r';Wheel; Events', 5, -2.5 , 2.5),
      "func"     : lambda reader: [seg.wh for seg in fcns.get_best_matches( reader, station = 4, _4showereds = True )],
      "numdef"   : lambda reader: [
          ((seg.sc, seg.wh) in fcns.get_shower_locs( reader, station = 4))
          for seg in fcns.get_best_matches( reader, station = 4, _4showereds = True )
        ],
  },

  "seg_m_shower_fprgm_MB1":{ # fake positive ratio --> segments which loc matches with any shower / segments (relative to non showered genmuons)
      "type": "eff",
      "histoDen" : r.TH1D(f"Seg_m_shower_fprgm_MB1_total", r';Wheel; Events', 5, -2.5 , 2.5),
      "histoNum" : r.TH1D(f"Seg_m_shower_fprgm_MB1_num", r';Wheel; Events', 5, -2.5 , 2.5),
      "func"     : lambda reader: [seg.wh for seg in fcns.get_best_matches( reader, station = 1, _4showereds = False)],
      "numdef"   : lambda reader: [
          ((seg.sc, seg.wh) in fcns.get_shower_locs( reader, station = 1))
          for seg in fcns.get_best_matches( reader, station = 1, _4showereds = False)
        ],
  },
  "seg_m_shower_fprgm_MB2":{
      "type": "eff",
      "histoDen" : r.TH1D(f"Seg_m_shower_fprgm_MB2_total", r';Wheel; Events', 5, -2.5 , 2.5),
      "histoNum" : r.TH1D(f"Seg_m_shower_fprgm_MB2_num", r';Wheel; Events', 5, -2.5 , 2.5),
      "func"     : lambda reader: [seg.wh for seg in fcns.get_best_matches( reader, station = 2, _4showereds = False )],
      "numdef"   : lambda reader: [
          ((seg.sc, seg.wh) in fcns.get_shower_locs( reader, station = 2))
          for seg in fcns.get_best_matches( reader, station = 2, _4showereds = False)
        ],
  },
  "seg_m_shower_fprgm_MB3":{
      "type": "eff",
      "histoDen" : r.TH1D(f"Seg_m_shower_fprgm_MB3_total", r';Wheel; Events', 5, -2.5 , 2.5),
      "histoNum" : r.TH1D(f"Seg_m_shower_fprgm_MB3_num", r';Wheel; Events', 5, -2.5 , 2.5),
      "func"     : lambda reader: [seg.wh for seg in fcns.get_best_matches( reader, station = 3, _4showereds = False )],
      "numdef"   : lambda reader: [
          ((seg.sc, seg.wh) in fcns.get_shower_locs( reader, station = 3))
          for seg in fcns.get_best_matches( reader, station = 3, _4showereds = False )
        ],
  },
  "seg_m_shower_fprgm_MB4":{
      "type": "eff",
      "histoDen" : r.TH1D(f"Seg_m_shower_fprgm_MB4_total", r';Wheel; Events', 5, -2.5 , 2.5),
      "histoNum" : r.TH1D(f"Seg_m_shower_fprgm_MB4_num", r';Wheel; Events', 5, -2.5 , 2.5),
      "func"     : lambda reader: [seg.wh for seg in fcns.get_best_matches( reader, station = 4, _4showereds = False)],
      "numdef"   : lambda reader: [
          ((seg.sc, seg.wh) in fcns.get_shower_locs( reader, station = 4))
          for seg in fcns.get_best_matches( reader, station = 4, _4showereds = False )
        ],
  },
})
