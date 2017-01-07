# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 17:17:42 2016

@author: Koats
"""

import string, sys, struct
from ctypes import *
import os
import sscapi
from pymongo import MongoClient
import csv
import borg as bg
#import json
#import urllib
#import urllib2
#import requests

c_number = c_float # must be c_double or c_float depending on how defined in sscapi.h

# Test program 'main'

print('Hello, PySSC')
ssc = sscapi.PySSC()
print('Computer = ', sys.platform)
print('Version: {0}'.format(ssc.version()))


# Analysis Period for lifetime of avg PV panel system

#tilt, azimuth, mods_string,string_num

def solar_opt(*variables):

    global cost_per_watt
    global max_inverter
    global mppt_low_inverter
    global mod_temp_coeff
    global mod_nom_voc
    global runCount
    
    # Initializes data creation module for 
    analysis_period = 25 # Average solar system lifespan
    degradation = [0.5 for x in range(analysis_period)] # Average degradation selection  
#    nVars = [string_num,mods_string,tilt,azimuth]
#    for i in len(nVars):
#        nVars[i] = variables[i]

    inverter_num = int(variables[0])
    

    
    dat = ssc.data_create()
    #######Weather Data#############################
    # Pulls from TMY data storage
    ssc.data_set_string(dat, 'solar_resource_file', '../../examples/daggett.tm2')
    ssc.data_set_string(dat, 'file_name', '../../examples/daggett.tm2')

    
    # Simulation Parameter Call
    ######Simulation Parameters ######################
    # Lifetime Simulation Boolean
    
    ssc.data_set_number(dat, 'pv_lifetime_simulation', 1)
    # Analysis Period Length
    ssc.data_set_number(dat, 'analysis_period', analysis_period)
    # DC degregation Rate %
    ssc.data_set_array(dat, 'dc_degradation', degradation)
    # Snow Model Toggle    
    ssc.data_set_number(dat, 'en_snow_model', 1)
    # Use Albedo in weather file if provided Boolean
    ssc.data_set_number(dat, 'use_wf_albedo', 1)
    # User Specified Albedo
    ssc.data_set_array(dat, 'albedo', [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1])
    #Irradiance Input Translation mode    
    # 0=beam&diffuse,1=total&beam,2=total&diffuse
    ssc.data_set_number(dat, 'irrad_mode', 0)
    # Diffuse Model
    #0=isotropic,1=hkdr,2=perez
    ssc.data_set_number(dat, 'sky_model', 0)
    # Interconnection AC loss %
    ssc.data_set_number(dat, 'ac_loss', 0.77)
    # Modules Per String
    
    # Enables misaligned panels
    #Boolean
    ssc.data_set_number(dat, 'enable_mismatch_vmax_calc', 0)
    # Photovoltaic module model specification
    # 0=spe,1=cec,2=6par_user,3=snl,4=sd11-iec61853
    ssc.data_set_number(dat, 'module_model', 0)
    # Inverter Module
    # 0=cec,1=datasheet,2=partload
    ssc.data_set_number(dat, 'inverter_model', 1)
    #Battery Load Profile
    #ssc.data_set_number(dat, 'load', 1)
    #System Capacity
    
    ######### Nonessential Subarray Parameters #############3#    
    #Subarray 2 Enable
    ssc.data_set_number(dat,'subarray2_enable', 0)
    #Subarray 3 Enable
    ssc.data_set_number(dat,'subarray3_enable', 0)
    #Subarray 4 Enable
    ssc.data_set_number(dat,'subarray4_enable', 0)    
    #Subarray 2 shade set
    ssc.data_set_number(dat,'subarray2_shade_mode', 1)
    #Subarray 3 shade set
    ssc.data_set_number(dat,'subarray3_shade_mode', 1)
    #Subarray 4 shade set
    ssc.data_set_number(dat,'subarray4_shade_mode', 1)
    #Subarray 2 track set
    ssc.data_set_number(dat,'subarray2_track_mode', 1)
    #Subarray 3 track set
    ssc.data_set_number(dat,'subarray3_track_mode', 1)
    #Subarray 4 track set
    ssc.data_set_number(dat,'subarray4_track_mode', 1)
    #Subarray 2 tilt set
    ssc.data_set_number(dat,'subarray2_tilt', 0)
    #Subarray 3 tilt set
    ssc.data_set_number(dat,'subarray3_tilt', 0)
    #Subarray 4 tilt set
    ssc.data_set_number(dat,'subarray4_tilt', 0)
    #Subarray 2 backtrack set
    ssc.data_set_number(dat,'subarray2_backtrack', 0)
    #Subarray 3 backtrack set
    ssc.data_set_number(dat,'subarray3_backtrack', 0)
    #Subarray 4 backtrack set
    ssc.data_set_number(dat,'subarray4_backtrack', 0)      
    
    ####### Subarray Parameters ###############################3
    
    
    # Auto-tilt of Subarray = Latitude
    ssc.data_set_number(dat,'subarray1_tilt_eq_lat', 0)
    
    # Tracking Mode
    #0=fixed,1=1axis,2=2axis,3=azi
    ssc.data_set_number(dat,'subarray1_track_mode', 0)
    # Shading Mode
    #0=selfshaded,1=none
    ssc.data_set_number(dat,'subarray1_shade_mode', 1)
    #No of modules along side of array
    ssc.data_set_number(dat,'subarray1_nmody',9)
    ssc.data_set_number(dat,'subarray1_nmodx',1)
    
    ######### Loss Parameters ########################
    # External Equipment loss 
    # Loss from DC optimizer %
    ssc.data_set_number(dat,'dcoptimizer_loss', 1.0)
    # AC wiring loss %
    ssc.data_set_number(dat,'acwiring_loss', 1.0)
    # transfomer Loss %
    ssc.data_set_number(dat, 'transformer_loss', 1.0)
    # Constant Loss Adjustment %
    ssc.data_set_number(dat, 'adjust:constant', 0)
    
    # Hourly Loss Adjustments %
    #ssc.data_set_array(dat, 'adjust:hourly', 0)
    # Period-Based Loss Adjustments
    # n x 3 matrix
    #ssc.data_set_matrix(dat, 'adjust:periods', 1)
    
    # Ground Coveraage Ratio
    ssc.data_set_number(dat, 'subarray1_', 0.3)
    # Panel Losses
    # Monthly Soiling Loss %
    ssc.data_set_array(dat, 'subarray1_soiling', [5.0,5.0,5.0,5.0,5.0,5.0,5.0,5.0,5.0,5.0,5.0,5.0])
    # DC Power Loss %
    ssc.data_set_number(dat, 'subarray1_dcloss', 0)
    # DC diodes and connections loss %
    ssc.data_set_number(dat, 'subarray1_diodeconn_loss', 0.5)
    # DC wiring loss %
    ssc.data_set_number(dat, 'subarray1_dcwiring_loss', 2.0)
    # Nameplate Loss %
    ssc.data_set_number(dat, 'subarray1_nameplate_loss', 0)
     # Panel Mismatch Loss
    ssc.data_set_number(dat, 'subarray1_mismatch_loss', 2.0)
    # Panel Tracking Loss
    ssc.data_set_number(dat, 'subarray1_tracking_loss', 0)
    
    ######### Inverter Parameters##################
    
    ##### Standard Inverter Setup from SAM Model
    # Minimum Inverter MPPT Voltage
    ssc.data_set_number(dat,'mppt_low_inverter', mppt_low_inverter)
    # Maximum Inverter MPPT Voltage
    ssc.data_set_number(dat, 'mppt_hi_inverter', 480)
    # AC maximum power rating (Wac)
    ssc.data_set_number(dat, 'inv_ds_paco', 4000)
    # Weighted or PEak or Nominal Efficiency
    ssc.data_set_number(dat, 'inv_ds_eff', 95.002)
    # AC power consumbed by inverter at night (Wac)
    ssc.data_set_number(dat, 'inv_ds_pnt',1 )
    # DC power required to enable the inversion process (Wdc)
    ssc.data_set_number(dat, 'inv_ds_pso',0 )
    # DC input voltage for the rated AC-Power rating
    ssc.data_set_number(dat, 'inv_ds_vdco',310)
    # Maximum DC operating voltage
    ssc.data_set_number(dat, 'inv_ds_vdcmax', max_inverter_v)
    
    ####### Module Parameters#######################
    
    ##### Kyocera KD315GX-LPB##
    # Module Area (m2)
    ssc.data_set_number(dat, 'spe_area',2.19384 )
    # Irradiance Level 0 (W/m2)
    ssc.data_set_number(dat, 'spe_rad0',200)
    # Irradiance Level 1 (W/m2)
    ssc.data_set_number(dat, 'spe_rad1',400 )
    # Irradiance Level 2 (W/m2)
    ssc.data_set_number(dat, 'spe_rad2', 600)
    # Irradiance Level 3 (W/m2)
    ssc.data_set_number(dat, 'spe_rad3', 800)
    # Irradiance Level 4 (W/m2)
    ssc.data_set_number(dat, 'spe_rad4', 1000)
    # Effciency at IRR 0 %
    ssc.data_set_number(dat, 'spe_eff0', 14.8267)
    # Effciency at IRR 1 %
    ssc.data_set_number(dat, 'spe_eff1', 14.8267)
    # Effciency at IRR 2 %
    ssc.data_set_number(dat, 'spe_eff2', 14.8267)
    # Effciency at IRR 3 %
    ssc.data_set_number(dat, 'spe_eff3', 14.8267)
    # Effciency at IRR 4 %
    ssc.data_set_number(dat, 'spe_eff4', 14.8267)
    # Reference Irradiance Level %
    ssc.data_set_number(dat, 'spe_reference', 4)
    # Module mounting Structure 
    # 0=glass/cell/polymer sheet - open rack,1=glass/cell/glass - open rack,2=polymer/thin film/steel - open rack,3=Insulated back, building-integrated PV,4=close roof mount,5=user-defined
    ssc.data_set_number(dat, 'spe_module_structure', 4)
    # Cell temp parameter a
    ssc.data_set_number(dat, 'spe_a', -2.98)
    # Cell temp parameter b
    ssc.data_set_number(dat, 'spe_b', -0.0471)
    # Cell temp parameter dT
    ssc.data_set_number(dat, 'spe_dT', 1)
    # Temperature Coefficient
    ssc.data_set_number(dat, 'spe_temp_coeff', mod_temp_coeff)
    # Diffuse Fraction
    ssc.data_set_number(dat, 'spe_fd', 1)
    # Nominal Max power Voltage
    ssc.data_set_number(dat, 'spe_vmp', mod_nom_vmp)
    # Nominal Open Circuit Voltage
    ssc.data_set_number(dat, 'spe_voc', mod_nom_voc)
    ##########################################
    
    
    ##############Altered Parameters###########################
    # Tilt of Subarray 
    ssc.data_set_number(dat,'subarray1_tilt', variables[2])
    # Nameplate Capacity
    ssc.data_set_number(dat, 'system_capacity', 5.0)
    #system_size = system_size + 0.1
    ssc.data_set_number(dat, 'modules_per_string', int(variables[1]))
    #Strings in parallel    
    ssc.data_set_number(dat, 'strings_in_parallel',int(variables[0]))
    # Number of Inverter
    ssc.data_set_number(dat, 'inverter_count', inverter_num)
    # Azimuth of subarray 
    #0=N,90=E,180=S,270=W
    ssc.data_set_number(dat,'subarray1_azimuth', variables[3])
    
    panel_num = variables[1] * variables[0]
    install_cost = panel_num *315 * cost_per_watt
    
    ###########################################################
    # run PV system simulation
    pvsamv1 = ssc.module_create("pvsamv1")
    if ssc.module_exec(pvsamv1, dat) == 0:
        print ('PVSAM1 simulation error')
        idx = 1
        msg = ssc.module_log(pvsamv1, 0)
        while (msg != None):
            print ('\t: ' + msg)
            msg = ssc.module_log(pvsamv1, idx)
            idx = idx + 1
    else:
        
        gen = ssc.data_get_array(dat,"gen")
        annual_energy = ssc.data_get_number(dat,"annual_energy")
    
    ssc.module_free(pvsamv1)
    
    
    
    
    ############ Utility Rate ###############################
    
    load_data = []
    with open('USA_CA_Barstow.Daggett.AP.723815_TMY3_BASE.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        next(readCSV)
        for row in readCSV:
            load_data.append(float(row[1]))
    
    
    
    
    
    #Analysis Period
    ssc.data_set_number(dat,"analysis_period", analysis_period)
    # System Use Lifetime Output
    ssc.data_set_number(dat,"system_use_lifetime_output", 1)
    # Gen
    ssc.data_set_array(dat,"gen", gen)
    #Load
    ssc.data_set_array(dat,"load", load_data)
    # Inflation Rate
    ssc.data_set_number(dat,"inflation_rate", 2.5)
    # Degradation
    ssc.data_set_array(dat,"degradation", degradation)
    # Set Load Escalation Array
    ssc.data_set_array(dat,"load_escalation", [1])
    # Excess Monthly Energy Handling
    # 0=Rollover energy,1=Rollover dollars
    ssc.data_set_array(dat,"rate_escalation", [0])
    #Enable Net Metering
    ssc.data_set_number(dat,"ur_enable_net_metering",1)
    # Excess Monthly Rollover Energy
    # 0=Rollover energy,1=Rollover dollars
    ssc.data_set_number(dat,"ur_excess_monthly_energy_or_dollars",0)
    # Net MEtering Year-end Sell Rate
    ssc.data_set_number(dat,"ur_nm_yearend_sell_rate", nm_sell_rate)
    # Monthly Fixed Charge
    ssc.data_set_number(dat,"ur_monthly_fixed_charge", 10)
    # Flat Buy Rate
    ssc.data_set_number(dat,"ur_flat_buy_rate", 0)
    # Flat Sell Rate
    ssc.data_set_number(dat,"ur_flat_sell_rate", 0)
    # Monthly Minimum Charge
    ssc.data_set_number(dat,"ur_monthly_min_charge", 0)
    # Annual Monthly Minimum Charge
    ssc.data_set_number(dat,"ur_annual_min_charge", 0)
    
    
    utilrate = ssc.module_create("utilityrate3")
    if ssc.module_exec(utilrate, dat) == 0:
        print ('Utility Rate error')
        idx = 1
        msg = ssc.module_log(utilrate, 0)
        while (msg != None):
            print ('\t: ' + msg)
            msg = ssc.module_log(utilrate, idx)
            idx = idx + 1
    else:
        annual_energy_value = ssc.data_get_array(dat,"annual_energy_value")
        annual_electric_load = ssc.data_get_array(dat,"annual_electric_load")
        elec_cost_with_system = ssc.data_get_array(dat,"elec_cost_with_system")
        elec_cost_without_system = ssc.data_get_array(dat,"elec_cost_without_system")
        lifetime_load = ssc.data_get_array(dat,"lifetime_load")
        
        elec_cost_with_system_year1 = ssc.data_get_number(dat,"elec_cost_with_system_year1")
        elec_cost_without_system_year1 = ssc.data_get_number(dat,"elec_cost_without_system_year1")
        savings_year1= ssc.data_get_number(dat,"savings_year1")
        year1_electric_load =ssc.data_get_number(dat,"year1_electric_load")
        year1_hourly_load = ssc.data_get_array(dat,"year1_hourly_load") 
        year1_monthly_cumulative_excess_generation = ssc.data_get_array(dat, "year1_monthly_cumulative_excess_generation") #kWh/mo
        year1_monthly_cumulative_excess_dollars = ssc.data_get_array(dat, "year1_monthly_cumulative_excess_dollars") #$/mo
    ssc.module_free(utilrate)
    
    ############ Cash Loan ##################################
    
    
    #Analysis Period
    ssc.data_set_number(dat,"analysis_period", analysis_period)
    # Federal Tax Rate
    ssc.data_set_number(dat,"federal_tax_rate", 30)
    # State Tax Rate
    ssc.data_set_number(dat,"state_tax_rate", 12) ##########
    # Real Discount Rate
    ssc.data_set_number(dat,"real_discount_rate", 5.5)
    # Inflation Rate
    ssc.data_set_number(dat,"inflation_rate", 2.5)
    # Debt Fraction
    ssc.data_set_number(dat,"debt_fraction", 0)
    # Production-based O&M Amount
    ssc.data_set_array(dat,"om_production", [0])
    # Production-based O&M Escalation
    ssc.data_set_number(dat,"om_production_escal", 0)
    # Capacity-based O&M amount
    ssc.data_set_array(dat,"om_capacity", [20])
    # Capacity-based O&M escalation
    ssc.data_set_number(dat,"om_capacity_escal", 2.5)
    # Insurance Rate
    ssc.data_set_number(dat,"insurance_rate", 1)
    # Investment Tax Credit Federal %
    ssc.data_set_number(dat,"itc_fed_percent", 30)
    # ITC State Percent
    ssc.data_set_number(dat,"itc_sta_percent", 25)
    # System Capacity
    #ssc.data_set_number(dat,"system_capacity", 5.0)
    # Market
    #0=residential,1=comm.
    ssc.data_set_number(dat,"market", 0)
    # Mortgage
    # 0=standard loan,1=mortgage
    ssc.data_set_number(dat,"ur_monthly_fixed_charge", 0)
    # Total Installed Cost
    ssc.data_set_number(dat,"total_installed_cost", install_cost) ############3
    # Gen
    ssc.data_set_array(dat,"gen", gen)
    # Degradation
    ssc.data_set_array(dat,"degradation", degradation)
    # System Use Lifetime Output
    ssc.data_set_number(dat,"system_use_lifetime_output", 1)
    #
    
    
    cashloan = ssc.module_create("cashloan")
    if ssc.module_exec(cashloan, dat) == 0:
        print ('Cash loan error')
        idx = 1
        msg = ssc.module_log(cashloan, 0)
        while (msg != None):
            print ('\t: ' + msg)
            msg = ssc.module_log(cashloan, idx)
            idx = idx + 1
    else:
        
        lcoe_real = ssc.data_get_number(dat,"lcoe_real")
        lcoe_nom = ssc.data_get_number(dat,"lcoe_nom")
        payback = ssc.data_get_number(dat,"payback")
        present_value_oandm = ssc.data_get_number(dat,"present_value_oandm")
        adjusted_installed_cost = ssc.data_get_number(dat,"adjusted_installed_cost")
        npv = ssc.data_get_number(dat,"npv")
        

###################### Solar Fraction and Net Metering Credit for Year 1

    year1_excess_energy = sum(year1_monthly_cumulative_excess_generation)
    year1_excess_dollars = year1_excess_energy * nm_sell_rate

    grid_energy = []
    
    for i in range(1,len(load_data)):
        if load_data[i]-gen[i] > 0:
            grid_energy.append(load_data[i]-gen[i])
        elif load_data[i]-gen[i] <= 0:
            grid_energy.append(0)
    annual_avg_solar_fraction = ((annual_energy-sum(grid_energy))/year1_electric_load)*100
#############################Write Data to csv
    
    array_out = [annual_electric_load,lifetime_load,elec_cost_without_system,elec_cost_with_system, annual_energy_value,year1_hourly_load]
    single_out = [lcoe_real,lcoe_nom, savings_year1,elec_cost_with_system_year1,elec_cost_without_system_year1, year1_electric_load, year1_excess_energy, year1_excess_dollars]
    results_borg = [-1*npv,adjusted_installed_cost,-1*annual_avg_solar_fraction]
  
    
    directory = os.getcwd()
    with open(os.path.join(directory, 'arraysolar.csv'), 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = ["Annual Electric Load", "Lifetime Load", "Annual Electric Cost w\o System", "Annual Electric Cost w System","Annual Energy Value", "Year 1 Hourly Load", "Year 1 Hourly Energy Grid","Year 1 Hourly Power Grid"], delimiter = ',')
        writer.writeheader()
        wr = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        wr.writerow(array_out)
        
    with open(os.path.join(directory, 'singlesolar.csv'), 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = ["Real LCOE", "Nominal LCOE", "Year 1 Savings","Year 1 Electric Cost w System","Year 1 Electric Cost w\o System","Year 1 Load","Year 1 Excess Energy","Year 1 Excess Dollars"], delimiter = ',')
        writer.writeheader()
        wr = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        wr.writerow(single_out)
    
    with open(os.path.join(directory, 'results_borg.csv'), 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = ["Net Present Value", "Installed Cost", "Payback Period","Percent of Annual Load Satisfied"], delimiter = ',')
        writer.writeheader()
        wr = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        wr.writerow(results_borg)
        
    ssc.module_free(cashloan)
    ssc.data_free(dat)
    runCount += 1
    return results_borg



#########################################################



################################## BORG



nm_sell_rate= 0.09199

min_temp= -7.72
max_temp = 23.89
cost_per_watt = 4.38


## Change to Raw Input
max_inverter_v= 600
mppt_low_inverter = 250
mod_temp_coeff = -0.177
mod_nom_voc = 49.2
mod_nom_vmp = 39.8

mod_lower_bound = int(round(mppt_low_inverter/ (mod_nom_vmp - ((max_temp-25) * mod_temp_coeff)))) +1
mod_upper_bound = int(max_inverter_v/ (mod_nom_voc + ((max_temp-25) * mod_temp_coeff)))

if mod_lower_bound <= 0 or mod_upper_bound <= 0:
    print ("Module Bound Error, cannot be less than zero")
    exit()

str_lower_bound = 1

if mod_upper_bound <= 7:
    str_upper_bound = 4
elif mod_upper_bound > 7 and mod_upper_bound <=10:
    str_upper_bound = 3
elif mod_upper_bound > 10 and mod_upper_bound <=15:
    str_upper_bound = 2
else:
    str_upper_bound = 1

str_bounds = [str_lower_bound,str_upper_bound]
mod_bounds = [mod_lower_bound,mod_upper_bound]





client = MongoClient()  # On local client
dbName = 'test'
dbCollection = 'y16m03d28_1000'
db = client[dbName]
runsCollection = db[dbCollection]
runCount = 0
db.runsCollection.delete_many({})
bounds = [str_bounds,mod_bounds,[10,45],[0,359]] # Must be set for each variable
#
#
maxEvaluations = 100
borg = bg.Borg(4, 3, 0, solar_opt)
borg.setBounds(*bounds)

epsilon1 = 0.01  # for total cost (obj 1)
epsilon2 = 0.01  # Installed Cost
epsilon3 = 0.01 # Payback 
epsilon4 = 0.01 # % of Satisfied Load
borg.setEpsilons(epsilon1,epsilon2,epsilon3) 
result = borg.solve({"maxEvaluations":maxEvaluations})
solutionDict = {}
solutionNumber = 1
for solution in result:
    solution.display()  # keep this for now just in case
    solutionVariableList = solution.getVariables()
    solutionDict['strings'] = solutionVariableList[0]
    solutionDict['modules'] = solutionVariableList[1]
    solutionDict['tilt'] = solutionVariableList[2]
    solutionDict['azimuth'] = solutionVariableList[3]
    solutionObjectiveList = solution.getObjectives()
    solutionDict['npv'] = solutionObjectiveList[0]
    solutionDict['install_cost'] = solutionObjectiveList[1]
    solutionDict['solar_fraction'] = solutionObjectiveList[2]
    solutionNumber += 1
    doc_id = db.runsCollection.insert_one(solutionDict)
cursor = db.runsCollection.find()
for document in cursor:
    print(document['strings'])
    
    
    
    
    
#    with open(os.path.join(directory, 'solution_borg.csv'), 'w') as csvfile:
#        writer = csv.DictWriter(csvfile, fieldnames = ["Net Present Value", "Installed Cost", "Payback Period","Percent of Annual Load Satisfied"], delimiter = ',')
#        writer.writeheader()
#        wr = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
#        wr.writerow(results_borg)
#
