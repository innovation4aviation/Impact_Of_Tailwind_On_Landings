#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 09:51:07 2019

@author: chao2
"""
#This code permits to count the number of flights with a specific wind intensity
#In order to do more khi square test

#longlanding
#from the LongLandings_Information.txt file
list_nb = [15, 10, 18, 38, 22, 15, 13, 5, 3, 3, 1, 1, 1, 1]
list_intensity = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 16.0]

#tailwind
#from the Tailwind_Information.txt file
#list_nb = [5955, 4805, 5273, 6365, 5874, 5056, 5008, 3710, 3508, 2853, 3011, 1521, 1468, 810, 688, 392, 325, 191, 126, 106, 60, 49, 29, 19, 15, 6, 7, 1, 1, 1, 2]
#list_intensity = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0, 21.0, 22.0, 23.0, 24.0, 25.0, 26.0, 27.0, 28.0, 30.0, 34.0]

nb_total = 0

compteur = 0
for i in range(len(list_intensity)):
    nb_total += list_nb[i]
    if list_intensity[i] < 10:
        compteur += list_nb[i]
print(nb_total - compteur)
