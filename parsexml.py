import xml.etree.ElementTree as ET
import IPython
import os
def get_path(relative,base):
  return '{}/{}'.format(os.path.abspath(base),os.path.split(relative)[-1])

def format_sample_sys(element,rootdir):
  data = {
    'HFname':element.attrib['Name'],
    'HFtype':element.tag
  }
  return element.attrib['Name'],data
  
def format_channel_input(inputxml,rootdir):
  channel = inputxml.getroot()
  data = {
    'HFname':channel.attrib['Name'],
    'samples':{
      s.attrib['Name'] :
      {
        'HFname':s.attrib['Name'],
        'systs':dict(*zip([format_sample_sys(x,rootdir) for x in s.iter() if 'Sys' in x.tag])) 
      }
      for s in channel.findall('Sample')
    }
  }
  return data

def parse(configfile,rootdir):
  toplvl = ET.parse(configfile)
  for x in toplvl.findall('Input'):
    print get_path(x.text,rootdir)
  inputs = [ET.parse(x.text) for x in toplvl.findall('Input')]
  channels = {
    x['HFname']:x for x in [format_channel_input(inp,rootdir) for inp in inputs]
  }
  return {
    'toplvl':{
      'resultprefix':toplvl.getroot().attrib['OutputFilePrefix'],
      'measurements':{x.attrib['Name']:{} for x in toplvl.findall('Measurement')}
    },
    'channels': channels
  }

def main():
  print parse('./config/simple.xml','.')
  
if __name__ == '__main__':
  main()