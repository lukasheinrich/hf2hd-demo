#!/usr/bin/env python
import IPython
import ROOT

def main():
  f = ROOT.TFile.Open('./results/example_combined_Meas1_model.root')
  ws = f.Get('combined')
  x = ws.var('obs_x_channel1')
  fr = x.frame()
  
  mu = ws.var('mu')
  mu.setVal(0)
  
  pdf = ws.pdf('model_channel1')
  pdf.plotOn(fr)
  fr.Draw()

  s = ROOT.RooArgSet()
  s.add(x)
  
  al = ROOT.RooArgList()
  al.add(x)
  
  data = pdf.generate(s)
  
  datahist = x.createHistogram('data')
  data.fillHistogram(datahist,al)
  datahist.Sumw2(0)

  datahist.Draw('E0')
  datahist.SetName("data")
  datahist.SetTitle("data")
  datahist.SetDirectory(0)

  f = ROOT.TFile.Open('data/input.root','update')
  k = f.GetKey('data')
  k.Delete()
  datahist.Write()
  f.Close()
  
if __name__=='__main__':
  main()