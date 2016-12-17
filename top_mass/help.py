from Plotter import plotVar, plotVarNorm, plotShapes, getBkgHisto, getSigHisto, getDataHisto, logLikelihood, moveHisto

signalMoved = moveHisto(sig,m)
signalMoved.Scale(mu)
sb = signalMoved.Clone("sb")
sb.Add(bkg)

lr = logLikelihood(data , sb)

import array
arrX, arrY, arrZ = array.array('f',x),array.array('f',y),array.array('f',z)
gr = TGraph2D( len(x) , arrX, arrY, arrZ )
print gr.GetMinimum()
gr.Draw("CONT1,Z")


