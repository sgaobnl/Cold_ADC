#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 16:54:11 2019

@author: shanshangao
"""
#import numpy as np
from brd_config import Brd_Config
import time
#from udp import UDP 
#from adc_i2c_uart import COLDADC_tool
#
#from fpga_reg import FPGA_REG
#from fe_reg import FE_REG
#from user_defined import User_defined
#from adc_i2c_uart import COLDADC_tool
#from adc_reg import ADC_REG
#from frame import Frames
#import sys
#import time
#import math

class CMD_ACQ:
    def __init__(self):
        self.bc = Brd_Config()

    def init_chk(self ):
        print ("ADC hard reset after power on")
        self.bc.adc.hard_reset()
        init_str = self.bc.adc_read_reg(0)
        if (init_str == '0x52'):
            print ("ADC hard reset is done, I2C link looks good!")
    
    def ref_set(self, flg_bjt_r = True ):
        if (flg_bjt_r):
            self.bc.adc_ref_vol_src("BJT")
            print ("Internal BJT voltage references are used")
            self.bc.adc_bias_curr_src("BJT")
            print ("Bias currents come from BJT-based references")
            if (env == "RT"):
                vrefp_voft = 0xe4
                vrefn_voft = 0x24
                vcmi_voft = 0x60
                vcmo_voft = 0x82
                vrefp_ioft = 1
                vrefn_ioft = 1
                vcmi_ioft = 1
                vcmo_ioft = 1
            else:
                vrefp_voft = 0xf1
                vrefn_voft = 0x29
                vcmi_voft = 0x65
                vcmo_voft = 0x8d
                vrefp_ioft = 1
                vrefn_ioft = 1
                vcmi_ioft = 1
                vcmo_ioft = 1
            self.bc.adc_set_vrefs(vrefp_voft, vrefn_voft, vcmi_voft, vcmo_voft)
            self.bc.adc_set_ioffset(vrefp_ioft, vrefn_ioft, vcmi_ioft, vcmo_ioft)
            print ("BJT reference is set to pre-calibrated values!")
            ibuff0_15 = 0x99
            ibuff1_16 = 0x99
            ivdac0_17 = 0x99
            ivdac1_18 = 0x99
            self.bc.adc_set_curr_ibuff(ibuff0_15, ibuff1_16)
            self.bc.adc_set_curr_vdac(ivdac0_17, ivdac1_18)
            print ("BJT current source for input buffer and VDAC is set to default values!")
        else:
            self.bc.adc_ref_vol_src("CMOS")
            print ("CMOS voltage references are used")
            self.bc.adc_bias_curr_src("CMOS_INTR")
            print ("Bias currents come from CMOS-basedreference with internal R")  
            if (env == "RT"):
                vrefp_voft = 0xce
                vrefn_voft = 0x2b
                vcmi_voft = 0x5b
                vcmo_voft = 0x7b
            else:
                vrefp_voft = 0xc6
                vrefn_voft = 0x30
                vcmi_voft = 0x5b
                vcmo_voft = 0x7b
            self.bc.adc_set_cmos_vrefs(vrefp_voft, vrefn_voft, vcmi_voft, vcmo_voft)
            print ("CMOS reference is set to pre-calibrated values!") 
            iref_trim = 50
            self.bc.adc_set_cmos_iref_trim(iref_trim)
            print ("Set vt-reference current to 50uA by default!") 
            ibuff0_cmos = 0x27
            ibuff1_cmos = 0x27
            self.bc.adc_set_cmos_ibuff(ibuff0_cmos, ibuff1_cmos)
            print ("CMOS bias source for the input buffer is set!") 

    def ref_mon(self, flg_bjt_r = True, mon_src = "VREFP", aux_src = "AUX_VOLTAGE", vmon = "VBGR", imon = "ICMOS_REF_5k", avg_points =5  ):
        if (flg_bjt_r):
            self.bc.cots_adc_bjt_mon_src(src = mon_src)
            self.bc.cots_adc_mux_mon_src(src = aux_src )
            self.bc.cots_adc_data(avr = 3)
            time.sleep(0.1)
            val = self.bc.cots_adc_data(avr = avg_points)
            print (val)
            
            
env = "RT"
flg_bjt_r = True #default BJT reference

cq = CMD_ACQ()
cq.init_chk()
cq.ref_set(flg_bjt_r = flg_bjt_r )
cq.ref_mon()

