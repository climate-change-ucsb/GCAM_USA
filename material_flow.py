#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 13:40:00 2024

@author: haozheyang
"""

import pandas as pd

path='/Users/haozheyang/Documents/GCAM/material trade/'

module_code={'pv cell': {'q_name' : 'Second Unit of Quantity'},
             'wind blade and hub': {'q_name' : 'First Unit of Quantity'},
             'EV battery':{'q_name' : 'Second Unit of Quantity'},
             'permanent magnet':{'q_name': 'Second Unit of Quantity'}}

module_unit={'pv cell': 'W',
             'wind blade and hub': 'kg',
             'EV battery': 'kg',
             'permanent magnet': 'kg'
    }



material_code={
    'iron and steel': {'code': [7206, 7207,7208,7209,7210,7213,7216,7218,7219,7222], 'conversion': 1},
    'aluminium':{'code': [7601,7602, 7604], 'conversion': 1},
    'nickel': {'code': [7502], 'conversion':1},
    'lithium':{'code': False, 'conversion': 14/(14+60)},
    'copper': {'code': [7403], 'conversion': 1},
    'cobalt': {'code': False, 'conversion':1},
    'silicon':{'code': [2804.69], 'conversion':1},
    'natural graphite':{'code': False, 'conversion':1},
    }

#raw_list = ['iron ore', 'steel scrap']

raw_code = {
            'bauxite': {'code':[2606], 'conversion': 0.25, 'q_name' : 'First Unit of Quantity'}, #convert Al2O3 to Al
            'alumina': {'code':[2818], 'conversion': 0.5, 'q_name' : 'First Unit of Quantity'},
            'aluminum scrap': {'code':[7602],'conversion': 1, 'q_name' : 'First Unit of Quantity'},   
            'iron ore': {'code':[2601],'conversion': 1, 'q_name' : 'First Unit of Quantity'},      #keep using FexOy
            'steel scrap': {'code': [7204], 'conversion': 1, 'q_name' : 'First Unit of Quantity'},
            'nickel ore': {'code': [2604],'conversion': 1, 'q_name' : 'First Unit of Quantity'}, #source data is content value
            'nickel scrap': {'code':[7503],'conversion': 1, 'q_name' : 'First Unit of Quantity'},
            'cobalt ore' : {'code':[2605],'conversion': 1, 'q_name' : 'Second Unit of Quantity'}, #use second unit
            'cobalt scrap': {'code': [8105],'conversion': 1, 'q_name' : 'First Unit of Quantity'},
            }
# we focus on the processed material, which is the product of ore, not the ore. Except for rare earth elements

#choose_year = 2022 

#option =1 #use resource earth data
#option =2 #use US commission trade data
#%% trade of module
US_import_module = pd.DataFrame()
for module_item in module_code:
    Custom_value = pd.read_excel(path + module_item + '.xlsx',sheet_name='Customs Value',skiprows=2).groupby(['Country'])['Year 2022'].sum().sort_index()
    Custom_value = Custom_value.rename('Value')
    Quantity = pd.read_excel(path + module_item + '.xlsx',sheet_name=module_code[module_item]['q_name'],skiprows=2).groupby(['Country'])['Year 2022'].sum().sort_index()
    Quantity = Quantity.rename('Quantity')
    Tax = pd.read_excel(path + module_item  + '.xlsx',sheet_name='Calculated Duties',skiprows=2).groupby(['Country'])['Year 2022'].sum().sort_index()
    Tax = Tax.rename('Tax')
    Charge = pd.read_excel(path + module_item  + '.xlsx',sheet_name='Import Charges',skiprows=2).groupby(['Country'])['Year 2022'].sum().sort_index()
    Charge = Charge.rename('Charge')

    trade_module = pd.concat([Custom_value, Quantity, Tax, Charge], join = 'outer',axis=1).reset_index()
    trade_module['module'] = module_item
    trade_module['export_share'] = trade_module.Quantity/trade_module.Quantity.sum()
    US_import_module = US_import_module.append(trade_module)
    print(module_item, trade_module .Value.sum() / trade_module .Quantity.sum())  
    
US_import_module['price'] = US_import_module['Value']/US_import_module['Quantity']
US_import_module['charge_rate'] = US_import_module['Charge']/US_import_module['Value']
US_import_module['tax_rate'] = US_import_module['Tax']/US_import_module['Value']    


'''
if option == 1:
    for material_item in material_list:
        data = pd.read_excel(path+'/resourth_earth/' + material_item + '.xlsx',sheet_name='Exporters')
        exporter = data.groupby(['Exporter','Year','Resource'])[['Value (1000USD)', 'Weight (1000kg)']].sum().reset_index()
        if material_item == 'iron and steel':
            exporter_ore = pd.read_excel(path + 'iron ores and concentrates' + '.xlsx',sheet_name='Exporters').groupby(['Exporter','Year','Resource'])[['Value (1000USD)', 'Weight (1000kg)']].sum()
            exporter_scrap = pd.read_excel(path + 'iron and steel scrap' + '.xlsx',sheet_name='Exporters').groupby(['Exporter','Year','Resource'])[['Value (1000USD)', 'Weight (1000kg)']].sum()
            exporter_material=exporter_ore.merge(exporter_scrap,how='left',on=['Exporter','Year']).fillna(0)
            exporter=exporter.merge(exporter_material,how='left',on=['Exporter','Year']).fillna(0)
            exporter['Value (1000USD)']=exporter['Value (1000USD)'] - exporter['Value (1000USD)_x'] - exporter['Value (1000USD)_y']
            exporter['Weight (1000kg)']=exporter['Weight (1000kg)'] - exporter['Weight (1000kg)_x'] - exporter['Weight (1000kg)_y']
        if material_item == 'aluminum':
            exporter_material = pd.read_excel(path + 'alumina' + '.xlsx',sheet_name='Exporters').groupby(['Exporter','Year','Resource'])[['Value (1000USD)', 'Weight (1000kg)']].sum()
            exporter=exporter.merge(exporter_material,how='left',on=['Exporter','Year']).fillna(0)
            exporter['Value (1000USD)']=exporter['Value (1000USD)_x'] - exporter['Value (1000USD)_y'] 
            exporter['Weight (1000kg)']=exporter['Weight (1000kg)_x'] - exporter['Weight (1000kg)_y'] 
            
        if material_item == 'nickel':
            exporter_fe_nickel= pd.read_excel(path + 'ferro-nickel' + '.xlsx',sheet_name='Exporters').groupby(['Exporter','Year','Resource'])[['Value (1000USD)', 'Weight (1000kg)']].sum()
            exporter=exporter.merge(exporter_fe_nickel,how='left',on=['Exporter','Year']).fillna(0)
            exporter['Value (1000USD)']=exporter['Value (1000USD)_x'] - exporter['Value (1000USD)_y']
            exporter['Weight (1000kg)']=exporter['Weight (1000kg)_x'] - exporter['Weight (1000kg)_y']
        
        US_import =  US_import.append(exporter[['Exporter','Year','Resource','Value (1000USD)','Weight (1000kg)']])
   
    US_import  =  US_import .loc[ US_import .Year==choose_year,]   

    US_import_value = US_import.pivot(index='Exporter',columns='Resource',values='Value (1000USD)').fillna(0)
    US_import_weight = US_import.pivot(index='Exporter',columns='Resource',values='Weight (1000kg)').fillna(0)
    US_import_price = US_import_value/US_import_weight
    US_import_price = US_import_price.fillna(0)
    US_import_share = US_import_weight/US_import_weight.sum()
    
    US_total_import_weight = US_import_weight.sum()
    print(US_total_import_weight) #tonne
'''

#%% trade of material
US_import_material=pd.DataFrame()
for material_item in material_code:
    Custom_value = pd.read_excel(path + material_item + '.xlsx',sheet_name='Customs Value',skiprows=2).groupby(['Country', 'HTS Number','Quantity Description'])['Year 2022'].sum().sort_index()
    Custom_value = Custom_value.rename('Value')
    Quantity = pd.read_excel(path + material_item + '.xlsx',sheet_name='First Unit of Quantity',skiprows=2).groupby(['Country','HTS Number','Quantity Description'])['Year 2022'].sum().sort_index()
    Quantity = Quantity.rename('Quantity')
    Quantity = Quantity * material_code[material_item]['conversion']
    Tax = pd.read_excel(path + material_item + '.xlsx',sheet_name='Calculated Duties',skiprows=2).groupby(['Country', 'HTS Number','Quantity Description'])['Year 2022'].sum().sort_index()
    Tax = Tax.rename('Tax')
    Charge = pd.read_excel(path + material_item + '.xlsx',sheet_name='Import Charges',skiprows=2).groupby(['Country', 'HTS Number','Quantity Description'])['Year 2022'].sum().sort_index()
    Charge = Charge.rename('Charge')
    
    trade_material = pd.concat([Custom_value, Quantity, Tax, Charge], join = 'outer',axis=1).reset_index()
    
    #keep hts code we need
    if material_code[material_item]['code'] :
         trade_material  =  trade_material.loc[trade_material ['HTS Number'].isin(material_code[material_item]['code']),:]
    
    trade_material = trade_material.loc[ trade_material ['Quantity Description'] !='number',:]
    trade_material.loc[ trade_material ['Quantity Description'] == 'metric tons','Quantity'] = \
    trade_material.loc[ trade_material ['Quantity Description'] == 'metric tons','Quantity'] *1000
    trade_material.loc[trade_material ['Quantity Description'] == 'metric tons','Quantity Description'] = 'kilograms'
    
    trade_material  = trade_material.groupby('Country')[['Value','Quantity','Tax','Charge']].sum().reset_index()
    
    trade_material['material'] = material_item
    trade_material['export_share'] = trade_material.Quantity/trade_material.Quantity.sum()
    
    print(material_item, trade_material .Quantity.sum()/1000)  
    
    US_import_material = US_import_material.append(trade_material )
   
US_import_material['price'] = US_import_material['Value']/US_import_material['Quantity']
US_import_material['charge_rate'] = US_import_material['Charge']/US_import_material['Value']
US_import_material['tax_rate'] = US_import_material['Tax']/US_import_material['Value']  

check= US_import_material.groupby('material')[['Value','Quantity']].sum()
print (check.Value / check.Quantity)

#%% trade of ores and scrap


US_import_raw = pd.DataFrame()
for raw_item in raw_code:
        Custom_value = pd.read_excel(path + 'ores and scrap.xlsx',sheet_name='Customs Value',skiprows=2).groupby(['Country','HTS Number', 'Quantity Description'])['Year 2022'].sum().sort_index()
        Custom_value = Custom_value.rename('Value')

        Quantity = pd.read_excel(path +  'ores and scrap.xlsx',sheet_name=raw_code[raw_item]['q_name'],skiprows=2).groupby(['Country', 'HTS Number', 'Quantity Description'])['Year 2022'].sum().sort_index()
        Quantity = Quantity.rename('Quantity')
        Quantity = Quantity * raw_code[raw_item]['conversion']
         
        Tax = pd.read_excel(path + 'ores and scrap.xlsx',sheet_name='Calculated Duties',skiprows=2).groupby(['Country', 'HTS Number','Quantity Description'])['Year 2022'].sum().sort_index()
        Tax = Tax.rename('Tax')
        Charge = pd.read_excel(path + 'ores and scrap.xlsx',sheet_name='Import Charges',skiprows=2).groupby(['Country', 'HTS Number','Quantity Description'])['Year 2022'].sum().sort_index()
        Charge = Charge.rename('Charge')
        
        trade_raw = pd.concat([Custom_value, Tax, Charge], join = 'outer',axis=1).reset_index()
        trade_raw =trade_raw.merge(Quantity, how = 'right', on = ['Country', 'HTS Number'])
        
        hts_6=trade_raw['HTS Number'].astype(str)
        trade_raw['HTS_4'] = hts_6.str.split('.').str[0].astype(int)
        trade_raw = trade_raw.groupby(['Country','HTS_4', 'Quantity Description'])[['Value','Quantity','Tax','Charge']].sum().reset_index()

        trade_raw.loc[trade_raw ['Quantity Description'] == 'metric tons','Quantity'] = \
            trade_raw.loc[trade_raw['Quantity Description'] == 'metric tons','Quantity'] *1000
        trade_raw.loc[trade_raw ['Quantity Description'] == 'metric tons','Quantity Description'] = 'kilograms'
        trade_raw.loc[trade_raw ['Quantity Description'] == 'component kilograms','Quantity Description'] = 'kilograms'
        
        trade_raw = trade_raw.loc[trade_raw['HTS_4'].isin(raw_code[raw_item]['code']),:]
        trade_raw['raw'] = raw_item
        trade_raw['export_share'] = trade_raw.Quantity/trade_raw.Quantity.sum()
        
        print(raw_item, trade_raw .Quantity.sum()/1000)
        
        US_import_raw = US_import_raw.append(trade_raw[['Country','Value','Quantity','Tax','Charge','raw','export_share']])

US_import_raw['price'] = US_import_raw['Value']/US_import_raw['Quantity']
US_import_raw['charge_rate'] = US_import_raw['Charge']/US_import_raw['Value']
US_import_raw['tax_rate'] = US_import_raw['Tax']/US_import_raw['Value']
US_import_raw = US_import_raw.fillna(0)
    
check_raw= US_import_raw.groupby('raw')[['Value','Quantity']].sum()
print (check_raw.Value / check_raw.Quantity)
#%%
path_base='/Users/haozheyang/Documents/GCAM/'

domestic_module = pd.read_excel(path_base + 'cost_category.xlsx',sheet_name = 'domestic_module_share')
US_import_module = US_import_module.merge(domestic_module, how='left', on = 'module')
US_import_module.export_share = US_import_module.export_share * (1-US_import_module.domestic_module_share)

#USGS_import_domestic
domestic_material = pd.read_excel(path_base + 'cost_category.xlsx',sheet_name = 'domestic_material_share')[['material','domestic_material_share','domestic_material_price']]
US_import_material = US_import_material.merge(domestic_material, how='left', on = 'material')
US_import_material.export_share = US_import_material.export_share * (1-US_import_material.domestic_material_share)

#ore and scrap share
domestic_raw = pd.read_excel(path_base + 'cost_category.xlsx',sheet_name = 'domestic_raw_share')
US_import_raw = US_import_raw.merge(domestic_raw, how = 'left', on= 'raw')
US_import_raw.export_share = US_import_raw.export_share * (1-US_import_raw.domestic_raw_share)

#%%
module = pd.read_excel(path_base + 'cost_category.xlsx',sheet_name = 'module_requirement')
material = pd.read_excel(path_base + 'cost_category.xlsx',sheet_name = 'material_requirement')
raw = pd.read_excel(path_base + 'cost_category.xlsx',sheet_name = 'raw_requirement')

material_co2 = pd.read_excel(path_base + 'cost_category.xlsx',sheet_name = 'co2_material')
raw_co2 = pd.read_excel(path_base + 'cost_category.xlsx',sheet_name = 'co2_raw')

US_import_material = US_import_material.merge(material_co2, how ='left', on='material')
US_import_raw = US_import_raw.merge(raw_co2, how ='left', on='raw')

technology=['PV', 'Onshore wind', 'EV']

change=pd.DataFrame()

for tech in technology:
    module_tech = module[['module',tech]]
    module_tech_requirement = US_import_module.merge(module_tech, how='left', on ='module')
    
    material_tech = material[['material',tech]].fillna(0)
    material_tech_requirement = US_import_material.merge(material_tech, how= 'left', on='material')

    raw_tech = raw[['raw','material',tech]].merge(domestic_material, how ='left', on = 'material').fillna(0)
    raw_tech['raw_domestic_consumption'] = raw_tech[tech] * raw_tech.domestic_material_share
    raw_tech_requirement = US_import_raw.merge(raw_tech[['raw',tech,'raw_domestic_consumption']], how = 'left', on ='raw')
       
    if tech == 'PV':
        module_tech_requirement['Tariff']=0.5
    else:
        module_tech_requirement['Tariff']=0.25
                                
    material_tech_requirement['Tariff']=0.25
    raw_tech_requirement['Tariff']=0.25
    
    material_tech_requirement['CBAM']=0.055
    raw_tech_requirement['CBAM']=0.055

    other_cost = pd.read_excel(path_base + 'cost_category.xlsx',sheet_name = 'Other cost', index_col=0).loc[tech,'Other cost']
    
    # module
    module_tech_requirement['trade'] = module_tech_requirement.export_share \
                                 * module_tech_requirement.price \
                                 * (1+module_tech_requirement.charge_rate) \
                                 * (1+module_tech_requirement.tax_rate) \
                                 * module_tech_requirement[tech]
    
    module_tech = module_tech.merge(domestic_module)
    module_tech['domestic'] = module_tech[tech] * module_tech.domestic_module_share * module_tech.domestic_module_price   
         
    #matterial      
    material_tech_requirement['trade'] = material_tech_requirement.export_share \
                                 * material_tech_requirement.price \
                                 * (1 + material_tech_requirement.charge_rate) \
                                 * (1 + material_tech_requirement.tax_rate)\
                                 * material_tech_requirement[tech]
                            
    material_tech = material_tech.merge(domestic_material)
    material_tech['domestic'] = material_tech[tech] * material_tech.domestic_material_share * material_tech.domestic_material_price
    
    #raw
    raw_tech_requirement['trade'] = raw_tech_requirement.export_share \
                                 * raw_tech_requirement.price \
                                 * (1 + raw_tech_requirement.charge_rate) \
                                 * (1 + raw_tech_requirement.tax_rate)\
                                 * raw_tech_requirement['raw_domestic_consumption']
                            
    raw_tech = raw_tech[['raw',tech,'raw_domestic_consumption']].merge(domestic_raw)
    raw_tech['domestic'] = raw_tech['raw_domestic_consumption'] * raw_tech.domestic_raw_share * raw_tech.domestic_raw_price
    
    #BAU cost
    BAU_cost = sum(module_tech.domestic) + sum(module_tech_requirement.trade) + other_cost
  
    module_onshore = module_tech.groupby('module')['domestic'].sum() + module_tech_requirement[['module','trade']].groupby('module')['trade'].sum() 
    module_onshore = module_onshore.reset_index()
    module_onshore = module_onshore.rename (columns = {0: 'Trade'})
    
    module_tech['Onshore'] = module_tech[tech] * module_tech.domestic_module_price
    module_onshore = module_onshore.merge(module_tech, how='left', on = 'module')
    module_onshore['Onshore_change'] = module_onshore.Onshore - module_onshore.Trade
    module_onshore.loc[module_onshore.domestic_module_share ==0 , 'Onshore_change'] =0
    module_onshore.loc[module_onshore.domestic_module_share ==0, 'Onshore'] = module_onshore.loc[module_onshore.domestic_module_share ==0, 'Trade']
    module_onshore = module_onshore[['module','Onshore','Trade','Onshore_change']].set_index('module')
    
    material_onshore =  material_tech.groupby('material')['domestic'].sum() + material_tech_requirement.groupby('material')['trade'].sum()
    material_onshore = material_onshore.reset_index()
    material_onshore = material_onshore.rename (columns = {0: 'Trade'})
    
    material_tech['Onshore'] = material_tech[tech] * material_tech.domestic_material_price 
    material_tech.loc[material_tech.domestic_material_share ==0, 'Onshore'] =  material_onshore.loc[material_tech.domestic_material_share ==0, 'Trade']
    material_onshore = material_onshore.merge(material_tech, how='left', on = 'material')
    material_onshore['Onshore_change'] = material_onshore.Onshore - material_onshore.Trade
    material_onshore.loc[material_onshore.domestic_material_share ==0 , 'Onshore_change'] =0
    material_onshore.loc[material_onshore.domestic_material_share ==0, 'Onshore'] = material_onshore.loc[material_onshore.domestic_material_share ==0, 'Trade']
    material_onshore = material_onshore[['material','Onshore','Trade','Onshore_change']]
    material_onshore = material_onshore.set_index('material')
    
    raw_onshore =  raw_tech.groupby('raw')['domestic'].sum() + raw_tech_requirement.groupby('raw')['trade'].sum()
    raw_onshore = raw_onshore.reset_index()
    raw_onshore = raw_onshore.rename (columns = {0: 'Trade'}).set_index('raw')
    
    raw_tech['Onshore'] = raw_tech[tech] * raw_tech.domestic_raw_price 
    raw_onshore = raw_onshore.merge(raw_tech, how='left', on = 'raw')
    raw_onshore['Onshore_change'] = raw_onshore.Onshore - raw_onshore.Trade
    raw_onshore.loc[raw_onshore.domestic_raw_share ==0 , 'Onshore_change'] =0
    raw_onshore.loc[raw_onshore.domestic_raw_share ==0, 'Onshore'] = raw_onshore.loc[raw_onshore.domestic_raw_share ==0, 'Trade']
    raw_onshore = raw_onshore[['raw','Onshore','Trade','Onshore_change']]
    raw_onshore = raw_onshore.set_index('raw')
    
    Onshore = sum(module_onshore.Onshore_change) + BAU_cost
    
    Onshore_all = Onshore \
                + sum(material_onshore.Onshore_change)\
                + sum(raw_onshore.Onshore_change)
    
    
    #Tariff
    module_tech_requirement['module_tariff'] = module_tech_requirement.export_share \
                                 * module_tech_requirement.price\
                                 * module_tech_requirement.Tariff\
                                 * module_tech_requirement[tech]
                                 
    material_tech_requirement['material_tariff'] = material_tech_requirement.export_share \
                                 * material_tech_requirement.price \
                                 * material_tech_requirement.Tariff \
                                 * material_tech_requirement[tech]
    
    raw_tech_requirement['raw_tariff'] = raw_tech_requirement.export_share \
                                 * raw_tech_requirement.price \
                                 * raw_tech_requirement.Tariff \
                                 * raw_tech_requirement['raw_domestic_consumption']                                 
    
    tariff = sum(module_tech.domestic) + sum(module_tech_requirement.trade) + other_cost\
             + sum(module_tech_requirement.module_tariff)\
             + sum(material_tech_requirement.material_tariff)\
             + sum(raw_tech_requirement.raw_tariff) \

             
    module_tariff = module_tech_requirement[['module','module_tariff']].groupby('module')['module_tariff'].sum() 

    material_tariff = material_tech_requirement[['material','material_tariff']].groupby('material')['material_tariff'].sum().reset_index()  
    material_tariff['policy'] = 'Tariff'
    material_tariff = material_tariff.set_index('material')
    
    raw_tariff = raw_tech_requirement[['raw','raw_tariff']].groupby('raw')['raw_tariff'].sum().reset_index()  
    raw_tariff['policy'] = 'Tariff'
    raw_tariff = raw_tariff.set_index('raw')
    
    #CBAM
    material_tech_requirement['material_cbam'] = material_tech_requirement.export_share \
                                 * material_tech_requirement.price \
                                 * material_tech_requirement.CBAM \
                                 * material_tech_requirement[tech]
    
    raw_tech_requirement['raw_cbam'] = raw_tech_requirement.export_share \
                                 * raw_tech_requirement.price \
                                 * raw_tech_requirement.CBAM \
                                 * raw_tech_requirement['raw_domestic_consumption']                                 
    
    cbam = sum(module_tech.domestic) + sum(module_tech_requirement.trade) + other_cost\
             + sum(material_tech_requirement.material_cbam)\
             + sum(raw_tech_requirement.raw_cbam) \
     
    material_cbam = material_tech_requirement[['material','material_cbam']].groupby('material')['material_cbam'].sum().reset_index()  
    material_cbam = material_cbam.set_index('material')
    
    raw_cbam = raw_tech_requirement[['raw','raw_cbam']].groupby('raw')['raw_cbam'].sum().reset_index()  
    raw_cbam = raw_cbam.set_index('raw')
    
    #
    decompose=pd.DataFrame({
        'Module': [module_onshore.Onshore_change.sum() , module_tariff.sum(), 0]
        },
        index=  ['Onshore', 'Tariff', 'CBAM'],
        )
    
    material_change = material_onshore.T.append(material_tariff.T)
    material_change = material_change.append(material_cbam.T)
    material_change= material_change.loc[['Onshore_change', 'material_tariff','material_cbam'],:] 
    material_change.index = ['Onshore', 'Tariff','CBAM']
    
    raw_change= raw_onshore.T.append(raw_tariff.T)
    raw_change = raw_change.append(raw_cbam.T)
    raw_change= raw_change.loc[['Onshore_change', 'raw_tariff', 'raw_cbam'],:] 
    raw_change.index = ['Onshore', 'Tariff', 'CBAM']
    
    
    decompose = pd.concat([decompose, material_change, raw_change], axis=1)/BAU_cost
    decompose['total'] = decompose.sum(axis=1)
    decompose['technology'] =tech
    
    change = change.append(decompose)
    
    print({tech:[BAU_cost, Onshore, Onshore_all,tariff]})



