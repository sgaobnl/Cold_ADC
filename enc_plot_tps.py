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

nf_dir = "D:/ColdADC/D2_noise_acq/"
nfr_dir = nf_dir + "results/"

mode16bit = True
if (mode16bit):
    adc_bits = "ADC16bit"
else:
    adc_bits = "ADC12bit"
fn = nfr_dir + "Test_result" + adc_bits +".bin"

with open (fn, 'rb') as fp:
    test_ps = pickle.load(fp)
# 0  1    2       3          4       5      6   7          8              9                10
#                                          enc  std        rms           std               gain          
#[8, 8, '30us', '14mVfC', '200mV', 'SDC', 539, 40, 49.34276008740476, 3.7582430361394032, 10.934308572889488]

BL = "900mV"
sdc = "SDC"

enc_gs = []
estd_gs = []
adc_gs = []
astd_gs = []
gain_gs =[]

fig = plt.figure(figsize=(4,9))
ax1 = plt.subplot2grid((6, 2), (0, 0), colspan=2, rowspan=2)
ax2 = plt.subplot2grid((6, 2), (2, 0), colspan=2, rowspan=2)
ax3 = plt.subplot2grid((6, 2), (4, 0), colspan=2, rowspan=2)

print (len(test_ps))
for g in ["47mVfC","78mVfC", "14mVfC", "25mVfC" ]: 
    enc_tp  = []
    estd_tp = []
    adc_tp  =[]
    astd_tp =[]
    gain_tp =[]
    for tp in ["05us", "10us", "20us", "30us"]:
        for ti in test_ps:
            if (BL in ti) and (g in ti) and (tp in ti) and (sdc in ti):
                enc_tp.append(ti[6])
                estd_tp.append(ti[7])
                adc_tp.append(ti[8])
                astd_tp.append(ti[9])
                gain_tp.append(ti[10])
                break

    x = [0.5, 1.0, 2.0, 3.0]
    print (x, enc_tp, estd_tp)
    ax1.errorbar(x, enc_tp, estd_tp, label= g)
    ax2.errorbar(x, adc_tp, astd_tp, label= g)
    ax3.plot(x, gain_tp, label= g)

ax1.legend()
ax2.legend()
ax3.legend()

ax1.set_title("ENC Measurement ")
ax3.set_title("Noise with RMS(ADC)")
ax3.set_title("Gain (e-/LSB)")

ax1.set_xlabel("Peak time / ($\mu$s)")
ax2.set_xlabel("Peak time / ($\mu$s)")
ax3.set_xlabel("Peak time / ($\mu$s)")

ax1.set_ylabel("ENC / (e-) ")
ax2.set_ylabel("RMS(ADC) / LSB")
ax3.set_ylabel("Gain (e-/LSB)")

#xlim = (-2, 18) 
#ax1.set_xlim(xlim)
#ax2.set_xlim(xlim)
#ax3.set_xlim(xlim)
#
#if (mode16bit):
#    ax1_ylim = (0, 200)
#    ax2_ylim = (0, 50)
#    ax3_ylim = (0, 1500)
#else:
#    ax1_ylim = (0, 20)
#    ax2_ylim = (0, 1000)
#    ax3_ylim = (0, 1500)
#ax1.set_ylim(ax1_ylim)
#ax2.set_ylim(ax2_ylim)
#ax3.set_ylim(ax3_ylim)

ax1.grid(True)
ax2.grid(True)
ax3.grid(True)

plt.tight_layout()
#plt.savefig( nfr_dir + "NoiseTest%d"%test_ps[ty][0] +"_GainTest%d"%test_ps[ty][1] \
#            + test_ps[ty][2] +test_ps[ty][3] + test_ps[ty][4] +test_ps[ty][5] + adc_bits +  ".png" )
#plt.close()

#    y = enc_tp
#
#    title = "ENC Measurement"
#
#    enc_gs.append(  enc_tp  )
#    estd_gs.append( estd_tp ) 
#    adc_gs.append(  adc_tp  ) 
#    astd_gs.append( astd_tp )
#    gain_gs.append( gain_tp )
#
#    
#        x = tp_us
#        y = [xenc_tps[0][0], xenc_tps[1][0], xenc_tps[2][0], xenc_tps[3][0]]
#        maxy = np.max(y)
#        e = [xenc_tps[0][1], xenc_tps[1][1], xenc_tps[2][1], xenc_tps[3][1]]
#        label = "%d"%xchns +" X " +  "wires" 
#        ax.errorbar(x, y, e, label=label, color='g', marker='o')
#
