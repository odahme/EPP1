from MyAnalysis import MyAnalysis
from ROOT import TTree, TFile , TF1, TGraph2D, TMath, gROOT , TCanvas
from Plotter import plotVar, plotVarNorm, plotShapes, getBkgHisto, getSigHisto, getDataHisto
from Plotter import logLikelihood, moveHisto , least_square
import array
import numpy as np
import matplotlib.pyplot as plt
from pylab import sqrt

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
#


samples = ["qcd", "zz", "wz", "ww",  "single_top", "dy","wjets", "ttbar"]
#samples = ["ttbar"  ]

#vars = ["NIsoMu", "Muon_Pt","Inv_Mass_Z","Inv_Mass_W_l","tot_inv_mass"]
#vars = ["t_lep_m","t_hadron_mass"]
vars = ["t_hadron_mass","t_lep_m"]#,"MET_z1","MET_z2"]






for v in vars:
    print "Variable: ", v
    ### plotShapes (variable, samples,logScale )
    plotShapes(v, samples,  False)
    ### plotVar(variable, samples,isData, logScale )
    plotVar(v, samples,  True , False)



sig_var = "ttbar"
varias = ["t_hadron_mass","t_lep_m"]

t_mass_in_MC = 172.44

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
crosS = nAccData/(trigEff * lum * acRate)
nAccData_err = sqrt(nAccData)
crosS_err = sqrt( (nAccData_err * (trigEff * lum * acRate))**2 + ( trigEff_err * nAccData/(trigEff**2 * lum * acRate))**2 + (lum_err * nAccData/(trigEff * lum**2 * acRate))**2 + (acRate_err * nAccData/(trigEff * lum * acRate**2))**2 )
print "cross section tt = ",crosS," +- ",crosS_err
print "theory = 167 +17 -18"

for var in varias:
    print
    print "======================="
    print "Doing calculation with variable ", var

    bkg  = getBkgHisto(var, samples, signal=sig_var)
    sig  = getSigHisto(var, signal=sig_var)
    data = getDataHisto(var)


    nbin = data.GetXaxis().GetNbins()
    maximum = data.GetXaxis().GetXmax()
    minimum = data.GetXaxis().GetXmin()
    length = (maximum - minimum)/nbin
    medium = (maximum + minimum)/2
    x = []
    y = []
    z = []



    print " Starting fit"
    m = 0
    mu = 1


    ls_min = 0
    ls_mu  = 0
    ls_m   = 0
    first = True

#    fvec = range(-nbin , nbin)
    fvec = range(-10 ,10)
    #print fvec
    ivec = np.linspace(0, 1.5 , 100)
    #For loading bar
    counter =0
    max_iter = len(fvec) * len(ivec)
    #fvec = np.linspace(-40 , 20 , 100)
    for i in ivec:
        mu = i

        for f in fvec:
            if( counter%1000==0):
                print counter," / ", max_iter
            m = f
            signalMoved = moveHisto(sig, m)
            signalMoved.Scale(mu)
            sb = signalMoved.Clone("sb")
            sb.Add(bkg)
    #        lr = least_square(data,sb)
            lr = logLikelihood(data, sb)
            counter+=1

            if(first):
                ls_min= lr+1
                first = False

    #        lr = logLikelihood(data, sb)

            x.append(t_mass_in_MC+m*length)
    #        x.append(f)
            y.append(mu)
    #        y.append(i)
            z.append(lr)
    #        print "m", m, "mu", mu, "lr", lr
            if(lr< ls_min):
                ls_min = lr
                ls_mu  = mu
                ls_m   = t_mass_in_MC+m*length

    print var,": -loglikelihood = ", ls_min, "  at mass: " , ls_m , " with scaling: " , ls_mu



    minimum2 = min(z)
    ndof = 2

    #    z[i] = 1-TMath.Prob(z[i],ndof)


    arrX = array.array('f', x)
    arrY = array.array('f', y)
    arrZ = array.array('f', z)
    gr = TGraph2D( len(x) , arrX, arrY, arrZ )
    c1 = TCanvas()
    print "Drawing contur-plot"
    gr.Draw("CONT1,Z")
    c1.Print("contur_"+var+".pdf")

    x=[]
    z=[]

    for f in fvec:
        m = f
        signalMoved = moveHisto(sig, m)
        signalMoved.Scale(ls_mu)
        sb = signalMoved.Clone("sb")
        sb.Add(bkg)
    #        lr = least_square(data,sb)
        lr = logLikelihood(data, sb)
        counter+=1
        x.append(t_mass_in_MC+m*length)
        z.append(lr)


    minimum2 = min(z)
    print "len(z): " , len(z)
    for i in range (len(z)):
    #    if(i%100==0):
    #        print i ," / ", len(z)
        z[i] = z[i] - minimum2
        if( (z[i] > 1 and z[i-1]<1) or (z[i] < 1 and z[i-1] > 1)):
            print "index ",i," mass " ,x[i], " loglikelihood ", z[i]

    plt.figure()
    plt.plot(x,z)
    plt.grid()
    plt.savefig("loglikelihood"+var+ ".pdf")



    #m = axis.getXmin()
