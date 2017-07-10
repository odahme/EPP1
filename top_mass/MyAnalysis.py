import ROOT
import copy
from Samples import samp
import numpy as np

class MyAnalysis(object):

    def __init__(self, sample):

        """ The Init() function is called when an object MyAnalysis is initialised
        The tree corresponding to the specific sample is picked up
        and histograms are booked.
        """

        self._tree = ROOT.TTree()
        if(sample not in samp.keys() and sample != "data"):
            print RuntimeError("Sample %s not valid. please, choose among these: %s" % (sample, str(samp.keys())) )
            exit
        self.histograms = {}
        self.sample = sample
        self._file = ROOT.TFile("files/"+sample+".root")
        self._file.cd()
        tree = self._file.Get("events")
        self._tree = tree
        self.nEvents = self._tree.GetEntries()
        print "Number of entries for " + self.sample + ":\t" + str(self.nEvents)
        self.nTrig = 0
        self.nAcc = 0

        ### Book histograms
        self.bookHistos()

    def getTree(self):
        return self._tree

    def getHistos(self):
        return self.histograms

    def bookHistos(self):
        h_nJet = ROOT.TH1F("NJet","#of jets", 6, -0.5, 6.5)
        h_nJet.SetXTitle("%# of jets")
        self.histograms["NJet"] = h_nJet

        h_nJetFinal = ROOT.TH1F("NJetFinal","#of jets", 6, -0.5, 6.5)
        h_nJetFinal.SetXTitle("%# of jets")
        self.histograms["NJetFinal"] = h_nJetFinal

        h_MuonIso = ROOT.TH1F("Muon_Iso","Muon Isolation", 25, 0., 3.)
        h_MuonIso.SetXTitle("Muon Isolation")
        self.histograms["Muon_Iso"] = h_MuonIso

        h_NIsoMu = ROOT.TH1F("NIsoMu","Number of isolated muons", 5, 0.5, 5.5)
        h_NIsoMu.SetXTitle("Number of isolated muons")
        self.histograms["NIsoMu"] = h_NIsoMu

        h_MuonPt = ROOT.TH1F("Muon_Pt","Muon P_T", 50, 0., 200.)
        h_MuonPt.SetXTitle("Muon P_T")
        self.histograms["Muon_Pt"] = h_MuonPt

        h_METpt = ROOT.TH1F("MET_Pt","MET P_T", 25, 0., 300.)
        h_METpt.SetXTitle("MET P_T")
        self.histograms["MET_Pt"] = h_METpt

        h_JetPt = ROOT.TH1F("Jet_Pt","Jet P_T", 50, 0., 200.)
        h_JetPt.SetXTitle("Jet P_T")
        self.histograms["Jet_Pt"] = h_JetPt

        h_JetBtag = ROOT.TH1F("Jet_Btag","Jet B tag", 10, 1., 6.)
        h_JetBtag.SetXTitle("Jet B tag")
        self.histograms["Jet_btag"] = h_JetBtag

        h_NBtag = ROOT.TH1F("NBtag","Jet B tag", 4, 0.5, 4.5)
        h_NBtag.SetXTitle("Number of B tagged jets")
        self.histograms["NBtag"] = h_NBtag


        h_Inv_Mass_Z = ROOT.TH1F("Inv_Mass_Z","Inv Mass", 240, 60., 120.)
        h_Inv_Mass_Z.SetXTitle("Invariant masss of supposed Z-boson")
        self.histograms["Inv_Mass_Z"] = h_Inv_Mass_Z

        h_Inv_W_l = ROOT.TH1F("Inv_Mass_W_l","Inv Mass W l", 240, 0., 200.)
        h_Inv_W_l.SetXTitle("Invariant masss of leptonic W-boson")
        self.histograms["Inv_Mass_W_l"] = h_Inv_W_l


        h_t_lep = ROOT.TH1F("t_lep_m","Inv Mass t l", 50, 0., 600.)
        h_t_lep.SetXTitle("Invariant masss of leptonic t")
        self.histograms["t_lep_m"] = h_t_lep

        h_tot_inv_had = ROOT.TH1F("t_hadron_mass","t_hadron_mass", 50, 0., 600.)
        h_tot_inv_had.SetXTitle("t_hadron_mass")
        self.histograms["t_hadron_mass"] = h_tot_inv_had


        h_MET_z1= ROOT.TH1F("MET_z1","MET_z1", 100, -1000., 1000.)
        h_MET_z1.SetXTitle("MET_z1")
        self.histograms["MET_z1"] = h_MET_z1

        h_MET_z2= ROOT.TH1F("MET_z2","MET_z2", 100, -1000., 1000.)
        h_MET_z2.SetXTitle("MET_z2")
        self.histograms["MET_z2"] = h_MET_z2


    def saveHistos(self):
        outfilename = self.sample + "_histos.root"
        outfile = ROOT.TFile(outfilename, "RECREATE")
        outfile.cd()
        for h in self.histograms.values():
            h.Write()
        outfile.Close()






    def cut_check(self, tree):
        '''
        Apply the different cuts here
        Return: bool, True if event passes the checks

        '''

#        Check N_Jets ==4
 
        if( tree.NJet !=4):
            return False

#        Check leptons =1
        if( tree.NMuon!=1):
            return False


#        Check b_tags =2 (b_tag = sum of jets with btag>0)
        btags = 0
        for i in xrange(tree.NJet):
            if(tree.Jet_btag[i]>0):
                btags= btags +1

        if(btags !=2):
            return False

        return True


    def get_btag_indices(self , tree):
        '''
        Returns indizes of btagged , and not btagged Jets
        '''
        btagged = []

        not_btagged= []
        index =0
        for i in xrange(tree.NJet):
            index = i
            if(tree.Jet_btag[i]>0):
                btagged.append(index)
            else:
                not_btagged.append(index)

        return btagged , not_btagged

    def get_leptonic_nonleptonic_index(self, tree, btag, nbtagt):
        """
        Returns the index of the btagged Jet which belongs to the leptonic, then the index which belongs to the nonleptonic decay
        """
        light_hadrons = ROOT.TVector3(0,0,0)

        b_h1 = ROOT.TVector3(tree.Jet_Px[btag[0]],tree.Jet_Py[btag[0]],tree.Jet_Pz[btag[0]])
        b_h2 = ROOT.TVector3(tree.Jet_Px[btag[1]],tree.Jet_Py[btag[1]],tree.Jet_Pz[btag[1]])

        for m in nbtagt:
            light_hadrons = light_hadrons + ROOT.TVector3(tree.Jet_Px[m],tree.Jet_Py[m],tree.Jet_Pz[m])


        cos1 = b_h1*light_hadrons /np.sqrt((b_h1*b_h1)*(light_hadrons*light_hadrons))
        cos2 = b_h2*light_hadrons /np.sqrt((b_h2*b_h2)*(light_hadrons*light_hadrons))
        if( cos1> cos2 ):
            return btag[1] ,btag[0]
        else:
            return btag[0] ,btag[1]




    def hadronic_part(self , tree , nlep_ , nbtag):
        '''
        Hadronic part of the Decay

        Calculates the masss of the t-quark and fills the histogram
        '''
        All_4Vec    = ROOT.TLorentzVector(0,0,0,0)
        Sacrificial = ROOT.TLorentzVector(0,0,0,0)

        All_4Vec.SetXYZM(tree.Jet_Px[nlep_],tree.Jet_Py[nlep_],tree.Jet_Pz[nlep_],4.3)

        for i in nbtag:
            Sacrificial.SetXYZM(tree.Jet_Px[i],tree.Jet_Py[i],tree.Jet_Pz[i],0)
            All_4Vec= All_4Vec + Sacrificial
#        Get correct Jets check btag

#       Compare with light Jets, nearest b-tagt jet is the one you arre searching for

#calculate invariant mass
        w = tree.EventWeight
        self.histograms["t_hadron_mass"].Fill(All_4Vec.M() , w)





    def leptonic_part(self , tree, lep_ ):
        '''
        leptonic part of the Decay

        Calculates the masss of the t-quark and fills the histogram
        '''
        w = tree.EventWeight
        All_4Vec    = ROOT.TLorentzVector(0,0,0,0)
        Sacrificial = ROOT.TLorentzVector(0,0,0,0)

#calculate  correction for the missing energy

#===============================Probably Something wrong here===========================
        mw = 80.3
        X = mw**2/2 +  tree.Muon_Px[0]*tree.MET_px + tree.Muon_Py[0]*tree.MET_py

        a= tree.Muon_Pz[0]**2 - tree.Muon_E[0]**2
        b=2*X*tree.Muon_Pz[0]
        c= X**2 - tree.Muon_E[0]**2 *( tree.MET_px**2 + tree.MET_py**2 )
#        print "a: " , a , "\t b. " , b , " \t c: " , c
        D = b**2 - 4* a*c
        if(D<0):
            D=0

        MET_pz1 = (-b - np.sqrt(D))/(2*a)  #Look for selection between +sqrt D and -sqrt Dv
        MET_pz2 = (-b + np.sqrt(D))/(2*a)
        self.histograms["MET_z1"].Fill(MET_pz1 , w)
        self.histograms["MET_z2"].Fill(MET_pz2 , w)
#        udimentary, uneducated guess for MET_pz
        if(abs(MET_pz1)<abs(MET_pz2)):
            MET_pz = MET_pz1
        else:
            MET_pz = MET_pz2
#        print " 1: " , MET_pz1, " \t 2: ", MET_pz2
#========================================================================================
        All_4Vec.SetXYZM(tree.Jet_Px[lep_],tree.Jet_Py[lep_],tree.Jet_Pz[lep_],4.3)


        Sacrificial.SetXYZM(tree.Muon_Px[0],tree.Muon_Py[0],tree.Muon_Pz[0],tree.Muon_E[0])
        All_4Vec= All_4Vec + Sacrificial

        Sacrificial.SetXYZM(tree.MET_px,tree.MET_py , MET_pz,0)
#        Sacrificial.SetXYZM(tree.MET_px,tree.MET_py , 0,0)
        All_4Vec= All_4Vec + Sacrificial



        self.histograms["t_lep_m"].Fill(All_4Vec.M() , w)


    ### processEvent function implements the actions to perform on each event
    ### This is the place where to implement the analysis strategy: study of most sensitive variables
    ### and signal-like event selection

    def processEvent(self, entry):
        tree = self.getTree()
        tree.GetEntry(entry)
        if(self.cut_check(tree)):
            btag, n_btag =  self.get_btag_indices( tree)
            lep_ , non_lep_ = self.get_leptonic_nonleptonic_index( tree, btag, n_btag)  #Check this part if wierd masses are getting calculated
            self.hadronic_part( tree , non_lep_ , n_btag)
            self.leptonic_part( tree, lep_ )
            self.nAcc += 1
        if tree.triggerIsoMu24:
            self.nTrig +=1

#            hadronic_part(entry)




    ### processEvents run the function processEvent on each event stored in the tree
    def processEvents(self):
#        self.nEvents = 100
        nevts = self.nEvents
        for i in xrange(nevts):
            self.processEvent(i)

        self.saveHistos()
