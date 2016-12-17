from MyAnalysis import MyAnalysis
from ROOT import TTree, TFile, TF1, TF2, TCanvas
from Plotter import plotVar, plotVarNorm, plotShapes, getHisto
from pylab import sqrt
from math import pi

nTriggerd = 0.
nTotal = 0.
nAccTT = 0.
nTT = 0.

### Instantiation of an object of kind MyAnalysis for each single sample
TT = MyAnalysis("ttbar")
TT.processEvents()
nTriggerd += TT.nTrig
nTotal += TT.nEvents
nAccTT = TT.nAcc
nTT = TT.nEvents

DY = MyAnalysis("dy")
DY.processEvents()
nTriggerd += DY.nTrig
nTotal += DY.nEvents

QCD = MyAnalysis("qcd")
QCD.processEvents()
nTriggerd += QCD.nTrig
nTotal += QCD.nEvents

SingleTop = MyAnalysis("single_top")
SingleTop.processEvents()
nTriggerd += SingleTop.nTrig
nTotal += SingleTop.nEvents

WJets = MyAnalysis("wjets")
WJets.processEvents()
nTriggerd += WJets.nTrig
nTotal += WJets.nEvents

WW = MyAnalysis("ww")
WW.processEvents()
nTriggerd += WW.nTrig
nTotal += WW.nEvents

ZZ = MyAnalysis("zz")
ZZ.processEvents()
nTriggerd += ZZ.nTrig
nTotal += ZZ.nEvents

WZ = MyAnalysis("wz")
WZ.processEvents()
nTriggerd += WZ.nTrig
nTotal += WZ.nEvents
##
Data = MyAnalysis("data")
Data.processEvents()
nAccData = Data.nAcc


samples = ["qcd", "zz", "wz", "ww",  "single_top", "dy","wjets", "ttbar"]

#samples = ["ttbar"]

vars = ["NJet","NIsoMu","NBtag","inv_m"]

print "number of selected events in MC = ",nAccTT
print "number of selected events in Data = ",nAccData

for v in vars:
    print "Variable: ", v
    ### plotShapes (variable, samples,logScale )
    plotShapes(v, samples,  False)
    ### plotVar(variable, samples,isData, logScale )
    plotVar(v, samples,  True, False)
    
#Breit-Wigner function
def mybw(x,par):
  arg1 = 14.0/22.0; # 2 over pi
  arg2 = par[1]*par[1]*par[2]*par[2] #Gamma=par[1]  M=par[2]
  arg3 = ((x[0]*x[0]) - (par[2]*par[2]))*((x[0]*x[0]) - (par[2]*par[2]))
  arg4 = x[0]*x[0]*x[0]*x[0]*((par[1]*par[1])/(par[2]*par[2]))
  return par[0]*arg1*arg2/(arg3 + arg4)


func = TF1("mybw",mybw,0, 2000,3)
func.SetParameter(0,1.0)   
func.SetParName(0,"const")
func.SetParameter(2,5.0)    
func.SetParName(1,"sigma")
func.SetParameter(1,95.0)    
func.SetParName(2,"mean")    

canvas = TCanvas("canvas","canvas",800,600)
histo_m = getHisto("inv_m","ttbar")
histo_m.Fit("mybw")
histo_m.Draw()
canvas.Update()
canvas.SaveAs("top_mass_fit.pdf")



### get trigger efficiency
nTriggerd_err = sqrt(nTriggerd)
nTotal_err = sqrt(nTotal)
trigEff = 1.0* nTriggerd/nTotal
trigEff_err = 0.1*trigEff + sqrt( (nTriggerd_err * 1/nTotal)**2 + (nTotal_err * nTriggerd/(nTotal)**2)**2 )
print "Trigger eff = ", 1.0 * nTriggerd/nTotal," +- ",trigEff_err

### get acceptance
nAccTT_err = sqrt(nAccTT)
nTT_err = sqrt(nTT)
acRate = 1.0 * nAccTT/nTT
acRate_err = sqrt( (nAccTT_err * 1/nTT)**2 + (nTT_err * nAccTT/(nTT)**2)**2 )
print "accpetance = ",1.0 * nAccTT/nTT," +- ",acRate_err

##cross section tt
lum = 50.
lum_err = 0.1*50
#crosS = nAccData/(trigEff * lum * acRate)
#nAccData_err = sqrt(nAccData)
#crosS_err = sqrt( (nAccData_err * (trigEff * lum * acRate))**2 + ( trigEff_err * nAccData/(trigEff**2 * lum * acRate))**2 + (lum_err * nAccData/(trigEff * lum**2 * acRate))**2 + (acRate_err * nAccData/(trigEff * lum * acRate**2))**2 )
#print "cross section tt = ",crosS," +- ",crosS_err
print "theory = 167 +17 -18"

    

