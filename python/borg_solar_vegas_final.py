# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 17:17:42 2016

This model is designed to use a sequence of NREL SAM SSC SDK pvsamv1, utilityrate, 
and cashloand modules to model the performance of a residential rooftop solar 
system. The model is designed to handle systems 10kW of capacity and below. The model
takes in TMY2, local utility rate, OpenEI load profile data to produce NPV, net capital cost, and 
solar fraction as outputs for the system. Performance model is defined in the solar_opt
function. The BORG MOEA python wrapper is used to iterate through the function and
generate Pareto optimal results for the specified location to create an investment
tradeoff curve. Results are stored in MongoDB collections for further analysis.

@author: Dakota Pekerti, Swarthmore College
"""

import string, sys, struct
from ctypes import * # Ctypes library
import sscapi # NREL SSC SDK API
from pymongo import MongoClient # MongoDB 
import borg as bg # BORG Modules
import time # Time library

c_number = c_float # must be c_double or c_float depending on how defined in sscapi.h

ssc = sscapi.PySSC()
print('Computer = ', sys.platform)
print('Version: {0}'.format(ssc.version()))


# Solar Model Function
def solar_opt(*variables):

    global cost_per_watt # Cost per watt
    global max_inverter # Max inverter voltage
    global mppt_low_inverter # Max Power Point Inverter
    global mod_temp_coeff # Module Temperature Coefficient
    global mod_nom_voc # Module Nominal Open Circuit Voltage
    global runCount # Run Counter
    global nm_enabled # Net Metering Enabled Boolean
    # Initializes data creation module for 
    analysis_period = 25 # Average solar system lifespan
    degradation = [0.5 for x in range(analysis_period)] # Average degradation selection  
    panel_num = int(variables[1]) * int(variables[0]) # Number of Panels
    install_cost = panel_num *315 * cost_per_watt # Install cost in $
    system_capacity = panel_num*315/1000 # System Capacity in kWh
    inverter_num = int(variables[0]) # Number of inverters 
    dat = ssc.data_create() # API Data Creation
    #######Weather Data#############################
    # Pulls from TMY data storage
    ssc.data_set_string(dat, 'solar_resource_file', '../../languages/python/725090TYA.csv')
    ssc.data_set_string(dat, 'file_name', '../../languages/python/725090TYA.csv')

    ######Simulation Parameters ######################
    # Lifetime Simulation Boolean
    ssc.data_set_number(dat, 'pv_lifetime_simulation', 1)
    # Analysis Period Length
    ssc.data_set_number(dat, 'analysis_period', analysis_period)
    # DC degregation Rate %
    ssc.data_set_array(dat, 'dc_degradation', degradation)
    # Snow Model Toggle    
    ssc.data_set_number(dat, 'en_snow_model', 0)
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
    # Enables misaligned panels
    #Boolean
    ssc.data_set_number(dat, 'enable_mismatch_vmax_calc', 0)
    # Photovoltaic module model specification
    # 0=spe,1=cec,2=6par_user,3=snl,4=sd11-iec61853
    ssc.data_set_number(dat, 'module_model', 1)
    # Inverter Module
    # 0=cec,1=datasheet,2=partload
    ssc.data_set_number(dat, 'inverter_model', 1)
    
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
    ##### SMA 4000US Setup from SAM Model
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
    ssc.data_set_number(dat, 'cec_area',2.19384 )
    # Temperature coefficient adjustment
    ssc.data_set_number(dat, 'cec_adjust',-0.478)
    # Short circuit current temperature coefficient
    ssc.data_set_number(dat, 'cec_alpha_sc',0.071 )
    # Open circuit voltage temperature coefficient
    ssc.data_set_number(dat, 'cec_beta_oc', -0.362)
    # Maximum power point temperature coefficient
    ssc.data_set_number(dat, 'cec_gamma_r', -0.478)
    # Maximum power point current
    ssc.data_set_number(dat, 'cec_i_mp_ref', 7.9)
    # Light current
    ssc.data_set_number(dat, 'cec_i_l_ref', 8.51)
    # Saturation current
    ssc.data_set_number(dat, 'cec_i_o_ref', 0.000000001111)
    # Short circuit current
    ssc.data_set_number(dat, 'cec_i_sc_ref', 8.5)
    # Number of cells in series
    ssc.data_set_number(dat, 'cec_n_s', 80)
    # Series resistance
    ssc.data_set_number(dat, 'cec_r_s', 0.395)
    # Shunt resistance
    ssc.data_set_number(dat, 'cec_r_sh_ref', 331.78)
    # Maximum power point voltage
    ssc.data_set_number(dat, 'cec_v_mp_ref', mod_nom_vmp)
    # Nonideality factor a
    ssc.data_set_number(dat, 'cec_a_ref', 2.1635)
    # Open circuit voltage
    ssc.data_set_number(dat, 'cec_v_oc_ref', mod_nom_voc)
    # Standoff mode
    ssc.data_set_number(dat, 'cec_standoff', 6)
    # Array mounting height
    ssc.data_set_number(dat, 'cec_height', 0)
    # Cell temperature model selection
    ssc.data_set_number(dat, 'cec_temp_corr_mode', 0)
    # Nominal operating cell temperature
    ssc.data_set_number(dat, 'cec_t_noct', 46.3)

    ##############Altered Parameters###########################
    # Tilt of Subarray 
    ssc.data_set_number(dat,'subarray1_tilt', variables[2])
    # Nameplate Capacity
    ssc.data_set_number(dat, 'system_capacity', system_capacity)
    #system_size = system_size + 0.1
    ssc.data_set_number(dat, 'modules_per_string', int(variables[1]))
    #Strings in parallel    
    ssc.data_set_number(dat, 'strings_in_parallel',int(variables[0]))
    # Number of Inverter
    ssc.data_set_number(dat, 'inverter_count', inverter_num)
    # Azimuth of subarray 
    #0=N,90=E,180=S,270=W
    ssc.data_set_number(dat,'subarray1_azimuth', variables[3])

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
        
        gen = ssc.data_get_array(dat,"gen") # Grab hourly AC generated energy in kWh
        annual_energy = ssc.data_get_number(dat,"annual_energy") # Grab annual energy in kWh
    
    ssc.module_free(pvsamv1) # Free pvsamv1 module and memory space
    ############ Utility Rate ###############################
    
    load_data = [] # Load data 
    # Grabs Load Data from csv file
    with open('USA_MA_Boston-Logan.Intl.AP.725090_TMY3_BASE.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        next(readCSV)
        for row in readCSV:
            load_data.append(float(row[1]))
    
    # Analysis Period
    ssc.data_set_number(dat,"analysis_period", analysis_period)
    # System Use Lifetime Output
    ssc.data_set_number(dat,"system_use_lifetime_output", 1)
    # Gen
    ssc.data_set_array(dat,"gen", gen)
    #Load
    ssc.data_set_array(dat,"load", load_data)
    # Inflation Rate %
    ssc.data_set_number(dat,"inflation_rate", 2.5)
    # Degradation %
    ssc.data_set_array(dat,"degradation", degradation)
    # Set Load Escalation Array
    ssc.data_set_array(dat,"load_escalation", [1])
    # Excess Monthly Energy Handling
    # 0=Rollover energy,1=Rollover dollars
    ssc.data_set_array(dat,"rate_escalation", [0])
    #Enable Net Metering
    ssc.data_set_number(dat,"ur_enable_net_metering",nm_enabled)
    # Excess Monthly Rollover Energy
    # 0=Rollover energy,1=Rollover dollars
    ssc.data_set_number(dat,"ur_excess_monthly_energy_or_dollars",0)
    # Net Metering Year-end Sell Rate
    ssc.data_set_number(dat,"ur_nm_yearend_sell_rate", nm_sell_rate)
    # Monthly Fixed Charge $
    ssc.data_set_number(dat,"ur_monthly_fixed_charge", 6.43)
    # Flat Buy Rate $
    ssc.data_set_number(dat,"ur_flat_buy_rate", 0.09684)
    # Flat Sell Rate $
    ssc.data_set_number(dat,"ur_flat_sell_rate", 0)
    # Monthly Minimum Charge $
    ssc.data_set_number(dat,"ur_monthly_min_charge", 0)
    # Annual Monthly Minimum Charge $
    ssc.data_set_number(dat,"ur_annual_min_charge", 0)
    
    # Create utilityrate module
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
        annual_energy_value = ssc.data_get_array(dat,"annual_energy_value") # Energy value of solar energy in $
        annual_electric_load = ssc.data_get_array(dat,"annual_electric_load") # Annual electric load in kWh
        elec_cost_with_system = ssc.data_get_array(dat,"elec_cost_with_system") # Electrical cost in system #
        elec_cost_without_system = ssc.data_get_array(dat,"elec_cost_without_system") # Electric cost without system in $
        lifetime_load = ssc.data_get_array(dat,"lifetime_load") # Load in kWhh
        elec_cost_with_system_year1 = ssc.data_get_number(dat,"elec_cost_with_system_year1") # Electric Cost with System for year 1
        elec_cost_without_system_year1 = ssc.data_get_number(dat,"elec_cost_without_system_year1") # Electric Cost without System
        savings_year1= ssc.data_get_number(dat,"savings_year1") # Electric Savings in #
        year1_electric_load =ssc.data_get_number(dat,"year1_electric_load") # Year 1 Electric Load 
        year1_hourly_load = ssc.data_get_array(dat,"year1_hourly_load") # Year 1 hourly electric load
        year1_monthly_cumulative_excess_generation = ssc.data_get_array(dat, "year1_monthly_cumulative_excess_generation") #kWh/mo
    ssc.module_free(utilrate) # Free utility rate module and memory
    
    ############ Cash Loan ##################################
    #Analysis Period
    ssc.data_set_number(dat,"analysis_period", analysis_period)
    # Federal Tax Rate
    ssc.data_set_number(dat,"federal_tax_rate", 30)
    # State Tax Rate
    ssc.data_set_number(dat,"state_tax_rate", 5.1) ##########
    # Real Discount Rate
    ssc.data_set_number(dat,"real_discount_rate", 5.5)
    # Inflation Rate
    ssc.data_set_number(dat,"inflation_rate", 2.5)
    # Debt Fraction %
    ssc.data_set_number(dat,"debt_fraction", 100)
    # Production-based O&M Amount
    ssc.data_set_array(dat,"om_production", [0])
    # Production-based O&M Escalation
    ssc.data_set_number(dat,"om_production_escal", 0)
    # Capacity-based O&M amount
    ssc.data_set_array(dat,"om_capacity", [20])
    # Capacity-based O&M escalation
    ssc.data_set_number(dat,"om_capacity_escal", 2.5)
    # Insurance Rate %
    ssc.data_set_number(dat,"insurance_rate", 1)
    # Investment Tax Credit Federal %
    ssc.data_set_number(dat,"itc_fed_percent", 30)
    # ITC State Percent
    ssc.data_set_number(dat,"itc_sta_percent", 15)
    # System Capacity
    ssc.data_set_number(dat,"system_capacity", system_capacity)
    #Loan Term
    ssc.data_set_number(dat,"loan_term",analysis_period)
    #Loan Interest Rate %
    ssc.data_set_number(dat,"loan_rate",3.25)
    # Market Type
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
        
        lcoe_real = ssc.data_get_number(dat,"lcoe_real") # Real Levelized Cost of electricity $
        lcoe_nom = ssc.data_get_number(dat,"lcoe_nom") # Nominal Levelized Cost of Electricity $
        payback = ssc.data_get_number(dat,"payback") # Payback Period in Years
        adjusted_installed_cost = ssc.data_get_number(dat,"adjusted_installed_cost") # Adjusted installed cost $
        npv = ssc.data_get_number(dat,"npv") #Net present value in $
###################### Solar Fraction and Net Metering Credit for Year 1

    year1_excess_energy = sum(year1_monthly_cumulative_excess_generation) # Monthly generation in year 1
    year1_excess_dollars = year1_excess_energy * nm_sell_rate # Excess $ for year 1

    grid_energy = [] # Grid Energy 
    
    # Net Metering Solar Fraction Calculations
    for i in range(1,len(load_data)):
        if load_data[i]-gen[i] > 0:
            grid_energy.append(load_data[i]-gen[i])
        elif load_data[i]-gen[i] <= 0 or gen[i] < 0:
            grid_energy.append(0)
    if nm_enabled == 0:
        annual_avg_solar_fraction = (1 - (sum(grid_energy)/year1_electric_load))*100 #No net metering solar fraction
    elif nm_enabled == 1:
        annual_avg_solar_fraction = (annual_energy/year1_electric_load)*100 # Net metering solar fraction
####### Iterate and return results###############
    array_out = [annual_electric_load,lifetime_load,elec_cost_without_system,elec_cost_with_system, annual_energy_value,year1_hourly_load]
    single_out = [lcoe_real,lcoe_nom, savings_year1,elec_cost_with_system_year1,elec_cost_without_system_year1, year1_electric_load, year1_excess_energy, year1_excess_dollars]
    results_borg = [-1*npv,adjusted_installed_cost,-1*annual_avg_solar_fraction]
 
    ssc.module_free(cashloan)
    ssc.data_free(dat)
    runCount += 1 # Add to run count
    return results_borg # Return Results
################################################

"""
MAIN PROGRAM SEGMENT
"""

start = time.clock() # Start Timing Code

# Ask for net metering input
nm_enabled = int(raw_input("Enable Net Metering? 0= no, 1 = yes: "))
if nm_enabled == 0: # Net metering Disabled
    net_meter_status = " net metering disabled"
elif nm_enabled ==1: # Net Metering Enabled
    net_meter_status = " net metering enabled"
else:
    print("Net metering must be enabled or disabled. Exiting simulation..")
    exit()
nm_sell_rate= 0.20278 # Net Metering Excess Energy Sell rate


min_temp= -7.72 # Min Operating Temperature of Solar Panel
max_temp = 23.89 # Max Operating Temperature of Solar Panel
cost_per_watt = 3.09 # National Average Cost Per Watt
max_inverter_v= 600 # Max inverter voltage
mppt_low_inverter = 250 # Module max power point low inverter
mod_temp_coeff = -0.177 # Module temperature coefficient
mod_nom_voc = 49.2 # Module Nominal Open Circuit Voltage
mod_nom_vmp = 39.8 # Module Nominal Max Power Voltage

# Module per String Lower Bound Limit Constricted to Inverter MPPT
mod_lower_bound = int(round(mppt_low_inverter/ (mod_nom_vmp - ((max_temp-25) * mod_temp_coeff)))) +1
# Module per String Upper Bound Limit Constricted to Max inverter Voltage
mod_upper_bound = int(max_inverter_v/ (mod_nom_voc + ((max_temp-25) * mod_temp_coeff)))
# Module Error Message
if mod_lower_bound <= 0 or mod_upper_bound <= 0:
    print ("Module Bound Error, cannot be less than zero")
    exit()

# String * modules must be less than 30
str_lower_bound = 1 
if mod_upper_bound <= 7: 
    str_upper_bound = 4 
elif mod_upper_bound > 7 and mod_upper_bound <=10:
    str_upper_bound = 3
elif mod_upper_bound > 10 and mod_upper_bound <=15:
    str_upper_bound = 2
else:
    str_upper_bound = 1


str_bounds = [str_lower_bound,str_upper_bound] # String Bound Limits
mod_bounds = [mod_lower_bound,mod_upper_bound] # Module Per String Bounds


string_num = [] # String Num
mod_num = [] # Module num
tilt_angle = [] # Tilt Angle
azimuth_angle = [] # Azimuth Angle
npv_final = [] # NPV 
install_cost_final = [] # Install Cost
solar_fraction_final = [] # Solar Fraction



client = MongoClient()  # On local client
dbName = 'boston' # Database name
dbCollection = str(raw_input("Please enter a unique collection name for your data: ")) # DB input for collection
db = client[dbName]
borg_solar_opt = db[dbCollection]
borg_solar_opt.delete_many({})
print("Collection cleared")
runCount = 0
bounds = [str_bounds,mod_bounds,[10,45],[0,359]] # Bounds must be set for each variable
maxEvaluations = int(raw_input("Please enter the maximum number of evaluations you would like BORG to run for as an integer: ")) # Max Evals
borg = bg.Borg(4, 3, 0, solar_opt) # Initatie Borg Runs (vars,objs,)
borg.setBounds(*bounds) # Set Boundary Limits for Variables

epsilon1 = 0.01  # for total cost (obj 1)
epsilon2 = 0.01  # Installed Cost
epsilon3 = 0.01 # % of Satisfied Load
borg.setEpsilons(epsilon1,epsilon2,epsilon3) # Set Borg Epsilons
result = borg.solve({"maxEvaluations":maxEvaluations}) # Set Solutions Variable
solutionDict = {} # Dictionary Form of Solution for MongoDB Input
solutionNumber = 1 # Solution Index
for solution in result:
    solution.display()  # keep this for now just in case
    solutionVariableList = solution.getVariables() # Solution variable list
    solutionDict['strings'] = solutionVariableList[0] # Strings Variable
    solutionDict['modules'] = solutionVariableList[1] # Module Variable
    solutionDict['tilt'] = solutionVariableList[2] # Tilt Variable 
    solutionDict['azimuth'] = solutionVariableList[3] # Azimuth Variable 
    solutionObjectiveList = solution.getObjectives() # Solution Objective List
    solutionDict['npv'] = solutionObjectiveList[0] # Net Present Value
    solutionDict['install_cost'] = solutionObjectiveList[1] # Net Capital Cost
    solutionDict['solar_fraction'] = solutionObjectiveList[2] # solar Fraction
    solutionNumberStr = str(solutionNumber) # Turn solution index into string for id
    solutionDict['_id'] = solutionNumberStr # Set ID
    doc_id = borg_solar_opt.insert_one(solutionDict) # Insert Solution as Doc into MongoDB
    solutionNumber += 1 # Iterate Index
    
# Completion
print("Testing Complete, Data stored in MongoDB for " + str(maxEvaluations) + " runs case with " + net_meter_status )
end = time.clock() # End time record
timelapsed = (end-start)/60 # Time Elapsed in Minutes
print('Simulation took ' + str(timelapsed) + ' minutes')
print('Here is your collection name: ' + dbCollection )

