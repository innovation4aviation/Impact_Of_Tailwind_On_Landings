# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 14:03:21 2019

@author: Maël Akouz
"""

class CatTab :
    "Provide functions to classify metar information in dictionaries"

    def __init__(self,clee,liste) :
        "Provide an object with an HashMap, the type of the HashMap's key and the type of data in this HashMap (under the argument 'legend')."
        self.key = clee
        self.legend = liste
        self.htab = {}
    
    def size(self) :
        "Give the size of the HashMap."
        s=0
        for key in self.htab.keys() :
            s=s+1
        return s
    
    def database(txt) :
        Wind = CatTab('{ICAO Code + Date}',('Hour','Wind Information'))
        for line in txt :
            l = line.split(' ')
            l[-1] = l[-1].split('\n')[0]
            key = l[0]+l[-1]
            hour = ''
            wind = ''
            for word in l[1:-1] :
                if 'Z' in word and len(word)==7 :
                    hour = word
                if 'KT' in word :
                    wind = word
            if key in Wind.htab :
                Wind.htab[l[0]+l[-1]].append((hour,wind))
            else :
                Wind.htab[l[0]+l[-1]] = [(hour,wind)]
        return Wind
                

#txt = open('/home/chao2/PROJECTS_JUPITER_NOTEBOOK/PythonMETAR/Preprocessing/metar_infos_airports.txt','r')
#txt = txt.readlines()
#Wind = CatTab.database(txt)
