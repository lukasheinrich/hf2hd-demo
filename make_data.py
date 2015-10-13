#!/usr/bin/env python

import numpy
import ROOT

def main():
  min_x,max_x = 200,600
  nbins = 25

  f = ROOT.TFile.Open('data/input.root','recreate')
  
  dummydata = ROOT.TH1F('data','data',nbins,min_x,max_x)
  dummydata.Write()
  
  hb1 =  ROOT.TH1F('background1','background1',nbins,min_x,max_x)
  events = numpy.random.exponential(150,20000)
  for e in filter(lambda x:min_x<x<max_x,events): hb1.Fill(e)
  hb1.Write()
  
  hb2 = ROOT.TH1F('background2','background2',nbins,min_x,max_x)
  events = numpy.random.normal(175,75,2000)
  for e in filter(lambda x:min_x<x<max_x,events): hb2.Fill(e)
  hb2.Write()
  
  hb2_dn = ROOT.TH1F('background2_sysdown','background2_sysdown',nbins,min_x,max_x)
  events = numpy.random.normal(150,75,2000)
  for e in filter(lambda x:min_x<x<max_x,events): hb2_dn.Fill(e)
  hb2_dn.Write()
  
  hb2_up = ROOT.TH1F('background2_sysup','background2_sysup',nbins,min_x,max_x)
  events = numpy.random.normal(200,75,2000)
  for e in filter(lambda x:min_x<x<max_x,events): hb2_up.Fill(e)
  hb2_up.Write()
  
  hs =  ROOT.TH1F('signal','signal',nbins,min_x,max_x)
  events = numpy.random.normal(400,20,200)
  for e in filter(lambda x:min_x<x<max_x,events): hs.Fill(e)
  hs.Write()
  
  f.Close()
  
if __name__=='__main__':
  main()