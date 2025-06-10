#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 20:32:34 2024

@author: haozheyang
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
import random

def pathGen(fn):
    path = []
    it = ET.iterparse(fn, events=('start', 'end'))
    for evt, el in it:
        if evt == 'start':
            path.append(el.tag)
            yield '/'.join(path)
        else:
            path.pop()
            
share_path='/Users/hy4174/Documents/gcam-v6.0/input/' 
#%% itc base file generation

itc_base_path='gcamdata/xml/elec_segments_water_USA_new.xml'
#base file
tree_itc_base = ET.parse(share_path + itc_base_path)
root_itc_base = tree_itc_base.getroot()

tree_cost_base = ET.parse(share_path + itc_base_path)
root_cost_base = tree_cost_base.getroot()


#%%
for parent in root_itc_base.findall('.//region/..'):
    for region in list(parent):  #getchildren() will be depreciated after python 3.9 
        if region.tag!='global-technology-database':
            parent.remove(region)

#%% fixed charge rate

for tech in root_itc_base.findall('.//period/..'):
    #print(tech.attrib)
    for period in tech.findall('period'):        
        if int(period.get('year')) < 2025:
            tech.remove(period)

            
for parent in root_itc_base.findall('.//input-capital/..'):
    for child in list(parent):
        #print(child.tag)
        if child.tag != 'input-capital':
            parent.remove(child)
        else:
            for grand in list(child):
                if grand.tag!='fixed-charge-rate':
                    child.remove(grand)
        
    
tree_itc_base.write(share_path + "policy_base/itc_base.xml") 

#%% cost
for parent in root_cost_base.findall('.//region/..'):
    for region in list(parent):  #getchildren() will be depreciated after python 3.9 
        if region.tag!='global-technology-database':
            parent.remove(region)


for tech in root_cost_base.findall('.//period/..'):
    #print(tech.attrib)
    for period in tech.findall('period'):        
        if int(period.get('year')) < 2025:
            tech.remove(period)

            
for parent in root_cost_base.findall('.//input-capital/..'):
    for child in list(parent):
        #print(child.tag)
        if child.tag != 'input-capital':
            parent.remove(child)
        else:
            for grand in list(child):
                if grand.tag!='capital-overnight':
                    child.remove(grand)
        
    
    
tree_cost_base.write(share_path + "policy_base/cost_base.xml") 

#%% CO2
tree_cost_base = ET.parse(share_path + itc_base_path)
root_cost_base = tree_cost_base.getroot()

for parent in root_cost_base.findall('.//region/..'):
    for region in list(parent):  #getchildren() will be depreciated after python 3.9 
        if region.tag == "global-technology-database":
            parent.remove(region)        
        elif 'grid' in region.attrib['name']:
            continue
        else:
            #if region.tag!='global-technology-database':
            parent.remove(region)

                
for parent in root_cost_base.findall('.//supplysector/..'):
    for supplysector in list(parent):
        if supplysector.tag !="supplysector":
            parent.remove(supplysector)
        else:
            for subsector in list(supplysector):
                if subsector.tag!="subsector":
                    supplysector.remove(subsector)
                else:
                    for pass_through in list(subsector):
                        if pass_through.tag not in ["pass-through-technology","technology"]:
                            subsector.remove(pass_through)
                        else:
                            for period in list(pass_through):
                                for grand in list(period):
                                    if grand.tag != 'CO2':
                                        period.remove(grand)
        
    
tree_cost_base.write(share_path + "policy_base/constraint_base.xml") 


tree_cost_base = ET.parse(share_path + itc_base_path)
root_cost_base = tree_cost_base.getroot()

for parent in root_cost_base.findall('.//region/..'):
    for region in list(parent):  #getchildren() will be depreciated after python 3.9 
        if region.tag != "global-technology-database":
            parent.remove(region)        


                
for parent in root_cost_base.findall('.//period/..'):
    for period in list(parent):
        for grand in list(period):
            if grand.tag != 'CO2':
                period.remove(grand)
        
    
tree_cost_base.write(share_path + "policy_base/constraint_all_base.xml") 
#%% tree USA
share_base_path='gcamdata/xml/elec_segments_water_USA.xml'
tree_share_base = ET.parse(share_path + share_base_path)
root_share_base = tree_share_base.getroot()

for parent in root_share_base.findall('.//region/..'):
    for region in list(parent):  #getchildren() will be depreciated after python 3.9 
        if (region.tag =='global-technology-database'):
            parent.remove(region)
        elif (region.attrib['name'] =='USA') | ('grid' in region.attrib['name']):
            parent.remove(region)

for parent2 in root_share_base.findall('.//nesting-subsector/..'):
    for child2 in list(parent2):
        if child2.tag!="nesting-subsector":
            parent2.remove(child2)
        for grand2 in list(child2):
            if grand2.tag != "subsector":
                child2.remove(grand2)

    #print(tech.attrib)

for parent3 in root_share_base.findall('.//subsector/stub-technology/..'):
    for child3 in list(parent3):
        #print(child.tag)
        if child3.tag != 'stub-technology':
            parent3.remove(child3)
        elif child3.tag =="stub-technology":
            for grand in list(child3):
                if grand.tag !="period":
                    child3.remove(grand)
                else:
                    for period in list(grand):
                        grand.remove(period)
                
            
tree_share_base.write(share_path + "policy_base/power_constraint_base.xml") 


#%% CCS share weight

#elec
share_base_path='gcamdata/xml/elec_segments_water_USA.xml'
tree_share_base = ET.parse(share_path + itc_base_path)
root_share_base = tree_share_base.getroot()

for parent in root_share_base.findall('.//region/..'):
    for region in list(parent):  #getchildren() will be depreciated after python 3.9 
        if (region.tag =='global-technology-database'):
            parent.remove(region)
        elif (region.attrib['name'] =='USA') | ('grid' in region.attrib['name']):
            parent.remove(region)

for parent2 in root_share_base.findall('.//nesting-subsector/..'):
    for child2 in list(parent2):
        if child2.tag!="nesting-subsector":
            parent2.remove(child2)
        for grand2 in list(child2):
            if grand2.tag != "subsector":
                child2.remove(grand2)

    #print(tech.attrib)

for parent3 in root_share_base.findall('.//subsector/share-weight/..'):
    for child3 in list(parent3):
        #print(child.tag)
        if child3.tag != 'share-weight':
            parent3.remove(child3)
        else:
            if int(child3.get('year'))<2025:
                parent3.remove(child3)
            
'''            
for parent in root_share_base.findall('.//region/..'):
    for region in list(parent):  #getchildren() will be depreciated after python 3.9 
        if region.tag!='global-technology-database':
            parent.remove(region)

for tech in root_share_base.findall('.//period/..'):
    #print(tech.attrib)
    for period in tech.findall('period'):        
        if int(period.get('year')) < 2025:
            tech.remove(period)

            
for parent in root_share_base.findall('.//share-weight/..'):
    for child in list(parent):
        #print(child.tag)
        if child.tag != 'share-weight':
            parent.remove(child)
'''
tree_share_base.write(share_path + "policy_base/share_USA_base.xml") 

#transformation
share_tr_base_path='gcamdata/xml/en_transformation_USA.xml'
tree_share_tr_base = ET.parse(share_path + share_tr_base_path)
root_share_tr_base = tree_share_tr_base.getroot()

for parent in root_share_tr_base.findall('.//region/..'):
    for region in list(parent):  #getchildren() will be depreciated after python 3.9 
        if (region.tag =='global-technology-database'):
            parent.remove(region)
        elif (region.attrib['name'] =='USA') | ('grid' in region.attrib['name']):
            parent.remove(region)            
        for pass_through in list(region):
            if pass_through.tag!= 'pass-through-sector':
                region.remove(pass_through)
            else:
                for subsector in list(pass_through):
                    if subsector.tag != "subsector":
                        pass_through.remove(subsector)
                    else:
                        for stub in list(subsector):
                            subsector.remove(stub)

tree_share_tr_base.write(share_path + "policy_base/en_transformation_share_base.xml") 

#hydrogen
share_h2_base_path='gcamdata/xml/Hydrogen_USA.xml'
tree_share_h2_base = ET.parse(share_path + share_h2_base_path)
root_share_h2_base = tree_share_h2_base.getroot()

for parent in root_share_h2_base.findall('.//region/..'):
    for region in list(parent):  #getchildren() will be depreciated after python 3.9 
        if region.attrib['name']=='USA':
            parent.remove(region)
        else: 
            for supplysector in list(region):
                if supplysector.attrib['name'] != "H2 central production":
                    region.remove(supplysector)
                else:
                    for subsector in list(supplysector):
                        if subsector.tag!= "subsector":
                            supplysector.remove(subsector)
                        elif subsector.attrib['name'] not in ['coal','gas','biomass']:
                            supplysector.remove(subsector)
                        else: 
                            for stub in list(subsector):
                                subsector.remove(stub)
                            

'''
for tech in root_share_h2_base.findall('.//subsector/..'):
    #print(tech.attrib)
    for subsector in tech.findall('subsector'):        
        if subsector.attrib['name'] not in ['coal','gas','biomass']:
            tech.remove(subsector)
        if subsector.tag != "subsector":
            tech.remove(subsector)
'''        
tree_share_h2_base.write(share_path + "policy_base/H2_share_base.xml") 

#%%
share_base_path='gcamdata/xml/en_distribution.xml'
tree_share_base = ET.parse(share_path + share_base_path)
root_share_base = tree_share_base.getroot()

for parent in root_share_base.findall('.//region/..'):
    for region in list(parent):  #getchildren() will be depreciated after python 3.9 
        if (region.tag =='global-technology-database'):
            parent.remove(region)
        elif (region.attrib['name'] !='USA'):
            parent.remove(region)
        else:
            for supplysector in list(region):
                if supplysector.attrib['name'] != 'backup_electricity':
                    region.remove(supplysector)
                else:
                    for sub in list(supplysector):
                        if sub.tag!="subsector":
                            supplysector.remove(sub)
                        else:
                            for tech in list(sub):
                                if tech.tag!= 'stub-technology':
                                    sub.remove(tech)
tree_share_base.write(share_path + "policy_base/en_USA_base.xml") 
 
#%% biomass constraint
share_biomass_path='gcamdata/xml/regional_biomass_USA.xml'
tree_share_biomass = ET.parse(share_path + share_biomass_path)
root_share_biomass = tree_share_biomass.getroot()
     
for parent in root_share_biomass.findall('.//region/..'):
    for region in list(parent):  #getchildren() will be depreciated after python 3.9 
        if region.attrib['name'] =='USA':
            parent.remove(region)            
        for supply_sector in list(region):
            if supply_sector.tag!= 'supplysector':
                region.remove(supply_sector)
            else:
                for subsector in list(supply_sector):
                    if subsector.tag != "subsector":
                        supply_sector.remove(subsector)
                    else:
                        for technology in list(subsector):
                            if (technology.tag!= "technology") & (technology.tag!= "stub-technology"):
                                subsector.remove(technology)
                            else:
                                for period in list(technology):
                                    if period.tag != 'period':
                                        technology.remove(period)
                                    elif int(period.attrib['year'])<2025:
                                        technology.remove(period)
                                    else:
                                        for child in list(period):
                                            period.remove(child)

tree_share_biomass.write(share_path + "policy_base/regional_biomass_base.xml") 
       
#%% empty base file generation

for tech in root_itc_base.findall('.//period/..'):
    for period in tech.findall('period'):         
        if int(period.get('year')) < 2025:
            tech.remove(period)
        for child in list(period):   
            period.remove(child)
               
tree_itc_base.write(share_path + "policy_base/empty_base.xml") 

#%% transportation
transport_base_path='gcamdata/xml/transportation_USA_CORE.xml'
#base file
tree_transport_base = ET.parse(share_path + transport_base_path)
root_transport_base = tree_transport_base.getroot()

#all vehicles
for world in root_transport_base.iter('world'):
    for region in world.findall('./region'):
        if region.attrib['name'] == 'USA':
            world.remove(region)
        else:
            for region_child in list(region):
                if region_child.tag!='supplysector':
                    region.remove(region_child)
                    
for supplysector in root_transport_base.findall('.//supplysector'):
    for supply_child in list(supplysector):  
        if supply_child.tag!='tranSubsector':
            supplysector.remove(supply_child)
        else:
            for subsector_child in list(supply_child):
                if subsector_child.tag!='stub-technology':
                    supply_child.remove(subsector_child)
                else: 
                    for period in subsector_child.findall('period'):
                        if int(period.get('year')) < 2025:
                            subsector_child.remove(period)
                        else:   
                            for child in list(period):
                                if child.tag!= 'minicam-non-energy-input':
                                    period.remove(child)
                            
tree_transport_base.write(share_path + "policy_base/transport_base.xml") 

#%% change file
#%% case and stop year
case_number=1

case_id=['case_'+str(i) for i in range(1,case_number+1)]

stop_year=2030

#%%change file this is template file with random numbers
from input_function import itc_function

itc_path=share_path + 'policy_base/itc_base.xml'
itc_output_path=share_path+'policy_change/itc_change'

itc_technology=['CSP_base_storage','PV_base_storage',
                'wind_base_offshore',
                'rooftop_pv',
                'CSP_int (dry_hybrid)','CSP_int (recirculating)',
                'PV_int',
                'CSP_peak (dry_hybrid)','CSP_peak (recirculating)',
                'PV_peak',
                'CSP_subpeak (dry_hybrid)', 'CSP_subpeak (recirculating)',
                'PV_subpeak',
                'battery'
                ]


#data
model_year=np.arange(2020,2055,5)
scenario={}

# this is used for data simulation
for i in range(1,case_number+1):
    data=pd.DataFrame({
        '2020': [random.uniform(0, 1) for j in range(len(itc_technology))],
        '2025': [random.uniform(0, 1) for j in range(len(itc_technology))],
        '2030': [random.uniform(0, 1) for j in range(len(itc_technology))],
        '2035': [random.uniform(0, 1) for j in range(len(itc_technology))],
        '2040': [random.uniform(0, 1) for j in range(len(itc_technology))],
        '2050': [random.uniform(0, 1) for j in range(len(itc_technology))],
        },
        index=itc_technology)

    scenario.update({'case_'+str(i):data})

#for pth in pathGen(share_path + itc_path):
#    print(pth)

itc_function(itc_path,itc_output_path,itc_technology,case_number,case_id, scenario, stop_year)

       
#%% ptc file
from input_function import ptc_function

ptc_path = share_path + 'policy_base/empty_base.xml'
ptc_output_path=share_path+'policy_change/ptc_change'

ptc_technology=['biomass (conv) (cooling pond)', 'biomass (conv) (dry cooling)','biomass (conv) (once through)',
                'biomass (conv) (recirculating)','biomass (conv) (seawater)', 'biomass (IGCC) (dry cooling)',
                'biomass (IGCC) (once through)', 'biomass (IGCC) (recirculating)', 'biomass (IGCC) (seawater)',
                'CSP_base_storage',
                'geothermal (dry_hybrid)','geothermal (recirculating)',
                'Gen_II_LWR (cooling pond)','Gen_II_LWR (once through)','Gen_II_LWR (recirculating)','Gen_II_LWR (seawater)',
                'Gen_III (cooling pond)','Gen_III (once through)','Gen_III (recirculating)','Gen_III (seawater)',
                'PV_base_storage',
                'wind_base_storage',
                'CSP_int (dry_hybrid)','CSP_int (recirculating)',
                'CSP_peak (dry_hybrid)', 'CSP_peak (recirculating)',
                'CSP_subpeak (dry_hybrid)', 'CSP_subpeak (recirculating)',
                'PV_int', 'PV_peak', 'PV_subpeak',
                'wind_base', 'wind_int', 'wind_subpeak'
                ]
     

#data
scenario_ptc={}

# this is used for data simulation
for i in range(1,case_number+1):
    data_ptc=pd.DataFrame({
        '2020': [random.uniform(-1, 0) for j in range(len(ptc_technology))],
        '2025': [random.uniform(-1, 0) for j in range(len(ptc_technology))],
        '2030': [random.uniform(-1, 0) for j in range(len(ptc_technology))],
        '2035': [random.uniform(-1, 0) for j in range(len(ptc_technology))],
        '2040': [random.uniform(-1, 0) for j in range(len(ptc_technology))],
        '2050': [random.uniform(-1, 0) for j in range(len(ptc_technology))],
        },
        index=ptc_technology)

    scenario_ptc.update({'case_'+str(i):data_ptc})

ptc_function(ptc_path,ptc_output_path,ptc_technology,case_number,case_id, scenario_ptc, stop_year)

#%%bus
from input_function import EV_bus_function

bus_path = share_path + 'policy_base/transport_base.xml'
bus_output_path=share_path+'policy_change/bus_change'

bus_technology={'supplysector': 'trn_pass_road', 
                'tranSubsector': 'Bus',
                'stub-technology':'BEV'}
     

#data
scenario_bus={}

# this is used for data simulation
for i in range(1,case_number+1):
    data_bus=pd.DataFrame({
        '2020': [random.uniform(-1, 0) for j in range(len(bus_technology))],
        '2025': [random.uniform(-1, 0) for j in range(len(bus_technology))],
        '2030': [random.uniform(-1, 0) for j in range(len(bus_technology))],
        '2035': [random.uniform(-1, 0) for j in range(len(bus_technology))],
        '2040': [random.uniform(-1, 0) for j in range(len(bus_technology))],
        '2050': [random.uniform(-1, 0) for j in range(len(bus_technology))],
        },
        index=bus_technology)

    scenario_bus.update({'case_'+str(i):data_bus})


    
#%%    
    
    
    