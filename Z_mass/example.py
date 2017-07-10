from MyAnalysis import MyAnalysis
from ROOT import TTree, TFile, TGraph2D, TMath, gROOT, TF1, TCanvas, TGraph
from Plotter import plotVar, plotVarNorm, plotShapes, getBkgHisto, getSigHisto, getDataHisto,logLikelihood, moveHisto
import array

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

# Breit-Wigner function
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
data.Fit("mybw")
data.Draw()
canvas.Update()
canvas.SaveAs("Z_mass_fit.pdf")


# First part of Long Exercise

m = 0
mu = 1
nbin = data.GetXaxis().GetNbins()
maximum = data.GetXaxis().GetXmax()
minimum = data.GetXaxis().GetXmin()
length = (maximum - minimum)/nbin
x = []
y = []
z = []
for i in range (5, 15):
    mu = i/10.
    for f in range (-2, 3):
        m = f
        signalMoved = moveHisto(sig, m)
        signalMoved.Scale(mu)
        sb = signalMoved.Clone("sb")
        sb.Add(bkg)
        lr = logLikelihood(data, sb)
        ndof = 2
        x.append(91.188+m*length)
        y.append(mu)
        z.append(lr)
        #print "m", m, "mu", mu, "lr", lr

minimum2 = min(z)
for i in range (len(z)):
    z[i] = z[i] - minimum2
    z[i]= 1-TMath.Prob(z[i],ndof)

arrX, arrY, arrZ = array.array('f', x), array.array('f', y), array.array('f', z)
gr = TGraph2D( len(x) , arrX, arrY, arrZ )
#gr = TGraph2D( 10 , arrX, arrY )
print gr.GetMinimum()
canvas.cd()
gr.Draw("CONT1,Z")
canvas.Update()
canvas.SaveAs("contur_plot.pdf")

#signalMoved = moveHisto(sig,m)

#c1.cd()
#bkg.Draw("hist")
#c2.cd()
#sig.Draw("hist")
#c3.cd()
#data.Draw("hist")
