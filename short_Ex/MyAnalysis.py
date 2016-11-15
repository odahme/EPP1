import ROOT
import copy
from Samples import samp

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
        print "Number of entries for " + self.sample + ": " + str(self.nEvents)

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


    def saveHistos(self):
        outfilename = self.sample + "_histos.root"
        outfile = ROOT.TFile(outfilename, "RECREATE")
        outfile.cd()
        for h in self.histograms.values():
            h.Write()
        outfile.Close()

    ### processEvent function implements the actions to perform on each event
    ### This is the place where to implement the analysis strategy: study of most sensitive variables
    ### and signal-like event selection

    def processEvent(self, entry):
        tree = self.getTree()
        tree.GetEntry(entry)
        w = tree.EventWeight

        ### Muon selection - Select events with at least 1 isolated muon
        ### with pt>25 GeV to match trigger requirements
        muonPtCut = 25.
        muonRelIsoCut = 0.05
        nIsoMu = 0

        for m in xrange(tree.NMuon):
            muon =ROOT.TLorentzVector(tree.Muon_Px[m],tree.Muon_Py[m],tree.Muon_Pz[m],tree.Muon_E[m])
            self.histograms["Muon_Iso"].Fill(tree.Muon_Iso[m], w)
            if(muon.Pt()>muonPtCut and (tree.Muon_Iso[m]/muon.Pt()) < muonRelIsoCut):
                nIsoMu += 1
            if(nIsoMu>0): self.histograms["Muon_Pt"].Fill(muon.Pt(), w)

        self.histograms["NIsoMu"].Fill(nIsoMu, w)



    ### processEvents run the function processEvent on each event stored in the tree
    def processEvents(self):
        nevts = self.nEvents
        for i in xrange(nevts):
            self.processEvent(i)

        self.saveHistos()
