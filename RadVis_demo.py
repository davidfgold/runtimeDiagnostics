# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 13:26:30 2020

@author: dgold
"""

from yellowbrick.features import RadViz
from yellowbrick.features import Manifold
from runtime_visualization_functions import *
import numpy as np
import matplotlib.pyplot as plt


runtime = read_runtime('DTLZ2_5obj_S1.runtime', 50000, 1000, 5)

#plot runtime snapshots at 1000, 5000, 10000 and 50,0000 NFE
# runtime reports every 1000 NFE, zero indexed so indicies are:
fig, axes = plt.subplots(2,2, figsize=(12,8))
j=0
for i, NFE in enumerate([0 ,4, 9, 49]):
    plot_Radvis(runtime['Objectives'][NFE], axes[int(i/2), j], 'NFE = ' + str(runtime['NFE'][NFE]))
    if i == 1:
        j=0
    else:
        j+=1
plt.savefig('RadVisEx.png', bbox_inches='tight')