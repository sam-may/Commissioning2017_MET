import sys, os
import time
import itertools
import numpy
import glob

os.system("/home/users/smay/Utilities/ShellFunctions.sh")
os.system("cd histograms")

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("eras", help = "Which 2017 data eras to consider (B,C,D,E,F)", type=str)
args = parser.parse_args()
eras = args.eras.split(",")

data = {"B" : ["DoubleEG_Run2017B-17Nov2017-v1_MINIAOD_CMS4_V00-00-06_allPfCands__MET_v1/", "DoubleMuon_Run2017B-17Nov2017-v1_MINIAOD_CMS4_V00-00-06_allPfCands__MET_v1/"],  
        "C" : ["DoubleEG_Run2017C-17Nov2017-v1_MINIAOD_CMS4_V00-00-06_allPfCands__MET_v1/", "DoubleMuon_Run2017C-17Nov2017-v1_MINIAOD_CMS4_V00-00-06_allPfCands__MET_v1/"],
        "D" : ["DoubleEG_Run2017D-17Nov2017-v1_MINIAOD_CMS4_V00-00-06_allPfCands__MET_v1/", "DoubleMuon_Run2017D-17Nov2017-v1_MINIAOD_CMS4_V00-00-06_allPfCands__MET_v1/"],
	"E" : ["DoubleEG_Run2017E-17Nov2017-v1_MINIAOD_CMS4_V00-00-06_allPfCands__MET_v1/", "DoubleMuon_Run2017E-17Nov2017-v1_MINIAOD_CMS4_V00-00-06_allPfCands__MET_v1/"],
	"F" : ["DoubleEG_Run2017F-17Nov2017-v1_MINIAOD_CMS4_V00-00-06_allPfCands__MET_v1/", "DoubleMuon_Run2017F-17Nov2017-v1_MINIAOD_CMS4_V00-00-06_allPfCands__MET_v1/"]}


mc = {	"Drell-Yan" : ["DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8_RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1_MINIAODSIM_CMS4_V00-00-06_allPfCands__MET_v1/", "DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8_RunIIFall17MiniAOD-94X_mc2017_realistic_v10_ext1-v1_MINIAODSIM_CMS4_V00-00-06_allPfCands__MET_v1/"] ,
	"DiBoson" : ["WW_TuneCP5_13TeV-pythia8_RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1_MINIAODSIM_CMS4_V00-00-06_allPfCands__MET_v1/", "WZ_TuneCP5_13TeV-pythia8_RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1_MINIAODSIM_CMS4_V00-00-06_allPfCands__MET_v1/", "ZZ_TuneCP5_13TeV-pythia8_RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1_MINIAODSIM_CMS4_V00-00-06_allPfCands__MET_v1/"],
	"TriBoson" : ["WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8_RunIIFall17MiniAOD-94X_mc2017_realistic_v11-v1_MINIAODSIM_CMS4_V00-00-06_allPfCands__MET_v1/", "WZZ_TuneCP5_13TeV-amcatnlo-pythia8_RunIIFall17MiniAOD-94X_mc2017_realistic_v11-v1_MINIAODSIM_CMS4_V00-00-06_allPfCands__MET_v1/", "WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8_RunIIFall17MiniAOD-94X_mc2017_realistic_v11-v1_MINIAODSIM_CMS4_V00-00-06_allPfCands__MET_v1/", "ZZZ_TuneCP5_13TeV-amcatnlo-pythia8_RunIIFall17MiniAOD-94X_mc2017_realistic_v11-v1_MINIAODSIM_CMS4_V00-00-06_allPfCands__MET_v1/"],
	"Top" : ["ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8_RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1_MINIAODSIM_CMS4_V00-00-06_allPfCands__MET_v1/", "ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8_RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1_MINIAODSIM_CMS4_V00-00-06_allPfCands__MET_v1/", "ST_t-channel_antitop_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8_RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1_MINIAODSIM_CMS4_V00-00-06_allPfCands__MET_v1/", "ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8_RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1_MINIAODSIM_CMS4_V00-00-06_allPfCands__MET_v1/", "ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8_RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1_MINIAODSIM_CMS4_V00-00-06_allPfCands__MET_v1/", "TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8_RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1_MINIAODSIM_CMS4_V00-00-06_allPfCands__MET_v1/"]
}

nPar = 10
basepath = "/hadoop/cms/store/user/smay/ProjectMetis/MET/"
intermediate_files = ""
for era in eras:
  for set in data[era]:
    files = glob.glob(basepath+set+"*.root")
    intermediate_file = "intermediate_" + set
    intermediate_files += intermediate_file + ".root "
    os.system("addHistos %s %s %d %d" % (intermediate_file, basepath+set+"/Zll_histograms", len(files), nPar))

os.system("hadd Zll_histograms_%s %s" % (args.eras + ".root", intermediate_files))

process_files = ""
for key, sets in mc.iteritems():
  intermediate_files = ""
  for set in sets:
    files = glob.glob(basepath+set+"*.root")
    intermediate_file = "intermediate_" + set + "_" + args.eras 
    intermediate_files += intermediate_file + ".root"
    os.system("addHistos %s %s %d %d" % (intermediate_file, basepath+set+"/Zll_histograms", len(files), nPar))
  process_file = "Zll_histograms_%s_%s.root" % (key, args.eras)
  process_files += process_file + " "
  os.system("hadd %s %s" % (process_file, intermediate_files))

os.system("hadd Zll_histograms_MC_%s.root %s" % (args.eras, process_files))