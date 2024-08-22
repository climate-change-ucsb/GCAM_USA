# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import xml.etree.ElementTree as ET

def pathGen(fn):
    path = []
    it = ET.iterparse(fn, events=('start', 'end'))
    for evt, el in it:
        if evt == 'start':
            path.append(el.tag)
            yield '/'.join(path)
        else:
            path.pop()
            
path='/Users/haozheyang/Documents/GCAM/gcam-v6.0-Mac-Release-Package/input/gcamdata/xml/'
tree = ET.parse(path + 'elecS_costs_USA_itc.xml')

for pth in pathGen(path + 'elecS_costs_USA_itc.xml'):
    print(pth)

root = tree.getroot()
root.tag
root.attrib
for child in root:
    print(child.tag, child.attrib)
    
for technology in root.iter('technology'):
    print(technology.attrib)

for period in root.iter('period'):
    print(period.attrib)
    
    
for fixed_charge_rate in root.iter('fixed-charge-rate'):
    print(fixed_charge_rate.text)
    
for technology in root.findall('location-info'):
    name = technology.get('name')
    print(name)      

technology.tag
technology.attrib
for child in technology:
    print(child.tag, child.attrib)

# find fiixed charge rate of PV
for PV in root.findall(".//period/..[@name='PV_base_storage']"):
    PV

for PV in root.findall(".//global-technology-database/location-info/technology[@name='PV_base_storage']"):
    PV
    
i=0
for child in PV:
    i=i+1
    print(child.tag, child.attrib)
    
i=0
for period in PV.findall('period'):
    year=period.get('year')
    charge_rate = period.find('input-capital/fixed-charge-rate')
    new_charge_rate = float(period.find('input-capital/fixed-charge-rate').text)-0.01
    charge_rate.text=str(new_charge_rate)
    
    print(year,charge_rate.text)

tree.write('/Users/haozheyang/Documents/GCAM/output.xml')   
    
    
