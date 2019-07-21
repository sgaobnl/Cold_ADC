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

#    def ref_mon(self, flg_bjt_r = True, mon_src = "VREFP", mux_src = "AUX_VOLTAGE", vmon = "VBGR", imon = "ICMOS_REF_5k", avg_points =5  ):
#        if (flg_bjt_r):
#            self.bc.cots_adc_bjt_mon_src(src = mon_src)
#            self.bc.cots_adc_mux_mon_src(src = mux_src )
#            self.bc.cots_adc_data(avr = 3)
#            time.sleep(0.1)
#            val = self.bc.cots_adc_data(avr = avg_points)
#            return val
            
    def bjt_ref_aux(self, mon_src = "VREFP", mux_src = "AUX_VOLTAGE", avg_points =5  ):
        self.bc.cots_adc_bjt_mon_src(src = mon_src)
        self.bc.cots_adc_mux_mon_src(src = mux_src )
        self.bc.cots_adc_data(avr = 2)
        val = self.bc.cots_adc_data(avr = avg_points)
        print ("MUX = %s, %s = %f"%(mux_src, mon_src, val))
        return val

    def all_bjt_ref_auxs(self ):
        vref  = cq.bjt_ref_aux(mon_src = "VREF_ext",  mux_src = "AUX_VOLTAGE")
        vrefn = cq.bjt_ref_aux(mon_src = "VREFN",     mux_src = "AUX_VOLTAGE")
        vrefp = cq.bjt_ref_aux(mon_src = "VREFP",     mux_src = "AUX_VOLTAGE")
        vcmi  = cq.bjt_ref_aux(mon_src = "VCMI",      mux_src = "AUX_VOLTAGE")
        vcmo  = cq.bjt_ref_aux(mon_src = "VCMO",      mux_src = "AUX_VOLTAGE")
        vbgr  = cq.bjt_ref_aux(mon_src = "VBGR_1.2V", mux_src = "AUX_VOLTAGE")
        vdac0_5k   = cq.bjt_ref_aux(mon_src = "Vdac0_5k",  mux_src = "AUX_ISOURCE")
        vdac1_5k   = cq.bjt_ref_aux(mon_src = "Vdac1_5k",  mux_src = "AUX_ISOURCE")
        ibuff0_5k  = cq.bjt_ref_aux(mon_src = "ibuff0_5k", mux_src = "AUX_ISOURCE")
        ibuff1_5k  = cq.bjt_ref_aux(mon_src = "ibuff1_5k", mux_src = "AUX_ISOURCE")
        isink_adc1_5k  = cq.bjt_ref_aux(mon_src = "Isink_adc1_5k", mux_src = "AUX_ISINK")
        isink_adc0_5k  = cq.bjt_ref_aux(mon_src = "Isink_adc0_5k", mux_src = "AUX_ISINK")
        isink_sha1_5k  = cq.bjt_ref_aux(mon_src = "Isink_sha1_5k", mux_src = "AUX_ISINK")
        isink_sha0_5k  = cq.bjt_ref_aux(mon_src = "Isink_sha0_5k", mux_src = "AUX_ISINK")
        isink_refbuf0_5k  = cq.bjt_ref_aux(mon_src = "Isink_refbuf0_5k", mux_src = "AUX_ISINK")
        isink_refbuf1_5k  = cq.bjt_ref_aux(mon_src = "Isink_refbuf1_5k", mux_src = "AUX_ISINK")
        return (vref, vrefn, vrefp, vcmi, vcmo, vbgr, vdac0_5k, vdac1_5k, ibuff0_5k, ibuff1_5k, 
                isink_adc1_5k, isink_adc0_5k, isink_sha1_5k, isink_sha0_5k, isink_refbuf0_5k, isink_refbuf1_5k )

    def ref_vmon(self, vmon = "VBGR", avg_points =5  ):
        self.bc.cots_adc_mux_mon_src(src = "VOLTAGE_MON")
        self.bc.cost_adc_v_mon_ena(1)
        self.bc.cost_adc_v_mon_select(vmon)
        self.bc.cots_adc_data(avr = 2)
        val = self.bc.cots_adc_data(avr = avg_points)
        self.bc.cost_adc_v_mon_ena(0)
        print ("MUX = VOLTAGE_MON, %s = %f"%( vmon, val))
        return val

    def all_ref_vmons(self ):
        vbgr  = cq.ref_vmon(vmon = "VBGR"  )
        vcmi  = cq.ref_vmon(vmon = "VCMI"  )
        vcmo  = cq.ref_vmon(vmon = "VCMO"  )
        vrefp = cq.ref_vmon(vmon = "VREFP" )
        vrefn = cq.ref_vmon(vmon = "VREFN" )
        vssa  = cq.ref_vmon(vmon = "VSSA"  )
        return (vbgr, vcmi, vcmo, vrefp, vrefn, vssa)

    def ref_imon(self, imon = "ICMOS_REF_5k", avg_points =5  ):
        self.bc.cots_adc_mux_mon_src(src = "CURRENT_MON")
        self.bc.cost_adc_i_mon_ena(1)
        self.bc.cost_adc_i_mon_select(imon)
        self.bc.cots_adc_data(avr = 2)
        val = self.bc.cots_adc_data(avr = avg_points)
        self.bc.cost_adc_i_mon_ena(0)
        print ("MUX = CURRENT_MON, %s = %f"%( imon, val))
        return val

    def all_ref_imons(self ):
        icmos_ref_5k = cq.ref_imon(imon = "ICMOS_REF_5k" )
        isha0_5k     = cq.ref_imon(imon = "ISHA0_5k" )
        iadc0_5k     = cq.ref_imon(imon = "IADC0_5k" )
        isha1_5k     = cq.ref_imon(imon = "ISHA1_5k" )
        iadc1_5k     = cq.ref_imon(imon = "IADC1_5k" )
        ibuff_cmos   = cq.ref_imon(imon = "IBUFF_CMOS" )
        iref_5k      = cq.ref_imon(imon = "IREF_5k" )
        irefbuffer0  = cq.ref_imon(imon = "IREFBUFFER0" )
        return (icmos_ref_5k, isha0_5k, iadc0_5k, isha1_5k, iadc1_5k, ibuff_cmos, iref_5k, irefbuffer0 )


    def Converter_Config(self, edge_sel = "Normal", out_format = "two-complement", 
                         adc_sync_mode ="Normal", adc_test_input = "Normal", 
                         adc_output_sel = "cal_ADCdata", adc_bias_uA = 50):
        self.bc.adc_edge_select(mode = edge_sel)
        self.bc.adc_outputformat(oformat = out_format)
        self.bc.adc_sync_mode(mode = adc_sync_mode)
        self.bc.adc_test_input(mode = adc_test_input)
        self.bc.adc_output_select(option = adc_output_sel)
        self.bc.adc_set_adc_bias(val = adc_bias_uA)
        
    def Input_buffer_cfg( self, sdc = "Bypass", db = "Bypass", sha = "Single-ended", curr_src = "BJT-sd"):        
        self.bc.adc_sdc_select(sdc)
        self.bc.adc_db_select(db)
        if (sha == "Single-ended"):
            self.bc.adc_sha_input(1)
        else:
            self.bc.adc_sha_input(0)
        self.bc.adc_ibuff_ctrl(curr_src)

    def get_adcdata(self, PktNum=128 ):
        rawdata = self.bc.get_data(PktNum,1) #packet check
        frames_inst = Frames(PktNum,rawdata)     
        frames = frames_inst.packets()
        #Change it to emit all 16 channels data 
        chns=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]] #16-bit
        for i in range(PktNum):
            for j in range(16): #16 channels
                chns[j].append(frames[i].ADCdata[j]) 
        return chns 
    
    def Word_order_cfg(self, PktNum=128 ):        
        self.bc.Acq_start_stop(1)
        for num in range(8):
            self.bc.word_order_slider(num)
            chns = self.get_adcdata(PktNum=128)
            if((chns[0][0] > 0xF000) and 
               (chns[1][0] > 0x4000) and  (chns[1][0] < 0xB000) and
               (chns[2][0] > 0x4000) and  (chns[1][0] < 0xB000)             
               (chns[1][0] > 0x4000) and  (chns[1][0] < 0xB000) 
               (chns[1][0] > 0x4000) and  (chns[1][0] < 0xB000)                
               (chns[1][0] > 0x4000) and  (chns[1][0] < 0xB000)                
               (chns[1][0] > 0x4000) and  (chns[1][0] < 0xB000)                
               (chns[1][0] > 0x4000) and  (chns[1][0] < 0xB000)                
               (chns[1][0] > 0x4000) and  (chns[1][0] < 0xB000)                
               
            print ("EEEEEEEEEEEEEEEEEEE")
            #self.bc.getdata()
#            break




env = "RT"
flg_bjt_r = True #default BJT reference

cq = CMD_ACQ()
cq.init_chk()
cq.ref_set(flg_bjt_r = flg_bjt_r )
cq.Input_buffer_cfg(sdc = "Bypass", db = "Bypass", sha = "Single-ended", curr_src = "BJT-sd")        
cq.Converter_Config(edge_sel = "Normal", out_format = "offset binary", 
                         adc_sync_mode ="Analog pattern", adc_test_input = "Normal", 
                         adc_output_sel = "cal_ADCdata", adc_bias_uA = 50)
cq.Word_order_cfg( )        


#tmp = cq.all_bjt_ref_auxs()
#print (tmp)
#tmp = cq.all_ref_vmons()
#print (tmp)
#tmp = cq.all_ref_imons()
#print (tmp)
#cq.ref_set(flg_bjt_r = False )
#tmp = cq.all_ref_vmons()
#print (tmp)
#tmp = cq.all_ref_imons()
#print (tmp)



