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
import statsmodels.api as sm

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
import matplotlib.mlab as mlab

import pickle

def file_list(runpath):
    if (os.path.exists(runpath)):
        for root, dirs, files in os.walk(runpath):
            break
    return files

noise_testno = 1
g_testno = 1
tp = "10us"
sg = "14mVfC"


mode16bit = False
f_dir = "D:/ColdADC/D2_noise_acq/"
fr_dir = f_dir + "results/"
if (os.path.exists(fr_dir)):
    pass
else:
    try:
        os.makedirs(fr_dir)
    except OSError:
        print ("Error to create folder ")
        exit()

noise_testno_str = "Test%02d"%noise_testno
fs = file_list(runpath=f_dir)
for f in fs:
    if (f.find(noise_testno_str)>0) and (f.find(tp)>0) and (f.find(sg)>0) and (f.find(".bin")>0):
        fn = f_dir + f
        break

with open (fn, 'rb') as fp:
    chns = pickle.load(fp)

rmss = []
for chnno in range(16):
    if (mode16bit):
        rmss.append(np.std(np.array(chns[chnno][0:10000])&0xffff))
    else:
        rmss.append( np.std( (np.array( chns[chnno][0:10000] )&0xffff)//16))

f_dir = "D:/ColdADC/D2_gainmeas_acq/"
fr_dir = f_dir + "results/"
g_testno_str = "Test%02d"%g_testno
fs = file_list(runpath=fr_dir)
for f in fs:
    if (f.find(g_testno_str)>=0) and (f.find(tp)>0) and (f.find(sg)>0) and (f.find(".csv")>0):
        gfn = fr_dir + f
        break

ccs = []
with open(gfn, 'r') as fp:
    for cl in fp:
        tmp = cl.split(",")
        x = []
        for i in tmp:
            x.append(i.replace(" ", ""))
        x = x[:-1]
        ccs.append(x)
        
gains = []        
for i in range(len(ccs[0])):
    gains.append(int(ccs[0][i]) )


encs = np.array(rmss)*np.array(gains)
print (encs)

enc_mean =int (np.std(encs))
chns = range(16)

fig = plt.figure(figsize=(8,6))
ax1 = plt.subplot2grid((4, 4), (0, 0), colspan=2, rowspan=2)
ax2 = plt.subplot2grid((4, 4), (2, 0), colspan=2, rowspan=2)
ax3 = plt.subplot2grid((4, 4), (0, 2), colspan=2, rowspan=4)
#    ax4 = plt.subplot2grid((4, 4), (2, 2), colspan=2, rowspan=2)
ax1.plot(chns, rmss, marker = '.')
ax2.plot(chns, gains, marker = '.')
ax3.plot(chns, encs, marker = '.', label = "Mean = %d"%enc_mean)

ax3.legend()

ax1.set_title("RMS Noise ")
ax2.set_title("Gain (e-/LSB)")
ax3.set_title("ENC (e-)")

ax1.set_xlabel("Channel No")
ax2.set_xlabel("Channel No")
ax3.set_xlabel("Channel No")

ax1.set_ylabel("RMS (LSB) ")
ax2.set_ylabel("Gain (e-/LSB)")
ax3.set_ylabel("ENC (e-)")

ax1.set_xlim((0,16))
ax2.set_xlim((0,16))
ax3.set_xlim((0,16))

ax1.set_ylim((0,10))
ax2.set_ylim((0,1000))
ax3.set_ylim((0,1000))

ax1.grid(True)
ax2.grid(True)
ax3.grid(True)

plt.tight_layout()
#plt.savefig( fpic + "_ch%d.png"%chnno)
#plt.close()

