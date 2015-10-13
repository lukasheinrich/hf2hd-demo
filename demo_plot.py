#!/usr/bin/env python 
import click
import ROOT
import math
import IPython
import parsexml
import histfactorycnv as hfc
import numpy as np

def combine_graphs(graphs,positionhist):
  result = graphs[0].Clone()
  for i in range(result.GetN()):
    x,y = np.array([0],dtype = float),np.array([0],dtype = float)
    result.GetPoint(i,x,y)

    total_widths = [g.GetErrorYhigh(i)+g.GetErrorYlow(i) for g in graphs]
    total_error = math.sqrt(sum(w**2 for w in total_widths))
    
    position = positionhist.GetBinContent(positionhist.FindBin(x))

    result.SetPoint(i,x,position)
    result.SetPointEYhigh(i,total_error/2.0)
    result.SetPointEYlow(i,total_error/2.0)
  return result

@click.command()
@click.argument('toplvlxml')
@click.argument('workspace')
@click.argument('channel')
@click.argument('observable')
@click.argument('plotfile')
def shape(toplvlxml,workspace,channel,observable,plotfile):
  parsed_data = parsexml.parse('config/simple.xml','./')
  firstmeas = parsed_data['toplvl']['measurements'].keys()[0]
  rootfile = '{}_{}_{}_model.root'.format(parsed_data['toplvl']['resultprefix'],workspace,firstmeas)
  samples = parsed_data['channels'][channel]['samples']
  sample_definition = [(samples[k]['HFname'],samples[k]) for k in ['signal','background1','background2']]

  f  = ROOT.TFile.Open(rootfile)
  ws = f.Get(workspace)
  x  = ws.var(hfc.obsname(observable,channel))
  
  mu_to_plot = 1

  mu = ws.var('mu')
  oldval = mu.getVal()
  mu.setVal(mu_to_plot)
  aset = ROOT.RooArgSet()
  aset.add(mu)
  mc = ws.obj('ModelConfig')
  mc.SetSnapshot(aset)
  mu.setVal(oldval)
  
  
  sample_definition = [
    ('signal',{
      'systs': {
      }
    }),
    ('background1',{
      'systs': {
        'systb1':{
          'HFname':'OverallSyst1',
          'HFtype':'OverallSys',
        },
      }
    }),
    ('background2',{
      'systs': {
        'systb2':{
          'HFname':'HistoSys1',
          'HFtype':'HistoSys',
        },
      }
    })
  ]
  
  all_bands = []

  colors = {'signal':ROOT.kAzure-9,'background1':ROOT.kRed+1,'background2':ROOT.kViolet-1}
  stack = ROOT.THStack()
  all_noms = []
  
  syst_bands = []
  for sample,sampledef in reversed(sample_definition):
    nom = hfc.extract_with_pars(ws,channel,observable,sample,{},reference_snapshot = 'ModelConfig__snapshot')
    nom.SetFillColor(colors[sample])
    nom.SetLineColor(ROOT.kBlack)
    stack.Add(nom)
    all_noms += [nom]

  topline_nosig = stack.GetStack().At(stack.GetStack().GetSize()-2)
  # IPython.embed()

  for sample,sampledef in reversed(sample_definition):
    for syst,defin in sampledef['systs'].iteritems():
      sysparsets = hfc.getsys_pars(defin['HFname'],defin['HFtype'], workspace = ws, observable = x,**(defin.get('additional_args',{})))
      up,nomvar,down = [hfc.extract_with_pars(ws,channel,observable,sample,parset, reference_snapshot = 'ModelConfig__snapshot') for parset in sysparsets]

      syst_bands += [hfc.make_band_root(up,down,nomvar)]

  c = ROOT.TCanvas()


  
  stack.Draw()
  
  stack.GetHistogram().GetXaxis().SetTitle("observable")
  stack.GetHistogram().GetYaxis().SetTitle("Events")

  error_graph = combine_graphs(syst_bands,topline_nosig)
  error_graph.Draw('sameE2')
  error_graph.SetFillColor(ROOT.kBlack)
  error_graph.SetFillStyle(3002)

  datahist = hfc.extract_data(ws,channel,observable)
  datahist.SetMarkerStyle(20)
  datahist.SetLineColor(ROOT.kBlack)
  datahist.SetMarkerColor(ROOT.kBlack)
  datahist.Draw('E0same')


  labels = ROOT.TLatex()
  labels.SetNDC(True)
  labels.SetTextSize(20)
  labels.SetTextFont(73)
  labels.DrawLatex(0.7,0.85,'Experiment')

  labels = ROOT.TLatex()
  labels.SetNDC(True)
  labels.SetTextSize(20)
  labels.SetTextFont(43)
  labels.DrawLatex(0.5,0.80,"#int L dt = XX fb^{-1}")
  labels.DrawLatex(0.5,0.70,"#sqrt{s} = Y TeV")

  legend = ROOT.TLegend(0.7,0.60,0.85,0.82)
  legend.AddEntry(datahist,'Data')
  legend.SetLineColor(0)
  
  for h,name in zip(reversed(all_noms),[x[0] for x in sample_definition]):
    legend.AddEntry(h,'signal (#mu={})'.format(mu_to_plot) if name=='signal' else name)
  legend.AddEntry(error_graph,'Syst. Uncert.')

  legend.Draw('same')

  c.SaveAs(plotfile)
  
if __name__=='__main__':
  shape()