#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 16:54:11 2019

@author: shanshangao
"""
#import numpy as np
from cmd_library import CMD_ACQ
import os
import sys

env = sys.argv[1]
flg_bjt_r = (sys.argv[2] == "BJT")
adc_sdc_en = (sys.argv[3] == "SDC")

cq = CMD_ACQ() 
if (adc_sdc_en):
    cq.adc_cfg(adc_sdc="On", adc_db="Bypass", adc_sha="Diff", adc_curr_src="BJT-sd", env=env, flg_bjt_r=flg_bjt_r)
else:
    cq.adc_cfg(adc_sdc="Bypass", adc_db="Bypass", adc_sha="Single-ended", adc_curr_src="BJT-sd", env=env, flg_bjt_r=flg_bjt_r)

