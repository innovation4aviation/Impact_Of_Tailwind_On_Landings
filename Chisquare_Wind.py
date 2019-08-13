#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 10:03:57 2019

@author: chao2
"""

import numpy as np
from scipy import stats

#This code permits to do the khi-square test
# If p-value > 0.05 , the distribution between the two events is the same

#longlanding // tailwind
a1 = [146, 397]
a2 = [57089, 79227]
#longlanding // tailwind 0-2
a3 = [4, 397]
a4 = [8824, 79227]

dice = np.array([a3, a4])

chi2_stat, p_val, dof, ex = stats.chi2_contingency(dice)

print("---Chi2 Stat---")
print(chi2_stat)
print("---Degrees of Freedom---")
print(dof)
print("---P-Value---")
print(p_val)
print("---Contingency Table---")
print(ex)
