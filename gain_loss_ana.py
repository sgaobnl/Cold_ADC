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

f_dir = "D:/ColdADC/D2_gain_loss/"
testno = 1
fn_pre = "Test%dgainloss_tp10us_sg2_snc0dly"%(testno)
chn_sel = 4
fig = plt.figure(figsize=(12,6))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

for fn_pre in ["Test1gainloss_tp10us_sg2_snc0dly", 
               "Test2gainloss_tp10us_sg2_snc1dly",
               "Test3gainloss_tp10us_sg2_snc0dly",
               "Test4gainloss_tp10us_sg2_snc1dly",
               "Test5gainloss_tp10us_sg2_snc0dly",
               "Test6gainloss_tp10us_sg2_snc1dly",
               "Test7gainloss_tp10us_sg2_snc0dly",
               "Test8gainloss_tp10us_sg2_snc1dly",

               "Test9gainloss_tp10us_sg2_snc0dly",
               "Test10gainloss_tp10us_sg2_snc1dly",
               "Test11gainloss_tp10us_sg2_snc0dly",
               "Test12gainloss_tp10us_sg2_snc1dly",
               "Test13gainloss_tp10us_sg2_snc0dly",
               "Test14gainloss_tp10us_sg2_snc1dly",
               "Test15gainloss_tp10us_sg2_snc0dly",
               "Test16gainloss_tp10us_sg2_snc1dly",

               ]:
    dly_avg_chns = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    for dly in range(0, 50, 1):
        fn = f_dir + fn_pre + "%02d.bin"%dly
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
                

    dly_chn = [val for tup in zip(*dly_avg_chns[chn_sel]) for val in tup]  
    sps = (len(dly_chn))
    x = np.arange(sps)*0.01
    peak_pos = np.where(dly_chn[0:1000] == np.max(dly_chn[0:1000]))[0][0]
#    ax1.plot(x[0:2000], np.array(dly_chn[peak_pos-200:peak_pos+1800]) - dly_chn[0], label = fn_pre[0:5] )#, marker ='.')
    if "snc1" in fn_pre:
        ax2.plot(x[0:2000], np.array(dly_chn[peak_pos-200:peak_pos+1800]) - dly_chn[0], label = fn_pre[0:6])#, marker ='.')
    else:
        ax1.plot(x[0:2000], np.array(dly_chn[peak_pos-200:peak_pos+1800]) - dly_chn[0], label = fn_pre[0:6])#, marker ='.')
ax1.set_xlim([0, 10])
ax1.set_xlabel("Time / $\mu$s")
ax1.set_ylim([-5000, 20000])
ax1.set_ylabel("ADC counts / bin")
ax1.set_title ("Waveforms with 900mV BL (BL substracted)")
ax1.grid(True)
ax1.legend()
ax2.set_xlim([0, 10])
ax2.set_xlabel("Time / $\mu$s")
ax2.set_ylabel("ADC counts / bin")
ax2.set_ylim([-5000, 20000])
ax2.set_title ("Waveforms with 200mV BL (BL substracted)")
ax2.grid(True)
ax2.legend()

plt.tight_layout()
plt.savefig("d:/ColdADC/noise/gain_loss_comp.png")
plt.close()
#plt.show()



