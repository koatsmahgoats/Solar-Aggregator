# -*- coding: utf-8 -*-
"""
Created on Sun Mar 20 21:05:23 2016

@author: Koats
"""
import os
import csv

fire = [[0,1,1,1,1],0,[0,2]]

directory = os.getcwd()
with open(os.path.join(directory, 'singlesolar.csv'), 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames = ["npv", "adjusted_installed_cost", "lcoe_real","lcoe_nom","payback","lifetime_load","year1_electric_load","savings_year1","elec_cost_with_system_year1","elec_cost_without"], delimiter = ',')
    writer.writeheader()
    wr = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
    wr.writerow(fire)
#with open('singlesolar.csv', 'w') as myfile:
    