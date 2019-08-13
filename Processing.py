#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 14:16:52 2019

@author: Marie1
"""
from datetime import datetime
import csv
import matplotlib.pyplot as plt
import numpy as np
from Wind_Dict import CatTab

def Last_Heading(filename, ident, date):
    'function to get the last heading, the airport and the date of a flight'
    
    flight_data = None
    
    #to get the right flight
    with open(filename, newline='') as file:
        #the number of lines is equal to the number of flights
        for line in file:
            position_id_debut = line.find('ident":"')
            new_line = line[position_id_debut:-1]
            position_id_fin = new_line.find(",") +len(line[0:position_id_debut])
            id_line = line[position_id_debut+len('ident":"'):position_id_fin-1]
            
            position_times_debut = line.find('times":')
            new_line = line[position_times_debut:-1]
            position_times_fin = new_line.find(',')+len(line[0:position_times_debut])
            times_line = line[position_times_debut+len('times":')+1:position_times_fin]
            date_line = str(datetime.fromtimestamp(float(times_line)))[0:10]

            if id_line == ident and date_line == date:
                flight_data = line
    file.close()
    
    #if there is no information about the flight in the json file
    if flight_data == None:
        return None
    
    #to get the flight data : headings
    position_heading_debut = flight_data.find('headings":')
    new_flight_data = flight_data[position_heading_debut:-1]
    position_heading_fin = new_flight_data.find(']')+len(flight_data[0:position_heading_debut])
    str_heading_data = flight_data[position_heading_debut+len('headings":')+1:position_heading_fin]
    
    #to find the airport
    position_dest_debut = flight_data.find('dest":')
    new_flight_data = flight_data[position_dest_debut:-1]
    position_dest_fin = new_flight_data.find(',')+len(flight_data[0:position_dest_debut])
    airport = flight_data[position_dest_debut+len('dest":')+1:position_dest_fin-1]
    
    #to find the date
    position_times_debut = flight_data.find('times":')
    new_flight_data = flight_data[position_times_debut:-1]
    position_times_fin = new_flight_data.find(']')+len(flight_data[0:position_times_debut])
    str_times_data = flight_data[position_times_debut+len('times":')+1:position_times_fin]
    
    #transformation of string data in float in a list
    nb_points = str_heading_data.count(',') +1
    heading_data = []
    times_data = []
    compteur = 0
    
    while compteur < nb_points:
        #headings
        position_heading = str_heading_data.find(",")
        heading = str_heading_data[0:position_heading]
        new_str_heading_data = str_heading_data[position_heading+1:]
        if compteur == nb_points-1 :
            heading = new_str_heading_data
        if heading != 'null':
            heading = float(heading)
        str_heading_data = new_str_heading_data
        heading_data.append(heading)
        
        #times
        position_times = str_times_data.find(",")
        times = str_times_data[0:position_times]
        new_str_times_data = str_times_data[position_times+1:]
        if compteur == nb_points-1 :
            times = new_str_times_data
        if times != 'null':
            times = float(times)
        str_times_data = new_str_times_data
        times_data.append(times)
        
        compteur +=1    
    
    return heading_data[-1], airport, str(datetime.fromtimestamp(times_data[-1]))

#------------------------------------------------------------------------------------------

def Metar_Info(wind_day, time, heading):
    'function to get the information about the wind for a specific flight from metar format'
   
    if len(wind_day) == 0:
        #no information about this day
        return [None, None, None]
    
    # take first element for sort
    def takeFirst(elem):
        return elem[0]
    
    #to sort the list by hour
    wind_day.sort(key=takeFirst)
    
    #to get the right hour
    position_hour = 0
    for i in range(len(wind_day)):
        if wind_day[i][0][2:4] <= time[0:2]:
            position_hour = i
        
    if wind_day[position_hour][0][2:4] == time[0:2]:
        if wind_day[position_hour][0][4:6] <= time[3:5]:
            position_hour = position_hour
        else:
            if wind_day[position_hour-1][0][2:4] == time[0:2]:
                if wind_day[position_hour-1][0][4:6] <= time[3:5]:
                    position_hour -+ 1
                else :
                    position_hour -+ 2
            else :
                position_hour -+ 1
    
    #to get the information about the wind in the metar format file
    wind =  wind_day[position_hour][1]  
    direction_wind = None
    intensity_wind = None
            
    if wind[0:3] == "VRB":
        #there is no wind
        result = 0
    
    elif wind[0:5].isnumeric() == False:
        #no information about the wind
        return [None, None, None]
            
    else:
        direction_brut = int(wind[0:3])
        #to have the wind relative to the runway
        direction_wind = heading-direction_brut
        intensity_brut = int(wind[3:5])
        intensity_wind = round(intensity_brut*np.cos((direction_wind)*np.pi/180),0)
                
        if -90 < direction_wind < +90:
            #tailwind
            result = 1
        else :
            #no tailwind
            result = 0
            
    return [result, direction_wind, intensity_wind]

#------------------------------------------------------------------------------------------
    
def Long_Landings_Flights(list_files):
    'function which permits to get the ident and the date of flights from csv files'
    
    list_long_landings = []
    
    for filename in list_files :
        with open('/home/chao2/PROJECTS_JUPITER_NOTEBOOK/PythonMETAR/Input_LongLandings/'+filename, newline='') as csvfile:
            filereader = csv.reader(csvfile)
            ligne = 0
            for row in filereader:
                infos = []
                for mot in row[2].split(";"):
                    infos.append(mot)
                for mot in row[3].split(";"):
                    if len(mot) > 10:
                        infos.append(mot[0:10])
                    else:
                        infos.append(mot)
                list_long_landings.append(infos)
                if ligne == 0:
                    list_long_landings.pop()
                ligne += 1
            csvfile.close()
    return list_long_landings

#------------------------------------------------------------------------------------------

def csvcount(filename):
    "function which permits to have the number of lines in a file"
    
    with open(filename, 'r') as f:
        i = 0
        for ligne in f:
            i += 1
    return i

def Long_Landings_Wind(filenamejson, list_flight, filename):
    'function which permits to get the impact of the wind on long landings : intensity and direction'
    
    #creation of the metar dictionnary
    txt = open(filename,'r')
    txt = txt.readlines()
    wind_dict = CatTab.database(txt)
    
    #result contains all the flights with wind data
    result = []
    list_intensity = []
    list_direction = []
    
    for flight in range(len(list_flight)):
        ident = list_flight[flight][0]
        date = list_flight[flight][1]
        if Last_Heading(filenamejson, ident, date) != None :
            heading_plane, airport, time_plane = Last_Heading(filenamejson, ident, date)
            time = time_plane[11:]
            heading = int(heading_plane)
            if airport+date[2:] in wind_dict.htab:
                wind_day = wind_dict.htab[airport+date[2:]]
                wind = Metar_Info(wind_day, time, heading)
                if wind[0] != None:
                    result.append(wind)
                if wind[0] == 1:
                    list_intensity.append(wind[2])
                    list_direction.append(wind[1])
    
    #to know the number of long landings with tailwind
    nb_tailwind = 0
    for j in range(len(result)):
        if result[j][0] == 1:
            nb_tailwind += 1
    print("There is {}% of long landings with tailwind.".format(nb_tailwind*100/len(result)))
    
    #to have the information in graphs
    while None in list_intensity:
        del list_intensity[list_intensity.index(None)]
    while None in list_direction:
        del list_direction[list_direction.index(None)]
    list_intensity.sort()
    list_direction.sort()
    
    diff_list_intensity = []
    diff_list_direction = []
    nb_list_intensity = []
    nb_list_direction = []
    
    compteur = 1
    for i in range(len(list_intensity)-1):
        if list_intensity[i] ==list_intensity[i+1]:
            compteur += 1
        else :
            nb_list_intensity.append(compteur)
            diff_list_intensity.append(list_intensity[i])
            compteur = 1
    if list_intensity[-1] in diff_list_intensity:
        nb_list_intensity[-1] += 1
    else :
        nb_list_intensity.append(compteur)
        diff_list_intensity.append(list_intensity[-1])
        
    compteur = 1
    for i in range(len(list_direction)-1):
        if list_direction[i] ==list_direction[i+1]:
            compteur += 1
        else :
            nb_list_direction.append(compteur)
            diff_list_direction.append(list_direction[i])
            compteur = 1
    if list_direction[-1] in diff_list_direction:
        nb_list_direction[-1] += 1
    else :
        nb_list_direction.append(compteur)
        diff_list_direction.append(list_direction[-1])
    
    #to see the different graphs
    y_pos = np.arange(len(diff_list_direction))
    
    size = (6,4)
    fig = plt.figure(figsize = size)
    plt.bar(y_pos, nb_list_direction, align = 'center', alpha = 0.5)
    plt.xticks(y_pos, diff_list_direction, rotation = 90, fontsize = 4)
    plt.ylabel("Number of flights")
    plt.title("Wind direction")
    plt.show()
    fig.savefig('/home/chao2/PROJECTS_JUPITER_NOTEBOOK/PythonMETAR/Output_Graphs/LongLanding_Wind_direction.png', dpi=200)

    y_pos = np.arange(len(diff_list_intensity))
    
    fig2 = plt.figure(figsize = size)
    plt.bar(y_pos, nb_list_intensity, align = 'center', alpha = 0.5)
    plt.xticks(y_pos, diff_list_intensity, rotation = 90, fontsize = 4)
    plt.ylabel("Nunber of flights")
    plt.title("Wind intensity")
    plt.show()
    fig2.savefig('/home/chao2/PROJECTS_JUPITER_NOTEBOOK/PythonMETAR/Output_Graphs/LongLanding_Wind_intensity.png', dpi=200)
    
    #to save the information in a txt file
    fichier = open('/home/chao2/PROJECTS_JUPITER_NOTEBOOK/PythonMETAR/Output_Infos/LongLandings_Information'+".txt", "w")
    fichier.write(str(nb_list_direction))
    fichier.write('\n')
    fichier.write(str(diff_list_direction))
    fichier.write('\n')
    fichier.write(str(nb_list_intensity))
    fichier.write('\n')
    fichier.write(str(diff_list_intensity))
    fichier.write('\n')
    fichier.close()
    
    return None


def Tailwind(filenamejson, filename):
    'function which permits to get the impact of the wind on landings : intensity and direction in txt format'
    
    #creation of the metar dictionnary
    txt = open(filename,'r')
    txt = txt.readlines()
    wind_dict = CatTab.database(txt)

    list_flight = []
    #result contains all the flights with wind data
    result = []
    list_intensity = []
    list_direction = []
    
    #to get the list of all flights
    with open(filenamejson, newline='') as file:
        #the number of flights is equal to the number of lines
        for line in file:
            position_id_debut = line.find('ident":"')
            new_line = line[position_id_debut:-1]
            position_id_fin = new_line.find(",") +len(line[0:position_id_debut])
            id_line = line[position_id_debut+len('ident":"'):position_id_fin-1]
            
            position_times_debut = line.find('times":')
            new_line = line[position_times_debut:-1]
            position_times_fin = new_line.find(',')+len(line[0:position_times_debut])
            times_line = line[position_times_debut+len('times":')+1:position_times_fin]
            date_line = str(datetime.fromtimestamp(float(times_line)))[0:10]
            
            list_flight.append([id_line, date_line])   
    file.close()

    for flight in range(len(list_flight)):
        ident = list_flight[flight][0]
        date = list_flight[flight][1]
        if Last_Heading(filenamejson, ident, date) != None :
            heading_plane, airport, time_plane = Last_Heading(filenamejson, ident, date)
            time = time_plane[11:]
            heading = int(heading_plane)
            if airport+date[2:] in wind_dict.htab:
                wind_day = wind_dict.htab[airport+date[2:]]
                wind = Metar_Info(wind_day, time, heading)
                if wind[0] != None:
                    result.append(wind)
                if wind[0] == 1:
                    list_intensity.append(wind[2])
                    list_direction.append(wind[1])
    
    #to save the information in txt files
    with open('/home/chao2/PROJECTS_JUPITER_NOTEBOOK/PythonMETAR/Output_Infos/Intensity_Tailwind.txt', "w") as file_intensity:
        file_intensity.write(str(list_intensity))
    file_intensity.close()     
    with open('/home/chao2/PROJECTS_JUPITER_NOTEBOOK/PythonMETAR/Output_Infos/Direction_Tailwind.txt', "w") as file_direction:
        file_direction.write(str(list_direction))
    file_direction.close()
    with open('/home/chao2/PROJECTS_JUPITER_NOTEBOOK/PythonMETAR/Output_Infos/Result_Tailwind.txt', "w") as file_result:
        file_result.write(str(result))
    file_result.close()
    
    return None

def Tailwind_Results():
    'function which permits to get the impact of the wind on landings : intensity and direction - graphs and percentage rate'
    
    #to get the data
    with open('/home/chao2/PROJECTS_JUPITER_NOTEBOOK/PythonMETAR/Output_Infos/Intensity_Tailwind.txt', "r") as file_intensity:
        for line in file_intensity :
            list_intensity = line[1:-1]
            list_intensity = list_intensity.split(',')
            for i in range(len(list_intensity)):
                list_intensity[i] = float(list_intensity[i])
    file_intensity.close() 
    
    with open('/home/chao2/PROJECTS_JUPITER_NOTEBOOK/PythonMETAR/Output_Infos/Direction_Tailwind.txt', "r") as file_direction:
        for line in file_direction :
            list_direction = line[1:-1]
            list_direction = list_direction.split(',')
            for i in range(len(list_direction)):
                list_direction[i] = float(list_direction[i])
    file_direction.close()
    
    with open('/home/chao2/PROJECTS_JUPITER_NOTEBOOK/PythonMETAR/Output_Infos/Result_Tailwind.txt', "r") as file_result:
        for line in file_result :
            result = line[1:-1]
            result = result.split('], [')
            result[0] = result[0][1:]
            result[-1] = result[-1][:-1]
            for i in range(len(result)):
                result[i] = result[i].split(',')
                for j in range(len(result[i])):
                    if result[i][j] != ' None':
                        result[i][j] = float(result[i][j])
                    else :
                         result[i][j] = None
    file_result.close()
    
    #to know the number of long landings with tailwind
    nb_tailwind = 0
    for j in range(len(result)):
        #print(result[j])
        if result[j][0] == 1:
            nb_tailwind += 1
    print("There is {}% of landings with tailwind.".format(nb_tailwind*100/len(result)))
    
    #to have the information in graphs
    while None in list_intensity:
        del list_intensity[list_intensity.index(None)]
    while None in list_direction:
        del list_direction[list_direction.index(None)]
    list_intensity.sort()
    list_direction.sort()
    
    diff_list_intensity = []
    diff_list_direction = []
    nb_list_intensity = []
    nb_list_direction = []
    
    compteur = 1
    for i in range(len(list_intensity)-1):
        if list_intensity[i] ==list_intensity[i+1]:
            compteur += 1
        else :
            nb_list_intensity.append(compteur)
            diff_list_intensity.append(list_intensity[i])
            compteur = 1
    if list_intensity[-1] in diff_list_intensity:
        nb_list_intensity[-1] += 1
    else :
        nb_list_intensity.append(compteur)
        diff_list_intensity.append(list_intensity[-1])
        
    compteur = 1
    for i in range(len(list_direction)-1):
        if list_direction[i] ==list_direction[i+1]:
            compteur += 1
        else :
            nb_list_direction.append(compteur)
            diff_list_direction.append(list_direction[i])
            compteur = 1
    if list_direction[-1] in diff_list_direction:
        nb_list_direction[-1] += 1
    else :
        nb_list_direction.append(compteur)
        diff_list_direction.append(list_direction[-1])
    
    #to see the different graphs
    y_pos = np.arange(len(diff_list_direction))
    
    size = (6,4)
    fig = plt.figure(figsize = size)
    plt.bar(y_pos, nb_list_direction, align = 'center', alpha = 0.5)
    plt.xticks(y_pos, diff_list_direction, rotation = 90, fontsize = 4)
    plt.ylabel("Number of flights")
    plt.title("Wind direction")
    plt.show()
    fig.savefig('/home/chao2/PROJECTS_JUPITER_NOTEBOOK/PythonMETAR/Output_Graphs/Tailwind_direction.png', dpi=200)

    y_pos = np.arange(len(diff_list_intensity))
    
    fig2 = plt.figure(figsize = size)
    plt.bar(y_pos, nb_list_intensity, align = 'center', alpha = 0.5)
    plt.xticks(y_pos, diff_list_intensity, rotation = 90, fontsize = 4)
    plt.ylabel("Nunber of flights")
    plt.title("Wind intensity")
    plt.show()
    fig2.savefig('/home/chao2/PROJECTS_JUPITER_NOTEBOOK/PythonMETAR/Output_Graphs/Tailwind_Wind_intensity.png', dpi=200)
    
    #to save the information in a txt file
    fichier = open('/home/chao2/PROJECTS_JUPITER_NOTEBOOK/PythonMETAR/Output_Infos/Tailwind_Information'+".txt", "w")
    fichier.write(str(nb_list_direction))
    fichier.write('\n')
    fichier.write(str(diff_list_direction))
    fichier.write('\n')
    fichier.write(str(nb_list_intensity))
    fichier.write('\n')
    fichier.write(str(diff_list_intensity))
    fichier.write('\n')
    fichier.close()
    
    return None

#------------------------------------------------------------------------------------------

list_long_landings = Long_Landings_Flights(["April_2_data_Avianca.csv",
                   "April_1_data_Avianca.csv", 
                   "february_data_avianca.csv",
                   "ftp_oaci_DEC.csv",
                   "ftp_oaci_FEB.csv",
                   "ftp_oaci_JAN.csv",
                   "ftp_oaci_JULY_AUGS.csv",
                   "ftp_oaci_MAR.csv",
                   "ftp_oaci_NOV.csv",
                   "ftp_oaci_OCT.csv",
                   "June_data_Avianca.csv",
                   "march_data_Avianca.csv",
                   "Mayo_1_data_Avianca.csv",
                   "Mayo_2_data_Avianca.csv"])
filenamejson = "/home/chao2/PROJECTS_JUPITER_NOTEBOOK/PythonMETAR/Input_LongLandings/ava2018.json"
filename = '/home/chao2/PROJECTS_JUPITER_NOTEBOOK/PythonMETAR/Preprocessing/metar_infos_airports.txt'

#Long_Landings_Wind(filenamejson, list_long_landings, filename)
#Tailwind(filenamejson,filename)
#Tailwind_Results()