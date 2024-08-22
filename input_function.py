#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 20:22:46 2024

@author: haozheyang
"""
import xml.etree.ElementTree as ET

def itc_function(itc_path,itc_output_path,itc_technology,case_number,case_id, scenario, stop_year):
    tree_itc = ET.parse(itc_path)
    root_itc = tree_itc.getroot()
    
    for case in range(1,case_number+1):
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
                                    new_charge_rate = float(charge_rate.text) * scenario[scenario_id].loc[tech_name,str(year)]
                                    charge_rate.text=str(new_charge_rate)
                                    #print(year,charge_rate.text)
                    else:
                        technology_parent.remove(technology)
                        
                if not any(tech_tmp in itc_technology for tech_tmp in all_tech):
                    parent.remove(technology_parent)
                        
        tree_itc.write(itc_output_path + scenario_id+".xml",encoding="UTF-8",xml_declaration=True) 


def ptc_function(ptc_path,ptc_output_path,ptc_technology,case_number,case_id, scenario_ptc, stop_year):
    tree_ptc = ET.parse(ptc_path)
    root_ptc = tree_ptc.getroot()
    
    for case in range(1,case_number+1):
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
    tree_bus = ET.parse(bus_path)
    root_bus = tree_bus.getroot()
    
    for case in range(1,case_number+1):
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
    tree_car = ET.parse(car_path)
    root_car = tree_car.getroot()
    
    for case in range(1,case_number+1):
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
        
        
        
