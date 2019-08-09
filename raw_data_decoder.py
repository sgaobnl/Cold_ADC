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

#import matplotlib.pyplot as plt
#import matplotlib.gridspec as gridspec
#import matplotlib.patches as mpatches
#import matplotlib.mlab as mlab
#
import pickle
#


import numpy as np
import struct

def raw_conv(raw_data):
    smps = int(len(raw_data) //2)
    dataNtuple =struct.unpack_from(">%dH"%(smps),raw_data)
    pkg_len = int(0x1610/2)

    chn_data=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],]
    datalength = int( (len(dataNtuple) // pkg_len) -3) * (pkg_len) 
    pkg_index  = []

    i = int(0) 
    j = int(0)
    k = []
    while (i <= datalength ):
        data_a =  ((dataNtuple[i+0]<<16)&0x00FFFFFFFF) + (dataNtuple[i+1]& 0x00FFFFFFFF) + 0x0000000001
        data_b =  ((dataNtuple[i+0+pkg_len]<<16)&0x00FFFFFFFF) + (dataNtuple[i+1+pkg_len]& 0x00FFFFFFFF)
        acc_flg = ( data_a  == data_b )

        if ( acc_flg == True ) :
            pkg_index.append(i)
            i = i + pkg_len
        else:
            i = i + 1 
            k.append(i)

        if ( acc_flg == False ) :
            j = j + 1
    
    if ( len(k) != 0 ):
        print ("raw_convertor.py: There are defective packages start at %d"%k[0] )
    if j != 0 :
        print ("raw_convertor.py: drop %d packages"%(j) )

    tmpa = pkg_index[0]
    tmpb = pkg_index[-1]
    data_a = ((dataNtuple[tmpa+0]<<16)&0xFFFFFFFF) + (dataNtuple[tmpa+1]&0xFFFFFFFF) 
    data_b = ((dataNtuple[tmpb+0]<<16)&0xFFFFFFFF) + (dataNtuple[tmpb+1]&0xFFFFFFFF) 
    if ( data_b > data_a ):
        pkg_sum = data_b - data_a + 1
    else:
        pkg_sum = (0x100000000 + data_b) - data_a + 1
    missed_pkgs = 0
    for i in range(len(pkg_index)-1):
        tmpa = pkg_index[i]
        tmpb = pkg_index[i+1]
        data_a = ((dataNtuple[tmpa+0]<<16)&0xFFFFFFFF) + (dataNtuple[tmpa+1]&0xFFFFFFFF)
        data_b = ((dataNtuple[tmpb+0]<<16)&0xFFFFFFFF) + (dataNtuple[tmpb+1]&0xFFFFFFFF) 
        if ( data_b > data_a ):
            add1 = data_b - data_a 
        else:
            add1 = (0x100000000 + data_b) - data_a 
        missed_pkgs = missed_pkgs + add1 -1

    if (missed_pkgs > 0 ):
        print ("raw_convertor.py: missing udp pkgs = %d, total pkgs = %d "%(missed_pkgs, pkg_sum) )
        print ("raw_convertor.py: missing %.8f%% udp packages"%(100.0*missed_pkgs/pkg_sum) )
    else:
        pass

    smps_num = 0
    for onepkg_index in pkg_index:
        onepkgdata = dataNtuple[onepkg_index : onepkg_index + pkg_len]
        i = 8
        while i < len(onepkgdata) :
            if (onepkgdata[i] == 0xbc3c ) :
                for chn in range(16):
                    chn_data[chn].append( onepkgdata[i+6+chn] )
                smps_num = smps_num + 1
            else:
                print ("incomplete user package is found")
            i = i + 22 
    return chn_data

fn = "D:/ColdADC/C3_debug_asicdac5/Data_chn0_20us_dly0.bin"
with open (fn, 'rb') as f:
#    rawdata = pickle.load(fp)
    raw_data = f.read()

chn_data = raw_conv(raw_data)
print (len(chn_data))
print (len(chn_data[0]))
for i in range(16):
    print (hex(chn_data[i][0]))

#fig = plt.figure(figsize=(8,8))    
#for i in range(16):
#    ax = plt.subplot2grid((8,2), (i%8, i//8), colspan=1, rowspan=1)
#    sps = (len(chns[i]))
#    x = np.arange(sps)*0.5
#    ax.scatter(x[0:200], np.array(chns[i][0:200])&0x0000FFFF, marker ='.')
#    ax.plot(x[0:200], np.array(chns[i][0:200])&0x0000FFFF)
#
#
#plt.tight_layout()
#plt.show()
#plt.savefig("d:/ColdADC/pics/" "a.png")
#plt.close()



