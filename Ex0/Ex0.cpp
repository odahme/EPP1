
#include "iostream"

#include "TCanvas.h"
#include "TF1.h"
#include "TApplication.h"
#include "TH1F.h"
#include "TRandom3.h"
#include "TFile.h"
#include "TTree.h"
#include "TBranch.h"
#include "RooRealVar.h"












int main(int argc, char **argv) {

  //create a window
  TApplication theApp("demoApplication",&argc,argv);

  TCanvas *c1 = new TCanvas("c1","Example1",1920,1080);
  TCanvas *c2 = new TCanvas("c2","Example2",1920,1080);
  TCanvas *c3 = new TCanvas("c3","Example3",1920,1080);

  c1->cd();
  TF1 *func = new TF1("func","abs(sin(x)/x)",0,10);
  c1->SetGridx();
  c1->SetGridy();
  func->Draw();

  c2->cd();
  TH1F *histo = new TH1F("histo","Histo Example",10,0,10);
  histo->Fill(3);
  histo->Fill(4.8,4);
  histo->Fill(5.6,3);
  histo->Fill(3.9,2);
  histo->Draw();
  std::cout << "Mean of histo = "<< histo->GetMean() << std::endl;
  std::cout << "RMS of histo = "<< histo->GetRMS() << std::endl;

  TH1F *hist_sim = new TH1F("hist_sim","Histogram of simulated Data",100,50,150);
  TFile *f = new TFile("myfile.root","RECREATE");
  TTree *t = new TTree("myTree","exampleTree");
  double val = 0;
  t->Branch("mass",&val,"mass/D");


  TRandom3 *rnd = new TRandom3(42);
  for (size_t i = 0; i < 3000;) {
    val = rnd->Gaus(91.19,2.49);
    if (val > 50 && val < 150) {
      hist_sim->Fill(val);
      t->Fill();
      i++;
    }
  }
  for (size_t i = 0; i < 20000;) {
    val = rnd->Exp(0.05) + 50;
    if (val > 50 && val < 150) {
      hist_sim->Fill(val);
      t->Fill();
      i++;
    }
  }

  f->Write();
  f->Close();
  c3->cd();
  hist_sim->Draw();

  //turns off the program with mous clic
  theApp.Connect("TCanvas","Closed()","TApplication",&theApp,"Terminate()");
  //starts the canvas
  theApp.Run();

  return 0;
}
