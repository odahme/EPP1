#include <cmath>
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <TRandom3.h>
#include <TH3F.h>
#include <TH2F.h>
#include <TCanvas.h>
#include <TApplication.h>
#include "TMath.h"
#include "TVectorD.h"
#include "TF2.h"
#include "TF1.h"
#include "TGraph.h"
using namespace std;


int main(int argc, char **argv)
{
  //create a window
  TApplication theApp("demoApplication",&argc,argv);
  // create a canvas
  TCanvas *c1 = new TCanvas("c1","c1",1,1,1024,768);
  TCanvas *c2 = new TCanvas("c2","c2",1,1,1024,768);

  unsigned int np = 5;

  TVectorD *xvals = new TVectorD(np);
  TVectorD *yvals = new TVectorD(np);
  for (size_t i = 0; i < np; i++) {
    (*xvals)[i] = i;
  }
  (*yvals)[0] = 1.49;
  (*yvals)[1] = 1.58;
  (*yvals)[2] = 1.67;
  (*yvals)[3] = 1.80;
  (*yvals)[4] = 1.908;


  c1->cd();
  TF1 *f1 = new TF1("f1","[0] + [1]*x",0,10);
  TGraph *gr1 = new TGraph(*xvals,*yvals);
  gr1->Fit(f1);
  gr1->Draw("A*");

  c2->cd();
  TF2 *chi = new TF2("chi","(y - [0] + [1]*x)**2",0,10);
  TGraph *gr2 = new TGraph(*xvals,*yvals);
  gr2->Fit(chi);
  gr2->Draw("A*");

  //turns off the program with mous clic
  theApp.Connect("TCanvas","Closed()","TApplication",&theApp,"Terminate()");
  //starts the canvas
  theApp.Run();
  return 1;
}
