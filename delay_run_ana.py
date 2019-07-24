# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 00:00:54 2019

@author: protoDUNE
"""

import numpy as np
import os
from sys import exit
import os.path
import math
import time

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
import matplotlib.mlab as mlab


import pickle
fn = "D:\ColdADC\Data_chn0_dly1.bin"
with open (fn, 'rb') as fp:
    chns = pickle.load(fp)
    
fig = plt.figure(figsize=(16,9))
n = 400
plt.plot(np.arange(n), chns[0][0:n])
plt.scatter(np.arange(n), chns[0][0:n])

#plt.savefig("d:\abc.png")
plt.show()

print ("xxxx")
#plt.close()

