# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 23:13:57 2016

@author: Koats
"""

import string, sys, struct
from ctypes import *
import os
import sscapi
import numpy as np
import matplotlib.pyplot as plt
import csv

c_number = c_float # must be c_double or c_float depending on how defined in sscapi.h

# Test program 'main'

print('Hello, PySSC')
ssc = sscapi.PySSC()
print('Computer = ', sys.platform)
print('Version: {0}'.format(ssc.version()))


dat = ssc.data_create()

angle = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85 ,90]
azimuth = [0,30,60,90,120,150,180,210,240,270,300,330,359.9]
system_size = 0
inverter = [1,2,3]
panel = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
degradation = [0.5,0.5,0.5,0.5,0.5]
pstring = [1,2,3]

ann = [0]
capacity_factor = []
performance_ratio = []
annual_energy = []

dc_net = []
a = 1
b = 1
#for a in range(len(azimuth)):

    
#######Weather Data#############################
# Pulls from TMY data storage
ssc.data_set_string(dat, 'solar_resource_file', '../../examples/daggett.tm2')

# Simulation Parameter Call
######Simulation Parameters ######################
# Lifetime Simulation Boolean

ssc.data_set_number(dat, 'pv_lifetime_simulation', 1)
# Analysis Period Length
ssc.data_set_number(dat, 'analysis_period', 1)
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
ssc.data_set_number(dat,'mppt_low_inverter', 250)
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
ssc.data_set_number(dat, 'inv_ds_vdcmax', 600)

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
ssc.data_set_number(dat, 'spe_temp_coeff', -0.478)
# Diffuse Fraction
ssc.data_set_number(dat, 'spe_fd', 1)
# Nominal Max power Voltage
ssc.data_set_number(dat, 'spe_vmp', 39.8)
# Nominal Open Circuit Voltage
ssc.data_set_number(dat, 'spe_voc', 49.2)
##########################################
moduledata=[]

paneldata =[]

inverterdata =[]

gen = []

annual_energy_2 = []

annual_energy_3 = []

annual_energy_4 = []

annual_energy_5 = []

annual_energy_6 = []

annual_energy_7 = []

annual_energy_8 = []

annual_energy_9 = []

annual_energy_10 = []


plt.figure()
for c in range(len(inverter)):
    for a in range(len(pstring)):
        panel_num = []
        for b in range(len(panel)):
            total_panel = pstring[a]*panel[b]
            panel_num.append(total_panel)
    #for c in range(inverter)
    #while system_size<7:
    ##############Altered Parameters###########################
            # Tilt of Subarray 
            ssc.data_set_number(dat,'subarray1_tilt', 30)
            # Nameplate Capacity
            ssc.data_set_number(dat, 'system_capacity', 5.0)
            #system_size = system_size + 0.1
            ssc.data_set_number(dat, 'modules_per_string', panel[b])
            #Strings in parallel    
            ssc.data_set_number(dat, 'strings_in_parallel', pstring[a])
            # Number of Inverters
            ssc.data_set_number(dat, 'inverter_count', inverter[c])
            # Azimuth of subarray 
            #0=N,90=E,180=S,270=W
            ssc.data_set_number(dat,'subarray1_azimuth', 180)
        
        ###########################################################
            # run PV system simulation
            mod = ssc.module_create("pvsamv1")
            if ssc.module_exec(mod, dat) == 0:
                print ('PVSAM1 simulation error')
                idx = 1
                msg = ssc.module_log(mod, 0)
                while (msg != None):
                    print ('\t: ' + msg)
                    msg = ssc.module_log(mod, idx)
                    idx = idx + 1
            elif pstring[a] ==1 and inverter[c] ==1:
                annual_energy.append(ssc.data_get_number(dat,"annual_energy"))
                
            elif pstring[a] ==2 and inverter[c] ==1:
                annual_energy_2.append(ssc.data_get_number(dat,"annual_energy"))
                
            elif pstring[a]== 3 and inverter[c] ==1:
                annual_energy_3.append(ssc.data_get_number(dat,"annual_energy"))
            
            elif pstring[a] ==1 and inverter[c] ==2:
                annual_energy_4.append(ssc.data_get_number(dat,"annual_energy"))
                
            elif pstring[a] ==2 and inverter[c] ==2:
                annual_energy_5.append(ssc.data_get_number(dat,"annual_energy"))
                
            elif pstring[a]== 3 and inverter[c] ==2:
                annual_energy_6.append(ssc.data_get_number(dat,"annual_energy"))
            
            elif pstring[a] ==1 and inverter[c] ==3:
                annual_energy_7.append(ssc.data_get_number(dat,"annual_energy"))
                
            elif pstring[a] ==2 and inverter[c] ==3:
                annual_energy_8.append(ssc.data_get_number(dat,"annual_energy"))
                
            elif pstring[a]== 3 and inverter[c] ==3:
                annual_energy_9.append(ssc.data_get_number(dat,"annual_energy"))
            gen.append(ssc.data_get_number(dat,"gen"))
            
            #system.append(system_size)
        
x = panel_num
y = annual_energy
plt.xlabel("Panel #")
plt.ylabel("Annual Energy, kWh")
num_1, =plt.plot(x, annual_energy, label='1 str, 1 inv')
num_2, =plt.plot(x,annual_energy_2, label='2 str, 1 inv')
num_3, =plt.plot(x,annual_energy_3, label='3 str, 1 inv')
num_4, =plt.plot(x, annual_energy_4, label='1 str, 2 inv',linestyle='dashed')
num_5, =plt.plot(x,annual_energy_5, label='2 str, 2 inv', linestyle='dashed')
num_6, =plt.plot(x,annual_energy_6, label='3 str, 2 inv', linestyle='dashed')
num_7, =plt.plot(x, annual_energy_7, label='1 str, 3 inv', linestyle='dotted')
num_8, =plt.plot(x,annual_energy_8, label='2 str, 3 inv', linestyle='dotted')
num_9, =plt.plot(x,annual_energy_9, label='3 str, 3 inv', linestyle='dotted')
plt.legend(loc='upper left', bbox_to_anchor=(1.0, 1.0),handles=[num_1,num_2,num_3,num_4,num_5,num_6,num_7,num_8,num_9])


#plt.figure()
#x = inverter
#y = capacity_factor
#plt.xlabel("Panel #")
#plt.ylabel("Capacity Factor %")
#plt.plot(x, y)
#
#plt.figure()
#x = inverter
#y = performance_ratio
#plt.xlabel("Panel #")
#plt.ylabel("Performance Ratio")
#plt.plot(x, y)

#    capacity_factor = []
#    performance_ratio = []
#    annual_energy = []
#    dc_net = []

ssc.module_free(mod)
ssc.data_free(dat)

#3/17/2016 Utility Rate

elec_cost_with_system =[]

elec_cost_without_system =[]

elec_cost_with_system_year1 =[]

elec_cost_without_system_year1 =[]

savings_year1 =[]

year1_electric_load =[]

year1_hourly_e_tofromgrid =[]

year1_hourly_load =[]

lifetime_load =[]

year1_hourly_p_tofromgrid =[]


#3/17/2016 Cash Loan
lcoe_real =[]

lcoe_nom=[]

payback =[]


present_value_oandm =[]

present_value_oandm_nonfuel =[]

present_value_fuel =[]

present_value_insandproptax=[]

adjusted_installed_cost =[]