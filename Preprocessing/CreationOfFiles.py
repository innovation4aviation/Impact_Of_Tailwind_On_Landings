#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 15:45:43 2019

@author: chao2
"""

def date_file(nb_day_february, year):
    'function to create the dates.txt file with the list of the dates'
    
    month_31_days = ['01', '03', '05', '07', '08', '10', '12']
    month_30_days = ['04', '06', '09', '11']
    
    months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    days = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']
    
    file = open('dates'+".txt", "a")
    
    for i in months:
        if i in month_31_days:
            for j in range(31):
                file.write(year[2:] + '-' + i + '-' + days[j])
                file.write('\n')
        elif i in month_30_days:
            for j in range(30):
                file.write(year[2:] + '-' + i + '-' + days[j])
                file.write('\n')
        else:
            for j in range(nb_day_february):
                file.write(year[2:] + '-' + i + '-' + days[j])
                file.write('\n')
    file.close()
    
    return None


date_file(28, '2018')
#--------------------------------------------------------------------------------------------------------------

def airport_file():
    'function to create the airports.txt file with the list of the useful airports'
    
    list_airports = ["SKBO","SLLP","SKPE","SKCG","SKEJ","SKBQ","SKNV","SKYP","SKVV","SKCO","SKBG","SKLT","SKSM","SKCL","KIAD","MDPC","SKMD","SKSP","SUMU","SBGL","TNCA","SKCC","MGGT","KMCO","MDSD","SKFL","SCEL","SPJC","SKPP","SKAR","KMIA","MMMX","SKMR","KLAX","SKRH","SBGR","SKVP","KJFK","MSLP","SKPS","SKMZ","EGLL","MUHA","LEMD","MMUN","SKRG","SKIB","TJSJ","LEBL","SAEZ","KFLL","SABE","TNCC","KBOS","SAAR","MPTO","SEGU","SAZM","SEQM","MHTG","KEWR","CYYR","LIMC","MROC","MMPR","MMGL","KVCV","SKCZ","EDDM","KORD"]
    
    file = open('airports'+".txt", "a")
    for i in list_airports:
        file.write(i)
        file.write('\n')
       
    file.close()
    
    return None

airport_file()