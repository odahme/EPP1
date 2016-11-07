
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
  TCanvas *c2 = new TCanvas("c2","Example2",1920,1080);
  TCanvas *c3 = new TCanvas("c3","Example3",1920,1080);
  TCanvas *c4 = new TCanvas("c4","Example4",1920,1080);
  TCanvas *c5 = new TCanvas("c5","Example5",1920,1080);
  TCanvas *c6 = new TCanvas("c6","Example6",1920,1080);



  TH1F *hitMissHist = new TH1F("hitMiss","Hit and Miss",100,0.24,0.26);
  TH1F *hitMissDist = new TH1F("hitMissDist","Hit and Miss Distribution",100,0,1);
  TH1F *histStrat1 = new TH1F("Strat1","Stratified sampling 0.5",100,0.22,0.28);
  TH1F *histStrat2 = new TH1F("Strat2","Stratified sampling 0.65",100,0.22,0.28);
  TH1F *histStrat3 = new TH1F("Strat3","Stratified sampling 0.5 0.15",100,0.22,0.28);
  TH1F *importhist = new TH1F("importhist","Importance sampling",100,0.248,0.252);

  TRandom3 *rand = new TRandom3(42);


for (size_t toy = 0; toy < 40; toy++) {




  //hit and miss method
  size_t hit = 0;
  size_t number = 100000;
  for(int i=0; i<number; ++i)
  {
    double x = rand->Uniform(0,1);
    double y_s = rand->Uniform(0,1);
    double y = pow(x,3);
    if (y_s <= y)
    {
      hit++;
      if (toy == 0) {
        hitMissDist->Fill(x);
      }
    }
  }
  std::cout << "I hit miss = " << hit*1.0/number*1.0 << std::endl;
  std::cout << "sigma = " << 1/(sqrt(number*1.0-1)) * sqrt((hit*1.0/number*1.0)*(1-hit*1.0/number*1.0)) << std::endl;
  std::cout << "---------" << std::endl;
  hitMissHist->Fill(hit*1.0/number*1.0);


  //Stratified sampling

double w[3] = {0.5,0.65};
for (size_t i = 0; i < 2; i++) {
  double d = w[i];
  hit = 0;
  for (size_t i = 0; i < number*0.5; i++) {
    double x = rand->Uniform(0,d);
    double y_s = rand->Uniform(0,1);
    double y = pow(x,3);
    if (y_s <= y)
    {
      hit++;
    }
  }
  double res =(d)* hit*1.0/(number*0.5);
  hit = 0;
  for (size_t j = number*0.5; j < number; j++) {
    double x = rand->Uniform(d,1);
    double y_s = rand->Uniform(0,1);
    double y = pow(x,3);
    if (y_s <= y)
    {
      hit++;
    }
  }
  res +=(1.-d)* hit*1.0/(number*0.5);

  std::cout << "I Stratified "<<d<<" = " << res << std::endl;
  std::cout << "---------" << std::endl;
  if (d == 0.5) {
    histStrat1->Fill(res);
  }
  if (d == 0.65) {
    histStrat2->Fill(res);
  }
}

double d = 0.5;
hit = 0;
for (size_t i = 0; i < number*0.15; i++) {
  double x = rand->Uniform(0,d);
  double y_s = rand->Uniform(0,1);
  double y = pow(x,3);
  if (y_s <= y)
  {
    hit++;
  }
}

double res = d* hit*1.0/(number*0.15);

for (size_t i = number*0.15; i < number; i++) {
  double x = rand->Uniform(d,1);
  double y_s = rand->Uniform(0,1);
  double y = pow(x,3);
  if (y_s <= y)
  {
    hit++;
  }
}
res += (1-d)* hit*1.0/(number*0.85);
std::cout << "I Stratified "<<d<<" = " << res << std::endl;
std::cout << "---------" << std::endl;
histStrat3->Fill(res);

//importance sampling
res = 0;
for (size_t i = 0; i < number; i++) {
  double u = rand->Uniform(0,1/3.);
  double x = pow(3*u,1/3.);
  res += x;
}
res /= number*3;
std::cout << "I Importance 2x = " << res << std::endl;
std::cout << "---------" << std::endl;
importhist->Fill(res);

//Antithetic variables



}
  c1->cd();
  hitMissHist->Fit("gaus");
  hitMissHist->Draw();
  c3->cd();
  histStrat1->Fit("gaus");
  histStrat1->Draw();
  c3->cd();
  histStrat2->Fit("gaus");
  histStrat2->Draw();
  c5->cd();
  histStrat3->Fit("gaus");
  histStrat3->Draw();
  c6->cd();
  importhist->Fit("gaus");
  importhist->Draw();
  c2->cd();
  hitMissDist->Draw();

  //turns off the program with mous clic
  theApp.Connect("TCanvas","Closed()","TApplication",&theApp,"Terminate()");
  //starts the canvas
  theApp.Run();

  return 0;
}
