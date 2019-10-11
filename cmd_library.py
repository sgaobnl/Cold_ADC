#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 16:54:11 2019

@author: shanshangao
"""
#import numpy as np
from brd_config import Brd_Config
import time
import numpy as np
from raw_data_decoder import raw_conv

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

    def ss_chk(self ):

        tmp1 = self.bc.adc.I2C_read(4, 2, 1)
        tmp2 = self.bc.adc.I2C_read(4, 2, 2)
        tmp3 = self.bc.adc.I2C_read(4, 2, 3)
        print (hex(tmp1), hex(tmp2), hex(tmp3))

        
    def init_chk(self ):
        self.bc.Acq_start_stop(0)
        print ("ADC hard reset after power on")
        self.bc.adc.hard_reset()
        init_str = self.bc.adc_read_reg(0)
        if (init_str == '0x52'):
            print ("ADC hard reset is done, I2C link looks good!")
        tmp1 = self.bc.adc.I2C_read(4, 2, 1)
        tmp2 = self.bc.adc.I2C_read(4, 2, 2)
        tmp3 = self.bc.adc.I2C_read(4, 2, 3)
        print (hex(tmp1), hex(tmp2), hex(tmp3))
        self.bc.adc_soft_reset()
#        self.bc.adc.I2C_write(4, 2, 2, 1)
        tmp1 = self.bc.adc.I2C_read(4, 2, 1)
        tmp2 = self.bc.adc.I2C_read(4, 2, 2)
        tmp3 = self.bc.adc.I2C_read(4, 2, 3)
        print (hex(tmp1), hex(tmp2), hex(tmp3))

    
    def ref_set(self, flg_bjt_r = True, env = "RT" ):
        if (flg_bjt_r):
            self.bc.adc_ref_vol_src("BJT")
            print ("Internal BJT voltage references are used")
            self.bc.adc_bias_curr_src("BJT")
            print ("Bias currents come from BJT-based references")
            if (env == "RT"):
                vrefp_voft = 0xf0#0xe4#0xf0#0xe4
                vrefn_voft = 0x08#0x24#0x08#0x24
                vcmi_voft = 0x5c#0x60#0x50#0x60
                vcmo_voft = 0x82#0x82
                vrefp_ioft = 1
                vrefn_ioft = 1
                vcmi_ioft = 1
                vcmo_ioft = 1
            else:
                vrefp_voft = 0xf1#0xd4#0xf1
                vrefn_voft = 0x29#0x28#0x29
                vcmi_voft = 0x65#0x58#0x65
                vcmo_voft = 0x8d
                vrefp_ioft = 1
                vrefn_ioft = 1
                vcmi_ioft = 1
                vcmo_ioft = 1
            self.bc.adc_set_vrefs(vrefp_voft, vrefn_voft, vcmo_voft, vcmi_voft )
            self.bc.adc_set_ioffset(vrefp_ioft, vrefn_ioft, vcmo_ioft, vcmi_ioft)
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
                vrefp_voft = 0xce#0xe1
                vrefn_voft = 0x2b#0x0f
                vcmi_voft = 0x5b#0x5c
                vcmo_voft = 0x7b
            else:
                vrefp_voft = 0xc8#0xd0
                vrefn_voft = 0x2e#0x10
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

    def bjt_ref_aux(self, mon_src = "VREFP", mux_src = "AUX_VOLTAGE", avg_points =5  ):
        self.bc.cots_adc_bjt_mon_src(src = mon_src)
        self.bc.cots_adc_mux_mon_src(src = mux_src )
        self.bc.cots_adc_data(avr = 2)
        val = self.bc.cots_adc_data(avr = avg_points)
        print ("MUX = %s, %s = %f"%(mux_src, mon_src, val))
        return val

    def all_bjt_ref_auxs(self ):
        vref  = self.bjt_ref_aux(mon_src = "VREF_ext",  mux_src = "AUX_VOLTAGE")
        vrefn = self.bjt_ref_aux(mon_src = "VREFN",     mux_src = "AUX_VOLTAGE")
        vrefp = self.bjt_ref_aux(mon_src = "VREFP",     mux_src = "AUX_VOLTAGE")
        vcmi  = self.bjt_ref_aux(mon_src = "VCMI",      mux_src = "AUX_VOLTAGE")
        vcmo  = self.bjt_ref_aux(mon_src = "VCMO",      mux_src = "AUX_VOLTAGE")
        vbgr  = self.bjt_ref_aux(mon_src = "VBGR_1.2V", mux_src = "AUX_VOLTAGE")
        vdac0_5k   = self.bjt_ref_aux(mon_src = "Vdac0_5k",  mux_src = "AUX_ISOURCE")
        vdac1_5k   = self.bjt_ref_aux(mon_src = "Vdac1_5k",  mux_src = "AUX_ISOURCE")
        ibuff0_5k  = self.bjt_ref_aux(mon_src = "ibuff0_5k", mux_src = "AUX_ISOURCE")
        ibuff1_5k  = self.bjt_ref_aux(mon_src = "ibuff1_5k", mux_src = "AUX_ISOURCE")
        isink_adc1_5k  = self.bjt_ref_aux(mon_src = "Isink_adc1_5k", mux_src = "AUX_ISINK")
        isink_adc0_5k  = self.bjt_ref_aux(mon_src = "Isink_adc0_5k", mux_src = "AUX_ISINK")
        isink_sha1_5k  = self.bjt_ref_aux(mon_src = "Isink_sha1_5k", mux_src = "AUX_ISINK")
        isink_sha0_5k  = self.bjt_ref_aux(mon_src = "Isink_sha0_5k", mux_src = "AUX_ISINK")
        isink_refbuf0_5k  = self.bjt_ref_aux(mon_src = "Isink_refbuf0_5k", mux_src = "AUX_ISINK")
        isink_refbuf1_5k  = self.bjt_ref_aux(mon_src = "Isink_refbuf1_5k", mux_src = "AUX_ISINK")
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
        vbgr  = self.ref_vmon(vmon = "VBGR"  )
        vcmi  = self.ref_vmon(vmon = "VCMI"  )
        vcmo  = self.ref_vmon(vmon = "VCMO"  )
        vrefp = self.ref_vmon(vmon = "VREFP" )
        vrefn = self.ref_vmon(vmon = "VREFN" )
        vssa  = self.ref_vmon(vmon = "VSSA"  )
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
        icmos_ref_5k = self.ref_imon(imon = "ICMOS_REF_5k" )
        isha0_5k     = self.ref_imon(imon = "ISHA0_5k" )
        iadc0_5k     = self.ref_imon(imon = "IADC0_5k" )
        isha1_5k     = self.ref_imon(imon = "ISHA1_5k" )
        iadc1_5k     = self.ref_imon(imon = "IADC1_5k" )
        ibuff_cmos   = self.ref_imon(imon = "IBUFF_CMOS" )
        iref_5k      = self.ref_imon(imon = "IREF_5k" )
        irefbuffer0  = self.ref_imon(imon = "IREFBUFFER0" )
        return (icmos_ref_5k, isha0_5k, iadc0_5k, isha1_5k, iadc1_5k, ibuff_cmos, iref_5k, irefbuffer0 )


    def Converter_Config(self, edge_sel = "Normal", out_format = "two-complement", 
                         adc_sync_mode ="Normal", adc_test_input = "Normal", 
                         adc_output_sel = "cali_ADCdata", adc_bias_uA = 50):
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
        self.bc.Acq_start_stop(1)
        rawdata = self.bc.udp.get_pure_rawdata(PktNum+1000 )
        self.bc.Acq_start_stop(0)
        chns = raw_conv(rawdata, PktNum)[0]
#        self.bc.Acq_start_stop(1)
#        rawdata = self.bc.get_data(PktNum,1, Jumbo="Jumbo") #packet check
#        self.bc.Acq_start_stop(0)
#        frames_inst = Frames(PktNum,rawdata)     
#        frames = frames_inst.packets()
#        #Change it to emit all 16 channels data 
#        chns=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]] #16-bit
#        for i in range(PktNum):
#            for j in range(16): #16 channels
#                chns[j].append(frames[i].ADCdata[j]) 
        return chns 
    
    def get_adcdata_raw(self, PktNum=128 ):
        self.bc.Acq_start_stop(1)
        rawdata = self.bc.udp.get_pure_rawdata(PktNum+1000 )
        self.bc.Acq_start_stop(0)
        chns = raw_conv(rawdata, PktNum)[1]
#        rawdata = self.bc.get_data(PktNum,1, Jumbo="Jumbo") #packet check
#        return rawdata
        return chns

    def chn_order_sync(self, PktNum=128 ):  
        print ("Starting ADC physical channel and logical channel mapping...")
        self.bc.adc_load_pattern_0(0x01, 0x01)
        self.bc.adc_load_pattern_1(0x01, 0x01)
        woc_f = False
        for chn_order in range(32):
            self.bc.adc_framemarker_shift (num = chn_order)
            self.bc.adc_test_data_mode(mode = "Test Pattern")
            chns = self.get_adcdata(PktNum=128)
            nibble_sync_f = True
            for chndata in chns:
                if (chndata[1]&0xFFFF) != 0x0101:
                    nibble_sync_f = False
                    break
            if nibble_sync_f:
                self.bc.adc_test_data_mode(mode = "Normal")
                chns = self.get_adcdata(PktNum=128)
                for i in range(10):
                    chns = self.get_adcdata(PktNum=128)
                    if(( (chns[0][1] & 0xFFFF) > 0xE000) and 
                       ( (chns[1][1] & 0xFFFF) > 0x6000) and  ((chns[1][1] &0xFFFF)  < 0xE000) and
                       ( (chns[2][1] & 0xFFFF) < 0x6000) and 
                       ( (chns[3][1] & 0xFFFF) > 0x6000) and  ((chns[2][1] &0xFFFF)  < 0xE000) and            
                       ( (chns[4][1] & 0xFFFF) > 0x6000) and  ((chns[4][1] &0xFFFF)  < 0xE000) and               
                       ( (chns[5][1] & 0xFFFF) > 0x6000) and  ((chns[5][1] &0xFFFF)  < 0xE000) and               
                       ( (chns[6][1] & 0xFFFF) > 0x6000) and  ((chns[6][1] &0xFFFF)  < 0xE000) and               
                       ( (chns[7][1] & 0xFFFF) > 0x6000) and  ((chns[7][1] &0xFFFF)  < 0xE000) and               
                       ( (chns[8][1] & 0xFFFF) > 0xE000) and 
                       ( (chns[9][1] & 0xFFFF) > 0x6000) and  ((chns[9][1] &0xFFFF)  < 0xE000) and
                       ( (chns[10][1]& 0xFFFF) < 0x6000) and  
                       ( (chns[11][1]& 0xFFFF) > 0x6000) and  ((chns[10][1] &0xFFFF) < 0xE000) and            
                       ( (chns[12][1]& 0xFFFF) > 0x6000) and  ((chns[12][1] &0xFFFF) < 0xE000) and               
                       ( (chns[13][1]& 0xFFFF) > 0x6000) and  ((chns[13][1] &0xFFFF) < 0xE000) and               
                       ( (chns[14][1]& 0xFFFF) > 0x6000) and  ((chns[14][1] &0xFFFF) < 0xE000) and               
                       ( (chns[15][1]& 0xFFFF) > 0x6000) and  ((chns[15][1] &0xFFFF) < 0xE000) ):             
                        woc_f = True
                    else:
                        woc_f = False
                        break
                if woc_f == True:
                    print ("ADC chn order is %d"%chn_order)
                    print ("ADC physical channel and logical channel mapping is done")
                    break
            else:
                woc_f = False
                pass
        return woc_f
                
    def fe_cfg(self,sts=16*[0], snc=16*[0], sg=16*[3], st=16*[2], sbf = 16*[0], sdc = 0, sdacsw=0, fpga_dac=0,asic_dac=0, delay=10, period=200, width=0xa00 ):  
        self.bc.sts = sts
        self.bc.snc = snc
        self.bc.sg  = sg 
        self.bc.st  = st 
        self.bc.sbf = sbf #buffer on
        self.bc.sdc = sdc #FE AC
        self.bc.sdacsw = sdacsw
        self.bc.sdac = asic_dac
        self.bc.fe_spi_config()
        if sdacsw == 0:
            mode = "RMS"
        elif sdacsw == 1:
            mode = "External"
        elif sdacsw == 2: 
            mode = "Internal"
        self.bc.fe_pulse_config(mode)
        self.bc.fe_fpga_dac(fpga_dac)
        self.bc.fe_pulse_param(delay, period, width)


    def adc_cfg(self, adc_sdc="Bypass", adc_db="Bypass", adc_sha="Single-Ended", adc_curr_src="BJT-sd", env="RT", flg_bjt_r=True):
        #default BJT reference
        woc_f = False
        while(woc_f==False):
            self.init_chk()
            self.ref_set(flg_bjt_r = flg_bjt_r , env=env)
            time.sleep(1)
#            self.all_ref_vmons( )
            self.Input_buffer_cfg(sdc = adc_sdc, db = adc_db, sha = adc_sha, curr_src = adc_curr_src)      
            #self.Input_buffer_cfg(sdc = "On", db = "Bypass", sha = "Diff", curr_src = "BJT-sd")      
            self.bc.adc_sha_clk_sel(mode = "internal")
            self.Converter_Config(edge_sel = "Normal", out_format = "offset binary", 
                                 adc_sync_mode ="Analog pattern", adc_test_input = "Normal", 
                                 adc_output_sel = "cali_ADCdata", adc_bias_uA = 50)
            self.bc.udp.clr_server_buf()
            woc_f = self.chn_order_sync()
        
        self.Converter_Config(edge_sel = "Normal", out_format = "two-complement", 
                                 adc_sync_mode ="Normal", adc_test_input = "Normal", 
                                 adc_output_sel = "cali_ADCdata", adc_bias_uA = 50)
        
#        print ("Manual Calibration starting, wait...")
#        self.bc.udp.clr_server_buf()
#        self.bc.adc_autocali(avr=20000,saveflag="undef")
#        self.Converter_Config(edge_sel = "Normal", out_format = "offset binary", 
#                                 adc_sync_mode ="Normal", adc_test_input = "Normal", 
#                                 adc_output_sel = "cali_ADCdata", adc_bias_uA = 50)
        print ("Manual Calibration is done, back to normal")

#cq = CMD_ACQ() 
#cq.adc_cfg(adc_sdc="Bypass", adc_db="Bypass", adc_sha="Single-Ended", adc_curr_src="BJT-sd", env="RT", flg_bjt_r=True)
#cq.adc_cfg(adc_sdc="On", adc_db="Bypass", adc_sha="Diff", adc_curr_src="BJT-sd", env="RT", flg_bjt_r=True)
