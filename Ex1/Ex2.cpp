
#include "TCanvas.h"
#include "TF1.h"
#include "TApplication.h"
#include "TH1F.h"
#include "TRandom3.h"
#include "TFile.h"
#include "TTree.h"
#include "TBranch.h"
#include "RooRealVar.h"
#include <cmath>
#include <stdio.h>
#include <stdlib.h>
#include <TH3F.h>
#include <time.h>
#include <math.h>

using namespace std;


int main(int argc, char **argv) {

  //create a window
  TApplication theApp("demoApplication",&argc,argv);

  TCanvas *c1 = new TCanvas("c1","Example1",1920,1080);
  // TCanvas *c2 = new TCanvas("c2","Example2",1920,1080);
  // TCanvas *c3 = new TCanvas("c3","Example3",1920,1080);
  // TCanvas *c4 = new TCanvas("c4","Example4",1920,1080);
  // TCanvas *c5 = new TCanvas("c5","Example5",1920,1080);
  // TCanvas *c6 = new TCanvas("c6","Example6",1920,1080);

  TRandom3 *rand = new TRandom3(42);

  TH1F *histbreit = new TH1F("histbreit","Breit Wigner",100,748,820);


  size_t number = 1000;
  for (size_t i = 0; i < number; i++) {
    double m = rand->Uniform(748,820);
    double w = (6.)/ (pow(m-748,2) + 36);
    histbreit->Fill(m,w);
  }

  //hit and miss method
  size_t hit = 0;
  number = 256;
  for(int i=0; i<number; ++i)
  {
    double x = rand->Uniform(0,1);
    double y_s = rand->Uniform(0,1);
    double y = pow(x,3);
    if (y_s <= y)
    {
      hit++;
    }
  }
  std::cout << "I hit miss 256 = " << hit*1.0/number*1.0 << std::endl;
  std::cout << "sigma = " << 1/(sqrt(number*1.0-1)) * sqrt((hit*1.0/number*1.0)*(1-hit*1.0/number*1.0)) << std::endl;
  std::cout << "---------" << std::endl;

  hit = 0;
  number = 512;
  for(int i=0; i<number; ++i)
  {
    double x = rand->Uniform(0,1);
    double y_s = rand->Uniform(0,1);
    double y = pow(x,3);
    if (y_s <= y)
    {
      hit++;
    }
  }
  std::cout << "I hit miss 512 = " << hit*1.0/number*1.0 << std::endl;
  std::cout << "sigma = " << 1/(sqrt(number*1.0-1)) * sqrt((hit*1.0/number*1.0)*(1-hit*1.0/number*1.0)) << std::endl;
  std::cout << "---------" << std::endl;

  c1->cd();
  histbreit->Draw();
  //turns off the program with mous clic
  theApp.Connect("TCanvas","Closed()","TApplication",&theApp,"Terminate()");
  //starts the canvas
  theApp.Run();

  return 0;
}
