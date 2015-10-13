#!/usr/bin/env python 
import click
import ROOT
import histfactorycnv.hepdata as hft_hepdata
import yaml
import sys
import parsexml


@click.command()
@click.argument('toplvlvxml')
@click.argument('workspace')
@click.argument('channel')
@click.argument('observable')
@click.argument('outputfile')
def main(toplvlvxml,workspace,channel,observable,outputfile):  
  parsed_data = parsexml.parse('config/simple.xml','./')
  firstmeas = parsed_data['toplvl']['measurements'].keys()[0]
  rootfile = '{}_{}_{}_model.root'.format(parsed_data['toplvl']['resultprefix'],workspace,firstmeas)
  samples = parsed_data['channels'][channel]['samples']
  sample_definition = [(samples[k]['HFname'],samples[k]) for k in ['signal','background1','background2']]
  
  
  f  = ROOT.TFile.Open(rootfile)
  ws = f.Get(workspace)
  
  hepdata_table = hft_hepdata.hepdata_table(ws,channel,observable,sample_definition)
  
  with open(outputfile,'w') as f:
    f.write(yaml.safe_dump(hepdata_table,default_flow_style = False))

if __name__=='__main__':
  main()