from MyAnalysis import MyAnalysis
from ROOT import TTree, TFile, TCanvas, gROOT
from Plotter import plotVar, plotVarNorm, plotShapes, getBkgHisto, getSigHisto, getDataHisto

gROOT.SetBatch(0)
#c1 = TCanvas("c1","c1",800,600)
#c2 = TCanvas("c2","c2",800,600)
#c3 = TCanvas("c3","c3",800,600)

### Instantiation of an object of kind MyAnalysis for each single sample
TT = MyAnalysis("ttbar")
TT.processEvents()

#DY = MyAnalysis("dy")
#DY.processEvents()
#
#QCD = MyAnalysis("qcd")
#QCD.processEvents()
#
#SingleTop = MyAnalysis("single_top")
#SingleTop.processEvents()
#
#WJets = MyAnalysis("wjets")
#WJets.processEvents()
#
#WW = MyAnalysis("ww")
#WW.processEvents()
#
#ZZ = MyAnalysis("zz")
#ZZ.processEvents()
#
#WZ = MyAnalysis("wz")
#WZ.processEvents()
#
#Data = MyAnalysis("data")
#Data.processEvents()



samples = ["qcd", "zz", "wz", "ww",  "single_top", "dy","wjets", "ttbar"]

vars = ["NIsoMu","Muon_Pt","inv_m"]

for v in vars:
    print "Variable: ", v
    ### plotVar(variable, samples,isData, logScale )
    plotVar(v, samples,  True, True)


var = "inv_m"
bkg = getBkgHisto(var, samples, signal="dy")
sig = getSigHisto(var, signal="dy")
data = getDataHisto(var)


#signalMoved = moveHisto(sig,m)

#c1.cd()
#bkg.Draw("hist")
#c2.cd()
#sig.Draw("hist")
#c3.cd()
#data.Draw("hist")