#!/usr/bin/env python 
import click
import ROOT
import hftools.hepdata as hft_hepdata
import yaml
import sys
import hftools.utils.parsexml as parsexml
import subprocess
import logging
logging.basicConfig(level = logging.INFO)

@click.command()
@click.argument('toplvlxml')
@click.argument('channel')
@click.argument('outputfile')
@click.option('-b','--observable', default = 'x')
@click.option('-w','--workspace', default = 'combined')
def main(toplvlxml,workspace,channel,observable,outputfile):  
  parsed_data = parsexml.parse('config/simple.xml','./')
  firstmeas   = parsed_data['toplvl']['measurements'].keys()[0]
  samples     = parsed_data['channels'][channel]['samples']
  sample_definition = [(samples[k]['HFname'],samples[k]) for k in ['signal','background1','background2']]
  
  subprocess.call('hist2workspace {}'.format(toplvlxml), shell = True)
  
  rootfile = '{}_{}_{}_model.root'.format(parsed_data['toplvl']['resultprefix'],workspace,firstmeas)


  f  = ROOT.TFile.Open(str(rootfile))
  ws = f.Get(str(workspace))

  hepdata_table = hft_hepdata.hepdata_table(ws,channel,observable,sample_definition)
  
  with open(outputfile,'w') as f:
    f.write(yaml.safe_dump(hepdata_table,default_flow_style = False))

if __name__=='__main__':
  main()