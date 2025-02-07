#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 13:11:51 2025

@author: hy4174
"""


import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
import random
import os

# set path here
os.chdir('/Users/hy4174/Documents/GitHub/GCAM_USA')


def pathGen(fn):
    path = []
    it = ET.iterparse(fn, events=('start', 'end'))
    for evt, el in it:
        if evt == 'start':
            path.append(el.tag)
            yield '/'.join(path)
        else:
            path.pop()

#set your GCAM path here            
share_path='/Users/hy4174/Documents/gcam-v6.0/input/' 


#%% case and stop year


stop_year=2050

#%%change file

from input_function import share_function, share_en_function, share_h2_function, bio_constraint_function, constraint_en_function

# output file path

share_share_path=share_path + 'policy_base/share_USA_base.xml'
share_output_path=share_path+'policy_change/'


output_name = "elec_wo_CCS.xml"
share_function(share_share_path,share_output_path, output_name, stop_year)


share_en_path=share_path + 'policy_base/en_transformation_share_base.xml'
share_en_output_path=share_path+'policy_change/'
output_en_name = "en_transformation_wo_CCS.xml"
share_en_function(share_en_path,share_en_output_path, output_en_name, stop_year)

share_h2_path=share_path + 'policy_base/H2_share_base.xml'
share_h2_output_path=share_path+'policy_change/'
output_h2_name = "H2_wo_CCS.xml"
share_h2_function(share_h2_path,share_h2_output_path, output_h2_name, stop_year)
# biomass constraint
bio_path=share_path + 'policy_base/regional_biomass_constraint.xml'
bio_output_path=share_path+'policy_change/'
output_bio_name = "regional_biomass_constraint.xml"
bio_constraint_function(bio_path,bio_output_path, output_bio_name, stop_year)

#constraint biomass liquid
share_en_path=share_path + 'gcamdata/xml/en_transformation_USA.xml'
share_en_output_path=share_path+'policy_change/'
output_en_name = "en_transformation_wo_CCS.xml"
constraint_en_function(share_en_path,share_en_output_path, output_en_name, stop_year)


#%% constraint Power CO2
from input_function import power_constraint_function


share_power_path=share_path + 'policy_base/constraint_base.xml'
share_output_path=share_path+'policy_change/'


output_name = "constraint_power.xml"
power_constraint_function(share_power_path,share_output_path, output_name, stop_year)

share_power_path=share_path + 'policy_base/constraint_all_base.xml'
output_name = "constraint_all_power.xml"
power_constraint_function(share_power_path,share_output_path, output_name, stop_year)

output_name = "constraint_power.xml"
share_power_path=share_path + 'policy_base/power_constraint_base.xml'
share_output_path=share_path+'policy_change/'

#%%
from input_function import ghg_link_function

link_input_path ='/Users/hy4174/Documents/gcam-v6.0/input/policy/paper2/GHG_link_energy_CO2_LUCdonly_alltimes_introduceCCS.xml'
link_output_path ='/Users/hy4174/Documents/gcam-v6.0/input/policy/paper2/'
output_link_name = "GHG_link_energy_power.xml"


