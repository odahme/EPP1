from ROOT import TLorentzVector,TRandom3,TH1F,TH2D,TCanvas,TApplication
from math import acos,pi
from ThreeBodyDecay import *



(part1,part2,part3) = exp4()


# fourVector = TLorentzVector()
# fourVector.SetPtEtaPhiM(10,0.52,0,1.)
# fourVector.SetPtEtaPhiE(10,0.52,0,5.)
# fourVector.SetPxPyPzE(2.3,0.,1.,5.)
# print fourVector.Pt(),fourVector.Px()
# print fourVector.E(),fourVector.M()
# fourVector2 = TLorentzVector()
vectorsum = part1+part2+part3
print part1.M()
print part2.M()
print part3.M()
# px = part1.Px() + part2.Px() + part3.Px()
# py = part1.Py() + part2.Py() + part3.Py()
# pz = part1.Pz() + part2.Pz() + part3.Pz()
# print (px**2+py**2+pz**2)**(1./2)
# print vectorsum.P()

dalitz = TH2D("dalitz","Dalitz-Plot Hist Example",100,0.5,2,100,0.5,2)
c1 = TCanvas("c1","c1",1920,1080)
c2 = TCanvas("c2","c2",1920,1080)
invmass = TH1F("invmass","invariant mass",100,0,3)


for i in range(100000):
    (part1,part2,part3) = exp4()
    mainsum = part1+part2+part3
    if ((mainsum.M()>1.9) and (mainsum.M()<2.2)):
        vectorsum1 = part1+part3
        vectorsum2 = part2+part3
        vectorsum3 = part1+part2
        m13 = vectorsum1.M()
        m23 = vectorsum2.M()
        m12 = vectorsum3.M()

        if ( (m12 < 1.4 or m12 > 1.6) and (m23 < 1.2 or m23 > 1.4) and (m23 < 0.8 or m23 > 1.0)):
            invmass.Fill(m13)
            dalitz.Fill(m13,m23)
            dalitz.Fill(m23,m13)



c1.cd()
dalitz.Draw()

c2.cd()
invmass.Draw()



################################
