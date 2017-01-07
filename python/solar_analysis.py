# -*- coding: utf-8 -*-
"""
Created on Sun Apr 10 13:46:57 2016

This code utilizes the matplotlib function in order to 

@author: Koats
"""
import matplotlib.pyplot as plt
import numpy as np
from pymongo import MongoClient
from mpl_toolkits.mplot3d import Axes3D

# Set variables for collection 1
number_collections = 0
panel_num = []
string_num = []
mod_num = []
tilt_angle = []
azimuth_angle = []
npv_final = []
install_cost_final = []
solar_fraction_final = []

# Set variables for collection 2
panel_num2 = []
string_num2 = []
mod_num2 = []
tilt_angle2 = []
azimuth_angle2 = []
npv_final2 = []
solar_fraction_final2 = []
install_cost_final2 = []

# Set variables for collection 3
panel_num3 = []
string_num3 = []
mod_num3 = []
tilt_angle3 = []
azimuth_angle3 = []
npv_final3 = []
solar_fraction_final3 = []
install_cost_final3 = []

# MongoDB collection access
client = MongoClient()  # On local client
dbName = 'boston'
dbCollection = str(input("Please enter the name of the 1st collection you wish to analyze: "))
db = client[dbName]
borg_solar_opt = db[dbCollection]

# First Collection Variable Assembly
cursor = borg_solar_opt.find()
for document in cursor:
    string_num.append(int(document['strings']))
    mod_num.append(document['modules'])
    tilt_angle.append(document['tilt'])
    azimuth_angle.append(document['azimuth'])
    npv_final.append(-document['npv'])
    solar_fraction_final.append(-document['solar_fraction'])
    install_cost_final.append(document['install_cost'])
X = np.asarray(npv_final)
Y = np.asarray(install_cost_final)
Z = np.asarray(solar_fraction_final)
for i in range(0,len(mod_num)):
    panel_num.append(int(string_num[i]*mod_num[i])) # Total Number of Panels
panel_num = np.asarray(panel_num)
mod_num = np.asarray(mod_num)
string_num = np.asarray(string_num)
tilt_angle = np.asarray(tilt_angle)
azimuth_angle = np.asarray(azimuth_angle)

# Ask about multiple collections
comparison_enable = int(input("Do you wish to Analyze Multiple Collections? yes=1,no=0: "))
if comparison_enable == 1:
    number_collections = int(input("Please enter the number of additional collections you would like to compare, Max 2: "))
elif comparison_enable == 0:
    number_collections = 0 
else:
    print("Not a valid response, please reply with y or n")
    exit()

# Assemble arrays from MongoDB for multiple collections
# Two collection scenario
if number_collections == 1:
    dbCollection = str(input("Please enter the name of the 2nd collection you wish to analyze: "))
    borg_solar_opt = db[dbCollection]
    cursor = db.borg_solar_opt.find()
    for document in cursor:
        string_num2.append(int(document['strings']))
        mod_num2.append(document['modules'])
        tilt_angle2.append(document['tilt'])
        azimuth_angle2.append(document['azimuth'])
        npv_final2.append(document['npv'])
        solar_fraction_final2.append(document['solar_fraction'])
        install_cost_final2.append(document['install_cost'])
    X2 = np.asarray(npv_final2)
    Y2 = np.asarray(install_cost_final2)
    Z2 = np.asarray(solar_fraction_final2)
    for i in range(0,len(mod_num2)):
        panel_num2.append(int(string_num2[i]*mod_num2[i])) # Total Number of Panels
    panel_num2 = np.asarray(panel_num2)
    string_num2 = np.asarray(string_num2)
    tilt_angle2 = np.asarray(tilt_angle2)
    azimuth_angle2 = np.asarray(azimuth_angle2)
# Assemble arrays from MongoDB for 3 total collections
elif number_collections ==2:
    dbCollection = str(input("Please enter the name of the 2nd collection you wish to analyze: "))
    borg_solar_opt = db[dbCollection]
    cursor = db.borg_solar_opt.find()
    for document in cursor:
        string_num2.append(int(document['strings']))
        mod_num2.append(document['modules'])
        tilt_angle2.append(document['tilt'])
        azimuth_angle2.append(document['azimuth'])
        npv_final2.append(document['npv'])
        solar_fraction_final2.append(document['solar_fraction'])
        install_cost_final2.append(document['install_cost'])
    X2 = np.asarray(npv_final2)
    Y2 = np.asarray(install_cost_final2)
    Z2 = np.asarray(solar_fraction_final2)
    for i in range(0,len(mod_num2)):
        panel_num2.append(int(string_num2[i]*mod_num2[i])) # Total Number of Panels
    panel_num2 = np.asarray(panel_num2)
    mod_num2 = np.asarray(mod_num2)
    string_num2 = np.asarray(string_num2)
    tilt_angle2 = np.asarray(tilt_angle2)
    azimuth_angle2 = np.asarray(azimuth_angle2)
    dbCollection2 = str(input("Please enter the name of the 3rd collection you wish to analyze: "))
    borg_solar_opt = db[dbCollection]
    cursor = db.borg_solar_opt.find()
    for document in cursor:
        string_num3.append(int(document['strings']))
        mod_num3.append(document['modules'])
        tilt_angle3.append(document['tilt'])
        azimuth_angle3.append(document['azimuth'])
        npv_final3.append(document['npv'])
        solar_fraction_final3.append(document['solar_fraction'])
        install_cost_final3.append(document['install_cost'])
    X3 = np.asarray(npv_final3)
    Y3 = np.asarray(install_cost_final3)
    Z3 = np.asarray(solar_fraction_final3)
    for i in range(0,len(mod_num3)):
        panel_num3.append(int(string_num3[i]*mod_num3[i])) # Total Number of Panels
    panel_num3 = np.asarray(panel_num3)
    mod_num3 = np.asarray(mod_num3)
    string_num3 = np.asarray(string_num3)
    tilt_angle3 = np.asarray(tilt_angle3)
    azimuth_angle3 = np.asarray(azimuth_angle3)
elif number_collections < 0 or number_collections > 2:
    print("Invalid Number of Collections, Terminating..")
    exit()


# Plots Installed Cost Versus NPV
label1 = str(input("Please enter the title for the first graph (Net Capital Cost v NPV): "))
plt.plot(Y,X, 'o')
if number_collections == 1:
    plt.plot(Y2,X2, 'o', color = 'r')
elif number_collections == 2:
    plt.plot(Y2,X2, 'o', color ='r')
    plt.plot(Y3,X3, 'o',color = 'g')
plt.xlabel("Net Capital Cost ($)")
plt.ylabel("NPV ($)")
#plt.axis( [5000, 21000, -12000, -2000])
plt.title(label1, fontdict=None,fontsize = 14, loc='center')

# Plots Installed Cost Versus Solar Fraction
label2 = str(input("Please enter the title for the second graph (Net Capital Cost v Solar Fraction): "))
fig = plt.figure()
plt.plot(Y,Z,'s', color ='b')
if number_collections == 1:
    plt.plot(Y2,X2, 's', 'r')
elif number_collections == 2:
    plt.plot(Y2,X2, 's',color = 'r')
    plt.plot(Y3,X3, 's', color ='g')
plt.xlabel("Net Capital Cost ($)")
plt.ylabel("Solar Fraction (%)")
plt.axis( [5000, 21000, 30, 120 ])
plt.title(label2, fontdict=None,fontsize = 14, loc='center')

# plots 3D graph of all objectives
label3 = str(input("Please enter the title for the 3D graph: "))
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(Y,X,Z)
if number_collections == 1:
    ax.scatter(Y2,X2,Z2, color ='r')
elif number_collections == 2:
    ax.scatter(Y2,X2,Z2, color ='r')
    ax.scatter(Y3,X3,Z3, color = 'g')
ax.set_xlabel('Total Installed Cost ($)')
ax.set_ylabel('NPV ($)')
ax.set_zlabel('Solar Fraction (%)')
ax.set_xlim3d(5000,21000)
ax.set_ylim3d(-12000,-2000)
ax.set_zlim3d(22,38)
ax.set_title(label3, fontdict=None,fontsize = 14, loc='center')

# Plots Solar Panels Versus String/Inverter Count
label4 = str(input("Please enter the title for the fourth graph (Cost vs Panel # and String Count): "))
fig = plt.figure()
plt.plot(Y,string_num,'d', color ='b')
plt.xlabel("Net Capital Cost ($)")
plt.ylabel("Inverter/String Count", color ='b')
plt.ylim([0,3])
plt.tick_params(axis='y', colors='blue')
plt2 = plt.twinx()
plt2.set_ylim([0,25])
plt2.set_xlim([5000, 21000])
plt2.tick_params(axis='y', colors='red')
plt2.plot(Y,panel_num, 's', color = 'r')
if number_collections == 1:
    plt.plot(Y2,string_num2, 'd', 'r')
    plt2.plot(Y2,panel_num2, 's', color = 'r')
elif number_collections == 2:
    plt.plot(Y2,string_num2, 'd',color = 'r')
    plt.plot(Y3,string_num3, 'd', color ='g')
    plt2.plot(Y2,panel_num2, 's', color = 'r')
    plt2.plot(Y3,panel_num3, '^', color = 'g')
plt2.set_ylabel('Panel Number', color ='r')
plt.title(label4, fontdict=None, fontsize=14, loc='center')

# Plots Solar Fraction vs Azimuth and Tilt Angle
label5 = str(input("Please enter the title for the fifth graph (Solar Fraction vs Azimuth and Tilt): "))
fig = plt.figure()
plt.plot(Z,azimuth_angle,'d', color ='b')
plt.xlabel("Solar Fraction (%)")
plt.ylabel("Azimuth (degrees)", color='b')
plt.ylim([0,360])
plt.tick_params(axis='y', colors='blue')
plt2 = plt.twinx()
plt2.set_xlim([22,38])
plt2.set_ylim([0,50])
plt2.tick_params(axis='y', colors='red')
plt2.plot(Z,tilt_angle, 's', color = 'r')
if number_collections == 1:
    plt.plot(Z2,azimuth_angle2, 'd', 'r')
    plt2.plot(Z2,tilt_angle2, 's', color = 'g')
elif number_collections == 2:
    plt.plot(Z2,azimuth_angle2, 'd',color = 'r')
    plt.plot(Z3,azimuth_angle3, 'd', color ='g')
    plt2.plot(Z2,tilt_angle2, 's', color = 'y')
    plt2.plot(Z3,tilt_angle3, '^', color = 'p')
plt2.set_ylabel('Tilt Angle (degrees)', color='r')
plt.title(label5, fontdict=None, fontsize=14, loc='center')

# Plots Installed Cost Versus Solar Fraction
label6 = str(input("Please enter the title for the 6th graph (NPV v Solar Fraction): "))
fig = plt.figure()
plt.plot(X,Z,'s', color ='b')
if number_collections == 1:
    plt.plot(X,Z, 's', 'r')
elif number_collections == 2:
    plt.plot(X2,Z2, 's',color = 'r')
    plt.plot(X3,Z3, 's', color ='g')
plt.xlabel("NPV ($)")
plt.ylabel("Solar Fraction (%)")
plt.title(label6, fontdict=None,fontsize = 14, loc='center')
plt.axis([-12000,-2000,22,38])