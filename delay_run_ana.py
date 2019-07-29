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

dly_avg_chns = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
tmpr = "BB5_C01"
f_dir = "D:/ColdADC/" + tmpr + "_asicdac5/"
fn_pre = "Data_chn0_05us_"
for dly in range(0,50,1):
    fn = f_dir + fn_pre + "dly%d.bin"%dly
    with open (fn, 'rb') as fp:
        chns = pickle.load(fp)
    oft = 100
    poft = oft + np.where(np.array(chns[0][oft:])>0xffff)[0][0]
    avg_chns = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

    avg_n = 50
    for i in range(0,avg_n):
        for j in range(len(avg_chns)):
            if i == 0:
                avg_chns[j] = np.array(chns[j][poft+200*i:poft+200+200*i])
            else:
                avg_chns[j] = avg_chns[j] + np.array(chns[j][poft+200*i:poft+200+200*i])
    for j in range(len(avg_chns)):
        avg_chns[j] = avg_chns[j]//avg_n
        dly_avg_chns[j].append( list(avg_chns[j]&0xffff)    )

for i in range(len(dly_avg_chns)):
    tmp = reversed(dly_avg_chns[i])
    dly_avg_chns[i] = tmp
    

#fig = plt.figure(figsize=(12,8))
#for i in [3]:
 #   ax = plt.subplot2grid((8,2), (i%8, i//8), colspan=1, rowspan=1)
#    dly_chn = [val for tup in zip(*dly_avg_chns[i]) for val in tup]  
#    sps = (len(dly_chn))
#    x = np.arange(sps)*0.01
#    plt.scatter(x[100:600], dly_chn[100:600], marker ='.')
fig = plt.figure(figsize=(12,12))
for i in range(16):
    ax = plt.subplot2grid((8,2), (i%8, i//8), colspan=1, rowspan=1)
    dly_chn = [val for tup in zip(*dly_avg_chns[i]) for val in tup]  
    sps = (len(dly_chn))
    x = np.arange(sps)*0.01
    ax.scatter(x[0:500], dly_chn[0:500], marker ='.')
#    
plt.tight_layout()
plt.savefig("d:/ColdADC/pics/" + fn_pre + tmpr + ".png")
plt.close()
#dly_chn = [val for tup in zip(*dly_avg_chns[0]) for val in tup]  
#sps = (len(dly_chn))
#x = np.arange(sps)*0.01
#
#
#plt.scatter(x[100:1000], dly_chn[100:1000], marker ='.')


#lists = [l1, l2, ...]
#[val for tup in zip(*lists) for val in tup]      
#    sps = 100
#    x = np.arange(sps)*0.5 - dly*0.01
##    print (x)
##    plt.plot(x, avg_chns[0][0: sps])
##    plt.plot(x, avg_chns[1][1: sps+1])
#    plt.scatter(x, avg_chns[1][1: sps+1], marker ='.')

    
#    plt.scatter(x, avg_chns[0][0:sps], marker = '.')
##    plt.plot(x, chns[0][poft:poft+sps])
##    plt.scatter(x, chns[0][poft:poft+sps], marker = '.')
#
##plt.savefig("d:\abc.png")
#plt.show()

print ("xxxx")
#plt.close()

