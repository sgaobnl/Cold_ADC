# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 09:05:51 2019

@author: JunbinZhang
"""
from adc_i2c_uart import COLDADC_tool
from adc_reg import ADC_REG
class COLDADC_Config:
    #--------hard_reset with I2C tool---#
    def hard_reset(self):
        self.adc.hard_reset()
        self.adc.config_tool("I2C")
        
    def write_reg(self,reg,data):
        offset = 0x80
        regaddr = reg + offset
        self.adc.I2C_write(self.chip_id,self.page,regaddr,data)
        
    def read_reg(self,reg,data):
        offset = 0x80
        regaddr = offset + reg
        return self.adc.I2C_read(self.chip_id,self.page,regaddr)
    
    def soft_reset(self):
        self.adc.I2C_write(0,0,6,0)
    def LArasic_interface(self,sdc,db,ndiff,ref_val):
        #sdc=1 bypass, db=1 bypass, ndiff=1 single-ended, ref_val=0
        self.adc.ADC_I2C_write(self.chip_id,self.page,self.reg.ibuff_sdc_pd,sdc)
        self.adc.ADC_I2C_write(self.chip_id,self.page,self.reg.ibuff_diff_pd,db)
        self.adc.ADC_I2C_write(self.chip_id,self.page,self.reg.sha_se_input,ndiff)
        #control of current multiplexer. BJT or CMOS reference Direct current to SDC or DB
        self.adc.ADC_I2C_write(self.chip_id,self.page,self.reg.ibuff_ctrl,ref_val)
        
    def ref_vol_src(self,src):
        if src == "BJT":
            bit0 = 0
            bit1 = 0
            bit2 = 0
        elif src =="BJT_EXT":
            bit0 = 0
            bit1 = 1
            bit2 = 0
        elif src =="CMOS":
            bit0 = 0
            bit1 = 0
            bit2 = 1
        elif src =="EXTERNAL":
            bit0 = 1
            bit1 = 0
            bit2 = 1
        else:
            print("Error")
        self.adc.ADC_I2C_write(self.chip_id,self.page,self.reg.external_reference,bit0) #internal reference 0, external reference 1
        self.adc.ADC_I2C_write(self.chip_id,self.page,self.reg.external_bgr,bit1)       #internal bandgap reference used 0, otherwise 1
        self.adc.ADC_I2C_write(self.chip_id,self.page,self.reg.bgr_select,bit2)         #BJT reference for bandgap 0, CMOS for bandgap
    def bias_curr_src(self,src):
        if src == "BJT":
            sel = 0
        elif src == "CMOS_INTR":
            sel = 1
        elif src == "CMOS_EXTR":
            sel = 2
        elif src == "PlanB":
            sel = 3
        self.adc.ADC_I2C_write(self.chip_id,self.page,self.reg.iref_sel,sel)
        self.adc.ADC_I2C_write(self.chip_id,self.page,self.reg.vt_iref_trim_ctrl,3)
    
    def set_vrefs(self,ioffset,vrefp_c,vrefn_c,vcmo_c,vcmi_c):
        self.adc.ADC_I2C_write(self.chip_id,self.page,self.reg.vrefp_offset,ioffset)
        self.adc.ADC_I2C_write(self.chip_id,self.page,self.reg.vrefn_offset,ioffset)
        self.adc.ADC_I2C_write(self.chip_id,self.page,self.reg.vcmo_offset,ioffset)
        self.adc.ADC_I2C_write(self.chip_id,self.page,self.reg.vcmi_offset,ioffset)
        self.adc.ADC_I2C_write(self.chip_id,self.page,self.reg.vrefp_ctrl,vrefp_c)
        self.adc.ADC_I2C_write(self.chip_id,self.page,self.reg.vrefn_ctrl,vrefn_c)
        self.adc.ADC_I2C_write(self.chip_id,self.page,self.reg.vcmo_ctrl,vcmo_c)
        self.adc.ADC_I2C_write(self.chip_id,self.page,self.reg.vcmi_ctrl,vcmi_c)
    
    def set_curr_vdac(self,vdac0,vdac1):
        self.adc.ADC_I2C_write(self.chip_id,self.page,self.reg.i_vdac_0_ctrl,vdac0)
        self.adc.ADC_I2C_write(self.chip_id,self.page,self.reg.i_vdac_1_ctrl,vdac1)  
        
    def set_curr_ibuff(self,ibuff0,ibuff1):
        self.adc.ADC_I2C_write(self.chip_id,self.page,self.reg.ibuff0_ctrl,ibuff0)
        self.adc.ADC_I2C_write(self.chip_id,self.page,self.reg.ibuff1_ctrl,ibuff1)          
    
    def ref_monitor(self,byteL,byteH):
        self.adc.ADC_I2C_write(self.chip_id,self.page,self.reg.ref_monitor_L,byteL)
        self.adc.ADC_I2C_write(self.chip_id,self.page,self.reg.ref_monitor_H,byteH)

    def ref_powerdown(self,byteL,byteH):
        self.adc.ADC_I2C_write(self.chip_id,self.page,self.reg.ref_powerdown_L,byteL)
        self.adc.ADC_I2C_write(self.chip_id,self.page,self.reg.ref_powerdown_H,byteH)   
    
    def set_adc_bias(self,value):
        self.adc.ADC_I2C_write(self.chip_id,self.page,self.reg.adc_bias,value)
          
    def __init__(self):
        self.adc = COLDADC_tool()
        self.reg = ADC_REG()
        self.chip_id = 0
        self.page = 1
    
if __name__ == '__main__':
    adc = COLDADC_Config()
    adc.hard_reset()
    adc.ref_vol_src("BJT")
    adc.bias_curr_src("BJT")  
    #set voltage reference
    
    adc.ref_monitor(0,0)
    adc.ref_powerdown(0,0) 
    
    adc.set_vrefs(0,0x0,0x0,0x0,0x0)

    
    adc.adc.I2C_write(0,1,0x88,0xb)
    #adc.adc.I2C_write(0,1,0xAF,0xD0)
    #adc.adc.I2C_write(0,1,0x80,0x91)
    
    #reg 15, reg 16
    adc.set_curr_ibuff(0xff,0xff)
    #reg17, reg18
    adc.set_curr_vdac(0xff,0x00) 
    #reg20, reg21 #80 for reg15 #20 for reg17
    adc.ref_monitor(0x40,0x00)
    
    #reg22, reg233
    
    
#    adc.adc.I2C_write(0,1,0x80,0x91)
#    adc.adc.I2C_write(0,1,0x88,0x0f)
#    
#    adc.adc.I2C_write(0,1,0x8a,0x00)
#    adc.adc.I2C_write(0,1,0x8b,0x00)
#    adc.adc.I2C_write(0,1,0x8c,0x00)
#    adc.adc.I2C_write(0,1,0x8d,0x00)
#    

#    
#    adc.adc.I2C_write(0,1,0x93,0x00)
    
#    adc.adc.I2C_write(0,1,0x94,0x00)    
#    adc.adc.I2C_write(0,1,0x95,0x01)
#    
#    #adc.adc.I2C_write(0,1,0x96,0x00)
#    
#    adc.adc.I2C_write(0,1,0x8f,0xff)
#    
#    adc.adc.I2C_write(0,1,0x90,0x80)
#    adc.adc.I2C_write(0,1,0x91,0xff)
#    adc.adc.I2C_write(0,1,0x92,0xff)  
#    adc.adc.I2C_write(0,1,0x93,0x00)
#    adc.adc.I2C_write(0,1,0x88,0x0f)
    
    
#    adc.adc.I2C_write(0,1,0x97,0x00)
#    
#    adc.adc.I2C_write(0,1,0xaf,0xd0)
    
