
#include "iostream"

#ifndef __CINT__
#include "RooGlobalFunc.h"
#endif

#include "TCanvas.h"
#include "TF1.h"
#include "TApplication.h"
#include "TH1F.h"
#include "TRandom3.h"
#include "TFile.h"
#include "TTree.h"
#include "TBranch.h"
#include "RooRealVar.h"
#include "RooGaussian.h"
#include "RooRealVar.h"
#include "RooDataSet.h"
#include "RooArgSet.h"
#include "RooExponential.h"
#include "RooAddPdf.h"
#include "RooAbsReal.h"
#include "RooPlot.h"
#include "RooMinuit.h"
#include "TLegend.h"
#include "TAxis.h"
#include "TFile.h"

using namespace RooFit ;


int main(int argc, char **argv) {

  //create a window
  TApplication theApp("demoApplication",&argc,argv);

  TCanvas *c1 = new TCanvas("c1","Example1",1920,1080);
  TCanvas *c2 = new TCanvas("c2","Example2",1920,1080);
  TFile *f = new TFile("myfile.root");
  TTree *t = (TTree*) f->Get("myTree");
  double val;
  t->SetBranchAddress("mass",&val);
  size_t entries = t->GetEntries();

  TH1F *hist = new TH1F("hist","Histogram of mass",100,50,150);

  RooRealVar *x = new RooRealVar("x","x",100,50,150);
  RooRealVar *mean = new RooRealVar("mean","mean of Gaussian",50,150);
  RooRealVar *sigma = new RooRealVar("sigma","sigma of Gaussian",0,10);
  RooGaussian *gaus = new RooGaussian("gaus","gaussian pdf",*x,*mean,*sigma);
  RooRealVar *c = new RooRealVar("c","c",0.001,0.1);
  RooExponential *expo = new RooExponential("expo","exponatial pdf",*x,*c);
  RooRealVar *frac = new RooRealVar("frac","frac",0.5,0.0,1.0) ;
  RooAddPdf *model = new RooAddPdf("model","model",RooArgList(*gaus,*expo),*frac) ;


  RooDataSet *data = new RooDataSet("data","data of mass",RooArgSet(*x));
  for (size_t i = 0; i < entries; i++) {
    t->GetEntry(i);
    hist->Fill(val);
    x->setVal(val);
    data->add(RooArgSet(*x));
  }

  RooAbsReal *nll = model->createNLL(*data);
  RooMinuit *m = new RooMinuit(*nll);
  m->migrad();

//  TLegend *leg = new TLegend(0.1,0.7,0.48,0.9);
//  leg->AddEntry(data,"datapoints");
//  leg->AddEntry(model,"fit");
  RooPlot *xframe = x->frame(Name("xframe"),Title("fit example"),Bins(100));
  data->plotOn(xframe);
  model->plotOn(xframe);
  model->paramOn(xframe);
  xframe->GetXaxis()->SetTitle("M[GeV]");
  c1->cd();
  xframe->Draw();
//  leg->Draw("LP");
  c2->cd();
  hist->Draw();




  //turns off the program with mous clic
  theApp.Connect("TCanvas","Closed()","TApplication",&theApp,"Terminate()");
  //starts the canvas
  theApp.Run();

  return 0;
}
