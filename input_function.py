#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 20:22:46 2024

@author: haozheyang
"""
import xml.etree.ElementTree as ET
import numpy as np

def capital_function(capital_path,capital_output_path,case_number,case_id, scenario, stop_year):

    for case in range(1,case_number+1):
        scenario_id = case_id[case-1]
        
        capital_technology = scenario[scenario_id].index
        
        tree_capital = ET.parse(capital_path)
        root_capital = tree_capital.getroot()
        
        for parent in root_capital.findall('.//location-info/..'):
            for technology_parent in parent.findall('location-info'):
                all_tech=[]
                for technology in technology_parent.findall('.//period/..'):
                    #print(technology.attrib)
                    tech_name = technology.attrib['name'] 
                    all_tech.append(tech_name)    
                    
                    if tech_name in capital_technology:
                        for period in technology.findall("period"): 
                            year=period.get('year')
                            if int(year)>stop_year:
                                technology.remove(period)
                            else:
                                for capital_overnight in period.findall('input-capital/capital-overnight'):
                                #charge_rate = period.find('input-capital/fixed-charge-rate')
                                #new_charge_rate = float(period.find('input-capital/fixed-charge-rate').text) * scenario[scenario_id].loc[tech_name,str(year)]
                                #charge_rate.text=str(new_charge_rate)
                                    print(capital_overnight.text)
                                    new_capital_overnight = float(capital_overnight.text) * scenario[scenario_id].loc[tech_name,str(year)]
                                    capital_overnight.text=str(new_capital_overnight)
                                    print(year,capital_overnight.text)
                    else:
                        technology_parent.remove(technology)
                        
                if not any(tech_tmp in capital_technology for tech_tmp in all_tech):
                    parent.remove(technology_parent)
                        
        tree_capital.write(capital_output_path + scenario_id+".xml",encoding="UTF-8",xml_declaration=True) 
        
def itc_function(itc_path,itc_output_path,itc_technology,case_number,case_id, scenario, stop_year):
    
    for case in range(1,case_number+1):
        tree_itc = ET.parse(itc_path)
        root_itc = tree_itc.getroot()
        scenario_id = case_id[case-1]
        for parent in root_itc.findall('.//location-info/..'):
            for technology_parent in parent.findall('location-info'):
                all_tech=[]
                for technology in technology_parent.findall('.//period/..'):
                    #print(technology.attrib)
                    tech_name = technology.attrib['name'] 
                    all_tech.append(tech_name)    
                    
                    if tech_name in itc_technology:
                        for period in technology.findall("period"): 
                            year=period.get('year')
                            if int(year)>stop_year:
                                technology.remove(period)
                            else:
                                for charge_rate in period.findall('input-capital/fixed-charge-rate'):
                                #charge_rate = period.find('input-capital/fixed-charge-rate')
                                #new_charge_rate = float(period.find('input-capital/fixed-charge-rate').text) * scenario[scenario_id].loc[tech_name,str(year)]
                                #charge_rate.text=str(new_charge_rate)
                                    #print(charge_rate.text)
                                    new_charge_rate = float(charge_rate.text) * scenario[scenario_id].loc[tech_name,str(year)]
                                    charge_rate.text=str(new_charge_rate)
                                    #print(year,charge_rate.text)
                    else:
                        technology_parent.remove(technology)
                        
                if not any(tech_tmp in itc_technology for tech_tmp in all_tech):
                    parent.remove(technology_parent)
                        
        tree_itc.write(itc_output_path + scenario_id+".xml",encoding="UTF-8",xml_declaration=True) 


def ptc_function(ptc_path,ptc_output_path,ptc_technology,case_number,case_id, scenario_ptc, stop_year):

    for case in range(1,case_number+1):
        tree_ptc = ET.parse(ptc_path)
        root_ptc = tree_ptc.getroot()
        
        scenario_id = case_id[case-1]
        for technology_parent in root_ptc.findall('location-info'):
            all_tech=[]
            for technology in technology_parent.findall('.//period/..'):
                #print(technology.attrib)
                tech_name = technology.attrib['name'] 
                all_tech.append(tech_name)  
                if tech_name in ptc_technology:
                    for period in technology.findall("period"): 
                        year=period.get('year')
                        if int(year)>stop_year:
                            technology.remove(period)
                        else:
                            non_energy_input = ET.SubElement(period, 'minicam-non-energy-input', name = 'tax credit')
                            ET.SubElement(non_energy_input, "input-cost").text=str(scenario_ptc[scenario_id].loc[tech_name,str(year)])
                else:
                    technology_parent.remove(technology)
            if not any(tech_tmp in ptc_technology for tech_tmp in all_tech):
                root_ptc.remove(technology_parent)
                    

                        
        tree_ptc.write(ptc_output_path + scenario_id+".xml",encoding="UTF-8",xml_declaration=True) 

    
def bus_function(bus_path,bus_output_path,bus_technology,case_number,case_id, scenario_bus, stop_year):
    
    for case in range(1,case_number+1):
        tree_bus = ET.parse(bus_path)
        root_bus = tree_bus.getroot()
        scenario_id = case_id[case-1]
        for region in root_bus.findall('.//region'):
            for supplysector in list(region):
                #print(supplysector.attrib)
                if supplysector.attrib['name'] != bus_technology['supplysector']:
                    region.remove(supplysector)
                else:
                    for tranSubsector in list(supplysector): 
                        if tranSubsector.attrib['name']!=bus_technology['tranSubsector']:
                            supplysector.remove(tranSubsector)
                        else:
                            for stub_technology in list(tranSubsector): 
                                if stub_technology.attrib['name'] != bus_technology['stub-technology']:
                                    tranSubsector.remove(stub_technology)
                                else:
                                    for period in list(stub_technology):
                                        year=period.get('year')
                                        if int(year)>stop_year:
                                            stub_technology.remove(period)
                                        else:
                                            for non_energy_input in period.findall('minicam-non-energy-input'):
                                                non_energy_input.attrib['name']='infra-cost'
                                                for input_cost in non_energy_input:
                                                    input_cost.text='-1'

                        
        tree_bus.write(bus_output_path + scenario_id+".xml",encoding="UTF-8",xml_declaration=True) 
        
        
def car_function(car_path,car_output_path,car_technology,case_number,case_id, scenario_car, stop_year):

    
    for case in range(1,case_number+1):
        tree_car = ET.parse(car_path)
        root_car = tree_car.getroot()
        scenario_id = case_id[case-1]
        for region in root_car.findall('.//region'):
            for supplysector in list(region):
                #print(supplysector.attrib)
                if supplysector.attrib['name'] != car_technology['supplysector']:
                    region.remove(supplysector)
                else:
                    for tranSubsector in list(supplysector): 
                        if tranSubsector.attrib['name']!=car_technology['tranSubsector']:
                            supplysector.remove(tranSubsector)
                        else:
                            for stub_technology in list(tranSubsector): 
                                if stub_technology.attrib['name'] != car_technology['stub-technology']:
                                    tranSubsector.remove(stub_technology)
                                else:
                                    for period in list(stub_technology):
                                        year=period.get('year')
                                        if int(year)>stop_year:
                                            stub_technology.remove(period)
                                        else:
                                            for non_energy_input in period.findall('minicam-non-energy-input'):
                                                non_energy_input.attrib['name']='infra-cost'
                                                for input_cost in non_energy_input:
                                                    input_cost.text=str(scenario_car[scenario_id].loc[:,str(year)].values[0])

                        
        tree_car.write(car_output_path + scenario_id+".xml",encoding="UTF-8",xml_declaration=True) 
        
        
def share_function(share_share_path,share_output_path, output_name, stop_year):
    tree_share = ET.parse(share_share_path)
    root_share = tree_share.getroot()
    for parent in root_share.findall('.//nesting-subsector/..'):
        for technology_parent in list(parent):
            all_tech=[]
            for technology in list(technology_parent):
                tech_name = technology_parent.attrib['name']
                all_tech.append(tech_name)
                if not "CCS" in technology.attrib['name']:
                    technology_parent.remove(technology)
                else:
                    for period in technology.findall('share-weight'):
                        year = period.attrib['year'] 
                        if int(year)>stop_year:
                            technology.remove(period)
                        else:
                           period.text="0"                   
            #if any(['CCS' not in tech_tmp for tech_tmp in all_tech]):
            if technology_parent.attrib['name'] in ['solar','wind','hydro','roof_top','nuclear','geothermal']:
                parent.remove(technology_parent)
                    
    tree_share.write(share_output_path + output_name,encoding="UTF-8",xml_declaration=True)         

def share_en_function(share_en_path,share_en_output_path, output_en_name, stop_year):
    tree_share = ET.parse(share_en_path)
    root_share = tree_share.getroot()
    for parent in root_share.findall('.//pass-through-sector/..'):
        for technology_parent in list(parent):
            if technology_parent.attrib['name'] == 'biomass liquids':
                for technology in list(technology_parent):  
                    #root_element = ET.Element(technology)
                    new_element1 = ET.SubElement(technology,'stub-technology')
                    new_element1.attrib['delete'] = "1"
                    new_element1.attrib['name'] = "cellulosic ethanol CCS level 1"
                    
                    new_element2 = ET.SubElement(technology,'stub-technology')
                    new_element2.attrib['delete'] = "1"
                    new_element2.attrib['name'] = "cellulosic ethanol CCS level 2"

                    new_element3 = ET.SubElement(technology,'stub-technology')                    
                    new_element3.attrib['delete'] = "1"
                    new_element3.attrib['name'] = "FT biofuels CCS level 1"
                    
                    new_element4 = ET.SubElement(technology,'stub-technology')                    
                    new_element4.attrib['delete'] = "1"
                    new_element4.attrib['name'] = "FT biofuels CCS level 2"
                    
                    new_element5 = ET.SubElement(technology,'stub-technology')                    
                    new_element5.attrib['delete'] = "1"
                    new_element5.attrib['name'] = "FT biofuels"
                    
                    new_element6 = ET.SubElement(technology,'stub-technology')
                    new_element6.attrib['delete'] = "1"
                    new_element6.attrib['name'] = "cellulosic ethanol"
             
            elif technology_parent.attrib['name'] == 'coal to liquids':
                 for technology in list(technology_parent):  
                     #root_element = ET.Element(technology)
                     new_element1 = ET.SubElement(technology,'stub-technology')
                     new_element1.attrib['delete'] = "1"
                     new_element1.attrib['name'] = "coal to liquids CCS level 1"
                     
                     new_element2 = ET.SubElement(technology,'stub-technology')
                     new_element2.attrib['delete'] = "1"
                     new_element2.attrib['name'] = "coal to liquids CCS level 2"
            else:
                parent.remove(technology_parent)
                    
    tree_share.write(share_en_output_path + output_en_name,encoding="UTF-8",xml_declaration=True) 
    
    
def share_h2_function(share_h2_path,share_h2_output_path, output_h2_name, stop_year):
    tree_share = ET.parse(share_h2_path)
    root_share = tree_share.getroot()
    for parent in root_share.findall('.//subsector/..'):
        for technology_parent in list(parent):
            if technology_parent.attrib['name'] == 'biomass':
                    new_element1 = ET.SubElement(technology_parent,'stub-technology')
                    new_element1.attrib['delete'] = "1"
                    new_element1.attrib['name'] = "biomass to H2 CCS"
             
            elif technology_parent.attrib['name'] == 'coal':
                     new_element1 = ET.SubElement(technology_parent,'stub-technology')
                     new_element1.attrib['delete'] = "1"
                     new_element1.attrib['name'] = "coal chemical CCS"

            elif technology_parent.attrib['name'] == 'gas':
                     new_element1 = ET.SubElement(technology_parent,'stub-technology')
                     new_element1.attrib['delete'] = "1"
                     new_element1.attrib['name'] = "natural gas steam reforming CCS"
    
    tree_share.write(share_h2_output_path + output_h2_name,encoding="UTF-8",xml_declaration=True) 

                
def bio_constraint_function(bio_path,bio_output_path, output_bio_name, stop_year):
    tree_bio = ET.parse(bio_path)
    root_bio = tree_bio.getroot()
    for parent in root_bio.findall('.//supplysector/..'):
        policy = ET.SubElement(parent,'policy-portfolio-standard')
        policy.attrib['name'] = "bio-constraint"
        market = ET.SubElement(policy,'market')
        market.text = 'USA'
        policytype = ET.SubElement(policy,'policyType')
        policytype.text = 'tax'
        for supplysector in list(parent):
            if supplysector.tag == "supplysector":
                if supplysector.attrib['name'] not in ['regional biomass','regional corn for ethanol', 'regional sugar for ethanol','regional biomassOil']:
                    parent.remove(supplysector)
                for tech in supplysector.findall('.//period/..'):
                    for period in list(tech):
                        if int(period.attrib['year']) < 2055:
                          new_element = ET.SubElement(period,'input-tax')
                          new_element.attrib['name'] = "bio-constraint"  
                
    tree_bio.write(bio_output_path + output_bio_name,encoding="UTF-8",xml_declaration=True) 
    
    
    
#this is not working    
def constraint_en_function(share_en_path,share_en_output_path, output_en_name, stop_year):
    tree_share = ET.parse(share_en_path)
    root_share = tree_share.getroot()
    
    for parent in root_share.findall('.//region/..'):
        for region in list(parent):
            if region.tag == "global-technology-database":
                parent.remove(region)
            elif region.attrib['name'] == "USA":
                parent.remove(region)
            
    for parent in root_share.findall('.//pass-through-sector/..'):
        if parent.attrib['name'] == "USA":
            root_share.remove(parent)
        if parent.tag == "global-technology-database":
            root_share.remove(parent)       
        else: 
            for technology_parent in list(parent):
                if (technology_parent.attrib['name'] in ['oil refining']) & (technology_parent.tag =="pass-through-sector"):
                    technology_parent.tag = "supplysector"
                    for subsector in list(technology_parent):  
                        if subsector.tag not in ["subsector",]:
                            technology_parent.remove(subsector)
                        else:
                            for tech in list(subsector):
                                if tech.tag != "stub-technology":
                                    subsector.remove(tech) 
                                else:
                                    for period in list(tech):
                                        for input_name in list(period):
                                            period.remove(input_name)
                                        if int(period.attrib['year']) < 2055:
                                            new_element = ET.SubElement(period,'input-tax')
                                            new_element.attrib['name'] = "oil-ceiling"                                             
                else:
                    parent.remove(technology_parent)
                    
    tree_share.write(share_en_output_path + output_en_name,encoding="UTF-8",xml_declaration=True)     
    
    
def power_constraint_function(share_power_path,share_output_path, output_name, stop_year):
     
    tree_power = ET.parse(share_power_path)
    root_power = tree_power.getroot()
    for technology in root_power.findall('.//location-info/..'):
        for sector in list(technology):
            if "biomass" in sector.attrib['subsector-name']:
                for CO2 in sector.findall('.//CO2'):
                    CO2.attrib['name'] = "CO2_USA"
                if 'CCS' in sector.attrib['subsector-name']:
                    for parent in sector.findall('.//period/..'):
                        for period in list(parent):
                            capture_component= ET.SubElement(period,'standard-capture-component')                        
                            target_gas = ET.SubElement(capture_component,'target-gas')
                            target_gas.text = "CO2_USA"
                
            elif "CCS" in sector.attrib['subsector-name']:
                for parent in sector.findall('.//period/..'):
                    for period in list(parent):
                        capture_component= ET.SubElement(period,'standard-capture-component')                        
                        target_gas = ET.SubElement(capture_component,'target-gas')
                        target_gas.text = "CO2_power"
                        
                        for sub_parent in parent.findall('.//CO2/..'):
                            for CO2 in list(sub_parent):
                                if CO2.tag == "CO2":
                                    CO2.attrib['name'] = "CO2_power"
            else:
                for parent in sector.findall('.//CO2/..'):
                    for CO2 in list(parent):
                        CO2.attrib['name'] = "CO2_power"
            
    tree_power.write(share_output_path + output_name,encoding="UTF-8",xml_declaration=True)    
    
    
def power_constraint_origin_function(origin_power_path,share_output_path, output_name, stop_year):
     
    tree_power = ET.parse(origin_power_path)
    root_power = tree_power.getroot()
                        
    for technology in root_power.findall('.//subsector/stub-technology/period/..'):
        for period in list(technology):
            if period.tag=="period":
                CO2 = ET.SubElement(period,'CO2')
                CO2.attrib['name'] = "CO2_power"
        if "biomass" in technology.attrib['name']:
            for CO2 in technology.findall('.//CO2'):
                CO2.attrib['name'] = "CO2_USA"
            if 'CCS' in technology.attrib['name']:
                for period in technology.findall('.//period'):                    
                    capture_component= ET.SubElement(period,'standard-capture-component')                        
                    target_gas = ET.SubElement(capture_component,'target-gas')
                    target_gas.text = "CO2_USA"
        elif "CCS" in technology.attrib['name']:
             for period in technology.findall('.//period'):
                    capture_component= ET.SubElement(period,'standard-capture-component')                        
                    target_gas = ET.SubElement(capture_component,'target-gas')
                    target_gas.text = "CO2_power"

            
    tree_power.write(share_output_path + output_name,encoding="UTF-8",xml_declaration=True)  
    
            
def power_constraint_usa_function(share_power_path,share_output_path, output_name, stop_year):
     
    tree_power = ET.parse(share_power_path)
    root_power = tree_power.getroot()
    for supply_sector in root_power.findall('.//pass-through-sector'):
        supply_sector.tag="supplysector"
    for technology in root_power.findall('.//subsector/..'):
        for sector in list(technology):
            if "biomass" in sector.attrib['name']:
                continue
            else:
                for parent in sector.findall('.//period/..'):
                    for period in list(parent): 
                        CO2 = ET.SubElement(period,'CO2')
                        CO2.attrib['name'] = "CO2_power"
            
    tree_power.write(share_output_path + output_name,encoding="UTF-8",xml_declaration=True)     
            
                     
            
def ghg_link_function(link_input_path,link_output_path,output_link_name,stop_year):
    tree_link = ET.parse(link_input_path)
    root_link = tree_link.getroot()
    '''
    for root in root_link.findall('.//region/..'):
        for region in list(root):
            if region.findall(".//*[.='USA']"):
                policy = ET.SubElement(region,'linked-ghg-policy')
                policy.attrib['name'] = "CO2_power_link"
                
                price_adjust = ET.SubElement(policy,'price-adjust')
                price_adjust.attrib['fillout'] = "1"
                price_adjust.attrib['year'] = "1975"
                price_adjust.text = "0"
                    
                demand_adjust = ET.SubElement(policy,'demand-adjust')
                demand_adjust.attrib['fillout'] = "1"
                demand_adjust.attrib['year'] = "1975"
                demand_adjust.text = "0"
                
                market = ET.SubElement(policy,'market')
                market.text = "USA"
                
                policy_name = ET.SubElement(policy,'policy-name')
                policy_name.text = "CO2_power"                
                
                GHG = ET.SubElement(policy,'linked-policy')
                GHG.text = "GHG"            
                
                price = ET.SubElement(policy,'price-unit')
                price.text = "1990$ /tC"  
                
                output = ET.SubElement(policy,'output-unit')
                output.text = "MtC"  
                
                price_adjust = ET.SubElement(policy,'price-adjust')
                price_adjust.attrib['fillout'] = "1"
                price_adjust.attrib['year'] = "2025"
                price_adjust.text = "1"
                
                demand_adjust = ET.SubElement(policy,'demand-adjust')
                demand_adjust.attrib['fillout'] = "1"
                demand_adjust.attrib['year'] = "2025"
                demand_adjust.text = "3.666666667"
                
                
                policy2 = ET.SubElement(region,'linked-ghg-policy')
                policy2.attrib['name'] = "CO2_transport_link"
                
                price_adjust2 = ET.SubElement(policy2,'price-adjust')
                price_adjust2.attrib['fillout'] = "1"
                price_adjust2.attrib['year'] = "1975"
                price_adjust2.text = "0"
                    
                demand_adjust2 = ET.SubElement(policy2,'demand-adjust')
                demand_adjust2.attrib['fillout'] = "1"
                demand_adjust2.attrib['year'] = "1975"
                demand_adjust2.text = "0"
                
                market2 = ET.SubElement(policy2,'market')
                market2.text = "USA"
                
                policy_name2 = ET.SubElement(policy2,'policy-name')
                policy_name2.text = "CO2_transport"                
                
                GHG2 = ET.SubElement(policy2,'linked-policy')
                GHG2.text = "GHG"            
                
                price2 = ET.SubElement(policy2,'price-unit')
                price2.text = "1990$ /tC"  
                
                output2 = ET.SubElement(policy2,'output-unit')
                output2.text = "MtC"  
                
                price_adjust2 = ET.SubElement(policy2,'price-adjust')
                price_adjust2.attrib['fillout'] = "1"
                price_adjust2.attrib['year'] = "2025"
                price_adjust2.text = "1"
                
                demand_adjust2 = ET.SubElement(policy2,'demand-adjust')
                demand_adjust2.attrib['fillout'] = "1"
                demand_adjust2.attrib['year'] = "2025"
                demand_adjust2.text = "3.666666667"
                
            else:
                continue
    '''
            
    for ghg_policy in root_link.findall(".//*[.='USA']/.."):
        if ghg_policy.attrib['name'] == 'CO2':
           ghg_policy.attrib['name'] = 'CO2_USA'
    for root in root_link.findall('.//region/..'):
        for region in list(root):
            if region.findall(".//*[.='USA']"):
              policy2 = ET.SubElement(region,'linked-ghg-policy')
              policy2.attrib['name'] = "CO2_USA_BECCS"
              
              price_adjust2 = ET.SubElement(policy2,'price-adjust')
              price_adjust2.attrib['fillout'] = "1"
              price_adjust2.attrib['year'] = "1975"
              price_adjust2.text = "0"
                  
              demand_adjust2 = ET.SubElement(policy2,'demand-adjust')
              demand_adjust2.attrib['fillout'] = "1"
              demand_adjust2.attrib['year'] = "1975"
              demand_adjust2.text = "0"
              
              market2 = ET.SubElement(policy2,'market')
              market2.text = "USA"
              
              #policy_name2 = ET.SubElement(policy2,'policy-name')
              #policy_name2.text = "CO2_transport"                
              
              GHG2 = ET.SubElement(policy2,'linked-policy')
              GHG2.text = "GHG"            
              
              price2 = ET.SubElement(policy2,'price-unit')
              price2.text = "1990$ /tC"  
              
              output2 = ET.SubElement(policy2,'output-unit')
              output2.text = "MtC"  
              
              price_adjust2 = ET.SubElement(policy2,'price-adjust')
              price_adjust2.attrib['fillout'] = "1"
              price_adjust2.attrib['year'] = "2025"
              price_adjust2.text = "1"
              
              demand_adjust2 = ET.SubElement(policy2,'demand-adjust')
              demand_adjust2.attrib['fillout'] = "1"
              demand_adjust2.attrib['year'] = "2025"
              demand_adjust2.text = "1"
            
    tree_link.write(link_output_path + output_link_name,encoding="UTF-8",xml_declaration=True)
     


def en_CO2_function(en_transformation_path,share_output_path, en_output_name, stop_year):
    tree_share = ET.parse(en_transformation_path)
    root_share = tree_share.getroot()
            
    for CO2 in root_share.findall(".//subsector[@name!='biomass liquids']/pass-through-technology//CO2"):
        CO2.attrib['name']='CO2_USA'
        
    for CO2 in root_share.findall(".//subsector[@name='oil refining']//pass-through-technology//CO2"):
        CO2.attrib['name']='CO2_USA'
        
    for period in root_share.findall(".//pass-through-sector[@name!='biomass liquids']//stub-technology/period"):
        CO2 = ET.SubElement(period,'CO2')
        CO2.attrib['name'] = "CO2_USA"

    for CO2 in root_share.findall(".//subsector[@name='oil refining']//stub-technology/period/CO2"):
        CO2.attrib['name'] = "CO2_USA"
        
    for technology in root_share.findall(".//pass-through-sector[@name!='biomass liquids']//stub-technology"):
        if "CCS" in technology.attrib['name'] :
            for period in technology.findall('.//period'):
                capture_component= ET.SubElement(period,'standard-capture-component')                        
                target_gas = ET.SubElement(capture_component,'target-gas')
                target_gas.text = "CO2_USA" 

    tree_share.write(share_output_path + en_output_name,encoding="UTF-8",xml_declaration=True)     

def en_all_CO2_function(en_all_transformation_path,share_output_path, en_all_output_name, stop_year):
    tree_share = ET.parse(en_all_transformation_path)
    root_share = tree_share.getroot()
                  
    for technology in root_share.findall(".//region[@name='USA']/supplysector[@name='gas processing']/subsector[@name!='biomass gasification']/stub-technology"):
        for year in np.arange(2020,2055,5):
                period_year = ET.SubElement(technology,'period')
                period_year.attrib['year'] = str(year)
                CO2 = ET.SubElement(period_year,'CO2')
                CO2.attrib['name'] = "CO2_USA"

    tree_share.write(share_output_path + en_all_output_name,encoding="UTF-8",xml_declaration=True)     
    
    
def transport_CO2_function(trans_path,share_output_path,trans_output_name, stop_year):
    
       tree_share = ET.parse(trans_path)
       root_share = tree_share.getroot()
               
       for period in root_share.findall('.//stub-technology/period'):
            CO2 = ET.SubElement(period,'CO2')
            CO2.attrib['name'] = "CO2_USA"
       for CO2 in root_share.findall(".//stub-technology[@name='Liquids']/period/CO2"):
            CO2.attrib['name'] = "CO2_transport"

       for CO2 in root_share.findall(".//stub-technology[@name='Hybrid Liquids']/period/CO2"):
            CO2.attrib['name'] = "CO2_transport" 
       tree_share.write(share_output_path + trans_output_name,encoding="UTF-8",xml_declaration=True)     


def building_CO2_function(building_path,share_output_path,building_output_name, stop_year):
    
       tree_share = ET.parse(building_path)
       root_share = tree_share.getroot()
               
       for period in root_share.findall('.//stub-technology/period'):
            CO2 = ET.SubElement(period,'CO2')
            CO2.attrib['name'] = "CO2_USA"
       
       tree_share.write(share_output_path + building_output_name,encoding="UTF-8",xml_declaration=True)  
       
def industry_CO2_function(industry_path,share_output_path, industry_output_name, stop_year):
    
       tree_share = ET.parse(industry_path)
       root_share = tree_share.getroot()
               
       for period in root_share.findall('.//stub-technology/period'):
            CO2 = ET.SubElement(period,'CO2')
            CO2.attrib['name'] = "CO2_USA"
            
       for period in root_share.findall(".//supplysector[@name='other industrial feedstocks']//stub-technology/period"):   
            non_capture_component = ET.SubElement(period,'non-energy-use-capture-component')
            target_gas = ET.SubElement(non_capture_component,'target-gas')
            target_gas.text = "CO2_USA"
            
       
       tree_share.write(share_output_path + industry_output_name,encoding="UTF-8",xml_declaration=True)         

def cement_CO2_function(cement_path,share_output_path, cement_output_name, stop_year):
    tree_share = ET.parse(cement_path)
    root_share = tree_share.getroot()
            
    for technology in root_share.findall('.//stub-technology'):
        if "CCS" in technology.attrib['name'] :
            for period in technology.findall('.//period'):
                capture_component= ET.SubElement(period,'standard-capture-component')                        
                target_gas = ET.SubElement(capture_component,'target-gas')
                target_gas.text = "CO2_USA" 
     
    for period in root_share.findall('.//stub-technology/period'):
        CO2 = ET.SubElement(period,'CO2')
        CO2.attrib['name'] = "CO2_USA"
                    
    tree_share.write(share_output_path + cement_output_name,encoding="UTF-8",xml_declaration=True)  
    
    
def H2_CO2_function(H2_path,share_output_path, H2_output_name, stop_year):
    tree_share = ET.parse(H2_path)
    root_share = tree_share.getroot()
                
    for period in root_share.findall(".//subsector[@name!='biomass']//stub-technology/period"):
        CO2 = ET.SubElement(period,'CO2')
        CO2.attrib['name'] = "CO2_USA"
        
    for technology in root_share.findall(".//subsector[@name!='biomass']//stub-technology"):
        if "CCS" in technology.attrib['name'] :
            for period in technology.findall('.//period'):
                capture_component= ET.SubElement(period,'standard-capture-component')                        
                target_gas = ET.SubElement(capture_component,'target-gas')
                target_gas.text = "CO2_USA"
                    
    tree_share.write(share_output_path + H2_output_name,encoding="UTF-8",xml_declaration=True) 
    
def fert_CO2_function(fert_path,share_output_path, fert_output_name, stop_year):
    tree_share = ET.parse(fert_path)
    root_share = tree_share.getroot()
            
    for technology in root_share.findall('.//stub-technology'):
        if "CCS" in technology.attrib['name'] :
            for period in technology.findall('.//period'):
                capture_component= ET.SubElement(period,'standard-capture-component')                        
                target_gas = ET.SubElement(capture_component,'target-gas')
                target_gas.text = "CO2_USA" 
     
    for period in root_share.findall('.//stub-technology/period'):
        CO2 = ET.SubElement(period,'CO2')
        CO2.attrib['name'] = "CO2_USA"
    for CO2 in root_share.findall('.//technology/period/CO2'):
        CO2.attrib['name'] = "CO2_USA"
                    
    tree_share.write(share_output_path + fert_output_name,encoding="UTF-8",xml_declaration=True) 
    
    
def biomass_CO2_function(biomass_path,share_output_path, biomass_output_name, stop_year):
    tree_share = ET.parse(biomass_path)
    root_share = tree_share.getroot()
            
    for technology in root_share.findall('.//stub-technology'):
        if "CCS" in technology.attrib['name'] :
            for period in technology.findall('.//period'):
                capture_component= ET.SubElement(period,'standard-capture-component')                        
                target_gas = ET.SubElement(capture_component,'target-gas')
                target_gas.text = "CO2_USA" 
     
    for period in root_share.findall('.//stub-technology/period'):
        CO2 = ET.SubElement(period,'CO2')
        CO2.attrib['name'] = "CO2_USA"
        
    for CO2 in root_share.findall('.//technology/period/CO2'):
        CO2.attrib['name'] = "CO2_USA"
                    
    tree_share.write(share_output_path + biomass_output_name,encoding="UTF-8",xml_declaration=True) 
    
def distribution_CO2_function(distribution_path,share_output_path, distribution_output_name, stop_year):
    tree_share = ET.parse(distribution_path)
    root_share = tree_share.getroot()
     
    for tech in root_share.findall(".//region[@name='USA']//stub-technology"):
        if tech.findall('.//period'):
            for period in tech.findall('.//period'):
                CO2 = ET.SubElement(period,'CO2')
                CO2.attrib['name'] = "CO2_USA"
                
        else:
            for year in np.arange(2015,2055,5):
                period_year = ET.SubElement(tech,'period')
                period_year.attrib['year'] = str(year)
                CO2 = ET.SubElement(period_year,'CO2')
                CO2.attrib['name'] = "CO2_USA"
        
                    
    tree_share.write(share_output_path + distribution_output_name,encoding="UTF-8",xml_declaration=True) 
    

def DAC_CO2_function(dac_path,share_output_path, dac_output_name, stop_year):
    tree_share = ET.parse(dac_path)
    root_share = tree_share.getroot()
     
    for tech in root_share.findall(".//stub-technology"):
        if tech.findall('.//period'):
            for period in tech.findall('.//period'):
                CO2 = ET.SubElement(period,'CO2')
                CO2.attrib['name'] = "CO2_USA"
                if tech.attrib['name'] != 'no DAC':
                    capture_component= ET.SubElement(period,'standard-capture-component')                        
                    target_gas = ET.SubElement(capture_component,'target-gas')
                    target_gas.text = "CO2_USA" 
                
        else:
            for year in np.arange(2015,2055,5):
                period_year = ET.SubElement(tech,'period')
                period_year.attrib['year'] = str(year)
                CO2 = ET.SubElement(period_year,'CO2')
                CO2.attrib['name'] = "CO2_USA"
        
                    
    tree_share.write(share_output_path + dac_output_name,encoding="UTF-8",xml_declaration=True)     
    
#%% change the cost of ele
def elec_capital_function(elec_path,elec_output_path, technology_cost, start_year, stop_year):
        
    tree_capital = ET.parse(elec_path)
    root_capital = tree_capital.getroot()
    
    technology_list=technology_cost.technology

    for parent in root_capital.findall(".//location-info"):
        tech_name = parent.attrib['subsector-name'] 
        if tech_name in technology_list.values:
            print(tech_name)
            for period in parent.findall('.//period'):
                year = int(period.attrib['year'])
                if (year<start_year) | (year>stop_year) :
                    continue
                else:
                    for capital_overnight in period.findall("input-capital[@name='capital']/capital-overnight"):
                       #print(capital_overnight.text)
                       new_capital_overnight = int(technology_cost.loc[technology_cost.technology==tech_name ,year])
                       capital_overnight.text=str(new_capital_overnight)
                       #print(year,capital_overnight.text)
                
        else:
            continue
        
    for subsector in root_capital.findall(".//nesting-subsector[@name='coal']/subsector"):
        name = subsector.attrib['name']
        if '-' in name: 
            print(name)
            for half in subsector.findall('.//half-life'):
                life = int(half.text)-10
                half.text = str(life)
                #print(half.text)
        else:
            continue
            
                    
    tree_capital.write(elec_output_path +".xml",encoding="UTF-8",xml_declaration=True) 
