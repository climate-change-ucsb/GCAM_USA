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
case_id=['Tariff_short','Tariff_long','Tariff_current','Tariff_shock']
case_number=len(case_id)
#%%
from input_function import itc_function, capital_function

# itc output file path
itc_path=share_path + 'policy_base/itc_base.xml'
itc_output_path=share_path+'policy_change/itc_change_'

capital_path=share_path + 'policy_base/cost_base.xml'
capital_output_path=share_path+'policy_change/capital_change_'

#technology you want to include
itc_technology=[  
                'PV_int',
                'PV_peak',
                'PV_subpeak',
                'rooftop_pv', 
                'PV_base_storage',
                'wind_base',
                'wind_base_storage',
                'wind_base_offshore',  
                #'battery'
                ]
capital_technology = itc_technology

#relative cost change 
# the cost change here corresponds to technology in itc_technology
'''
cost={
      'US':[1.06, 1.06, 1.06, 1.03],
      'Tariff': [1.09, 1.09, 1.09, 1.05],
      'Freer':  [0.9,  0.9,  0.9,  0.95],
      'China': [0.88, 0.88,  0.88, 0.94]
      }
'''
#data
cost = {}
for case in case_id:
    cost [case]= pd.read_excel('technology.xlsx', sheet_name = case, index_col=0)

model_year=np.arange(2020,2055,5)

scenario={}

# this is used for data simulation
for i in case_id:
    technology = cost[i].columns
    data=pd.DataFrame({
        '2020': cost[i].loc[2020,technology],
        '2025': cost[i].loc[2025,technology],
        '2030': cost[i].loc[2030,technology],
        '2035': cost[i].loc[2035,technology],
        '2040': cost[i].loc[2040,technology],
        '2045': cost[i].loc[2045,technology],
        '2050': cost[i].loc[2050,technology]
        },
        index=technology)

    scenario.update({str(i):data})

#for pth in pathGen(share_path + itc_path):
#    print(pth)

#itc_function(itc_path,itc_output_path,itc_technology,case_number,case_id, scenario, stop_year)
capital_function(capital_path,capital_output_path,case_number,case_id, scenario, stop_year)


#%%car


from input_function import car_function

car_path = share_path + 'policy_base/transport_base.xml'
car_output_path=share_path+'policy_change/car_change_'

car_technology={'supplysector': 'trn_pass_road_LDV_4W', 
                'tranSubsector': 'Car',
                'stub-technology':'BEV'}



# relative change in the non-energy input for car
pct=0.094
pct3=-0.29

base_cost =[0.2668,
            0.2456,
          0.2243,
          0.2243,
          0.2243,
          0.2243,
          0.2243]

cost_car = {}
for case in case_id:
    cost_car[case]=cost[case][['EV']] 
    cost_car[case]['EV'] = (cost_car[case]['EV'] -1)* base_cost
    
        
'''   
cost_car={'Subsidy': {   '2020': [0.2668*pct],
                    '2025': [0.2456*pct],
                    '2030': [0.2243*pct],
                    '2035': [0.2243*pct],
                    '2040': [0.2243*pct],
                    '2045': [0.2243*pct],
                    '2050': [0.2243*pct],
                    },
          'Tariff': {'2020': [0.2668*pct],
                     '2025': [0.2456*pct],
                     '2030': [0.2243*pct],
                     '2035': [0.2243*pct],
                     '2040': [0.2243*pct],
                     '2045': [0.2243*pct],
                     '2050': [0.2243*pct]
                     },
          'Free': {'2020': [0.2668*pct3],
                     '2025': [0.2456*pct3],
                     '2030': [0.2243*pct3],
                     '2035': [0.2243*pct3],
                     '2040': [0.2243*pct3],
                     '2045': [0.2243*pct3],
                     '2050': [0.2243*pct3]
                     }
          }

'''

#data
scenario_car={}

# this is used for data simulation
for i in case_id:
    data_car=pd.DataFrame(
        {
        '2020': cost_car[i].loc[2020],
        '2025': cost_car[i].loc[2025],
        '2030': cost_car[i].loc[2030],
        '2035': cost_car[i].loc[2035],
        '2040': cost_car[i].loc[2040],
        '2045': cost_car[i].loc[2045],
        '2050': cost_car[i].loc[2050]
        }
        )

    scenario_car.update({str(i):data_car})

car_function(car_path,car_output_path,car_technology,case_number,case_id, scenario_car, stop_year)


large_car_output_path=share_path+'policy_change/largecar_change_'

large_car_technology={'supplysector': 'trn_pass_road_LDV_4W', 
                'tranSubsector': 'Large Car and Truck',
                'stub-technology':'BEV'}

base_cost_large =[0.4032,
                0.3718,
                0.3404,
                0.3404,
                0.3404,
                0.3404,
                0.3404]

cost_car_large = {}
for case in case_id:
    cost_car_large[case]=cost[case][['EV']] 
    cost_car_large[case]['EV'] = (cost_car_large[case]['EV'] -1)* base_cost_large
    
    
#data
scenario_large_car={}

# this is used for data simulation
for i in case_id:
    data_large_car=pd.DataFrame({
        '2020': cost_car_large[i].loc[2020],
        '2025': cost_car_large[i].loc[2025],
        '2030': cost_car_large[i].loc[2030],
        '2035': cost_car_large[i].loc[2035],
        '2040': cost_car_large[i].loc[2040],
        '2045': cost_car_large[i].loc[2045],
        '2050': cost_car_large[i].loc[2050]
        }
        )

    scenario_large_car.update({str(i):data_large_car})

car_function(car_path,large_car_output_path,large_car_technology,case_number,case_id, scenario_large_car, stop_year)

    
#%%    
    
    
    