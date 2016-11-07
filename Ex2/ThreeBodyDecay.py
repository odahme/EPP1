from ROOT import TLorentzVector,TRandom3,TH1F,TH2F,TCanvas
from math import acos,pi

rnd = TRandom3()

def decayRestFrame(M,m1,m2):
    p = ((M**2-(m1+m2)**2)*(M**2-(m1-m2)**2))**0.5/(2*M)
    theta = acos(rnd.Rndm()*2-1)
    phi = rnd.Rndm()*2*pi

    part1 = TLorentzVector()
    part1.SetPxPyPzE(p,0,0,(p**2+m1**2)**0.5)
    part1.SetTheta(theta)
    part1.SetPhi(phi)

    part2 = TLorentzVector()
    part2.SetPxPyPzE(p,0,0,(p**2+m2**2)**0.5)
    part2.SetTheta(pi+theta)
    part2.SetPhi(pi+phi)

    return part1,part2

def decay(part,m1,m2):
    M = part.M()
    momentum = part.M()
    boost = part.BoostVector()
    part1,part2 = decayRestFrame(M,m1,m2)
    part1.Boost(boost)
    part2.Boost(boost)

    return part1,part2
   

angRes = 0.01 # rad
pRes   = 0.05  # fraction

def reco(part):
    part.SetTheta(part.Theta()*(1+angRes*rnd.Gaus()))
    part.SetPhi(part.Phi()*(1+angRes*rnd.Gaus()))    
    part.SetVectM( part.Vect()*( 1.+pRes*rnd.Gaus() ) , part.M())
    return part

def generateEvent(M, m1, m2, m3, pZ=10, mA=None, smear=True, bkg=0):
    if rnd.Rndm()<bkg:
        mA = None
        sideband = 0.4
        slope = M
        Mmin = M*(1-sideband)
        Mmax = M*(1+sideband)
        M =1e30
        while M>Mmax:
            M = Mmin+(rnd.Exp(slope))
    P = TLorentzVector()
    P.SetPxPyPzE(0,0,pZ,(pZ**2+M**2)**0.5)
    if mA is None:
        mA = rnd.Rndm()*(M-m2-m3-m1)+m2+m3
    part1,partA = decay(P,m1,mA)
    part2,part3 = decay(partA,m2,m3)
    
    if m1==m2 and rnd.Rndm()>0.5:
        tmp = part2
        part2 = part1
        part1 = tmp
    if m1==m3 and rnd.Rndm()>0.5:
        tmp = part3
        part3 = part1
        part1 = tmp
    if m1==m3 and rnd.Rndm()>0.5:
        tmp = part3
        part3 = part2
        part2 = tmp

    if smear:
        part1 = reco(part1)
        part2 = reco(part2)
        part3 = reco(part3)

    
    return sorted([part1,part2,part3],key=lambda part: -part.M())


##### Generate Ds -> K+ K- pi+

#no resonance
def generateDsKKpi_noRes(smear,bkg):
    return generateEvent(
        M=1.968,    #D0s
        m1 = 0.493001, #K-    
        m2 = 0.493, #K+
        m3 = 0.140, #pi+
        pZ = 10,
        bkg = bkg,
        smear = smear
    )

#phi(1020) -> KK resonance
def generateDsKKpi_phi(smear,bkg):
    return generateEvent(
        M=1.968,    #D0s
        m1 = 0.140, #pi+
        mA = 1.020,
        m2 = 0.493001, #K-    
        m3 = 0.493, #K+
        pZ = 10,
        bkg = bkg,
        smear = smear
    )

#K*(892) -> Kpi resonance
def generateDsKKpi_Kstar(smear,bkg):
    return generateEvent(
        M=1.968,    #D0s
        m1 = 0.493, #K+
        mA = 0.892,
        m2 = 0.493001, #K-    
        m3 = 0.140, #pi+
        pZ = 10,
        bkg = bkg,
        smear = smear
    )

#mix of the three channels

def generateDsKKpi(smear,bkg):
    if rnd.Rndm()>0.66:
        return generateDsKKpi_Kstar(smear,bkg)
    elif rnd.Rndm()>0.33:
        return generateDsKKpi_phi(smear,bkg)
    else:
        return generateDsKKpi_noRes(smear,bkg)

##### Generate ppbar -> pi0 eta eta
def generatePP2etapi0_noRes(smear,bkg):
    return generateEvent(
        M=2.050,
        m1 = 0.135, #pi0
        m2 = 0.547, #eta    
        m3 = 0.547, #eta
        pZ = 0.9,
        bkg = bkg,
        smear = smear
    )

#f(1500) -> eta eta
def generatePP2etapi0_f(smear,bkg):
    return generateEvent(
        M=2.050,
        m1 = 0.135, #pi0
        mA = 1.500,
        m2 = 0.547, #eta    
        m3 = 0.547, #eta
        pZ = 0.9,
        bkg = bkg,
        smear = smear
    )

#a2(1320) -> pi0 eta
def generatePP2etapi0_a2(smear,bkg):
    return generateEvent(
        M=2.050,
        m1 = 0.547, #eta    
        mA = 1.320,
        m2 = 0.135, #pi0
        m3 = 0.547, #eta
        pZ = 0.9,
        bkg = bkg,
        smear = smear
    )

#a0(980) -> pi0 eta
def generatePP2etapi0_a0(smear,bkg):
    return generateEvent(
        M=2.050,
        m1 = 0.547, #eta    
        mA = 0.980,
        m2 = 0.135, #pi0
        m3 = 0.547, #eta
        pZ = 0.9,
        bkg = bkg,
        smear = smear
    )

#mix of the three channels

def generatePP2etapi0(smear,bkg):
    if rnd.Rndm()>0.85:
        return generatePP2etapi0_noRes(smear,bkg)
    elif rnd.Rndm()>0.60:
        return generatePP2etapi0_f(smear,bkg)
    elif rnd.Rndm()>0.35:
        return generatePP2etapi0_a2(smear,bkg)
    else:
        return generatePP2etapi0_a0(smear,bkg)


################################

def exp1():
    smear = False
    bkg = 0
    return generateDsKKpi(smear,bkg)

def exp2():
    smear = True
    bkg = 0
    return generateDsKKpi(smear,bkg)

def exp3():
    smear = True
    bkg = 0.7
    return generateDsKKpi(smear,bkg)

def exp4():
    pRes=0.05
    smear = True
    bkg = 0.5
    return generatePP2etapi0(smear,bkg)


def exp5():
    smear = True
    bkg = 0.5
    pi0s = generatePP2etapi0(smear,bkg)
    photons = []
    for pi0 in pi0s:
        photon1, photon2 = decay(pi0,0,0)
        photons.append(reco(photon1))
        photons.append(reco(photon2))
    return sorted(photons,key=lambda part: -part.M())


################################

