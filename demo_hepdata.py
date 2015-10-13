#!/usr/bin/env python 
import click
import ROOT
import histfactorycnv.hepdata as hft_hepdata
import yaml
import sys

@click.command()
@click.argument('rootfile')
@click.argument('workspace')
@click.argument('channel')
@click.argument('observable')
@click.argument('outputfile')
def main(rootfile,workspace,channel,observable,outputfile):  
  sample_definition = [
    ('signal',{
      'systs': {
      }
    }),
    ('background1',{
      'systs': {
        'b1norm':{
          'HFname':'OverallSyst1',
          'HFtype':'OverallSys',
        },
      }
    }),
    ('background2',{
      'systs': {
        'b2shape':{
          'HFname':'HistoSys1',
          'HFtype':'HistoSys',
        },
      }
    })
  ]
  
  f  = ROOT.TFile.Open(rootfile)
  ws = f.Get(workspace)
  
  hepdata_table = hft_hepdata.hepdata_table(ws,channel,observable,sample_definition)
  
  with open(outputfile,'w') as f:
    f.write(yaml.safe_dump(hepdata_table,default_flow_style = False))

if __name__=='__main__':
  main()