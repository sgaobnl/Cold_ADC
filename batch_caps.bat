::Cd = 150pF
::python ADC_CFG_INIT.py RT BJT NoSDC
::python noise_acq.py        05us 14mVfC PLS_DIS 900mV BUF_OFF DC disable  01 RT 
::python noise_acq.py        10us 14mVfC PLS_DIS 900mV BUF_OFF DC disable  02 RT 
::python noise_acq.py        20us 14mVfC PLS_DIS 900mV BUF_OFF DC disable  03 RT 
::python noise_acq.py        30us 14mVfC PLS_DIS 900mV BUF_OFF DC disable  04 RT 
::python gain_measure_acq.py 05us 14mVfC PLS_EN  900mV BUF_OFF DC Internal 01 RT 
::python gain_measure_acq.py 10us 14mVfC PLS_EN  900mV BUF_OFF DC Internal 02 RT 
::python gain_measure_acq.py 20us 14mVfC PLS_EN  900mV BUF_OFF DC Internal 03 RT 
::python gain_measure_acq.py 30us 14mVfC PLS_EN  900mV BUF_OFF DC Internal 04 RT 
::
::python noise_acq.py        05us 14mVfC PLS_DIS 200mV BUF_OFF DC disable  01 RT 
::python noise_acq.py        10us 14mVfC PLS_DIS 200mV BUF_OFF DC disable  02 RT 
::python noise_acq.py        20us 14mVfC PLS_DIS 200mV BUF_OFF DC disable  03 RT 
::python noise_acq.py        30us 14mVfC PLS_DIS 200mV BUF_OFF DC disable  04 RT 
::python gain_measure_acq.py 05us 14mVfC PLS_EN  200mV BUF_OFF DC Internal 01 RT 
::python gain_measure_acq.py 10us 14mVfC PLS_EN  200mV BUF_OFF DC Internal 02 RT 
::python gain_measure_acq.py 20us 14mVfC PLS_EN  200mV BUF_OFF DC Internal 03 RT 
::python gain_measure_acq.py 30us 14mVfC PLS_EN  200mV BUF_OFF DC Internal 04 RT 

python ADC_CFG_INIT.py RT BJT NoSDC
python noise_acq.py        05us 14mVfC PLS_DIS 900mV BUF_OFF DC disable  01 LN 
python noise_acq.py        10us 14mVfC PLS_DIS 900mV BUF_OFF DC disable  02 LN 
python noise_acq.py        20us 14mVfC PLS_DIS 900mV BUF_OFF DC disable  03 LN 
python noise_acq.py        30us 14mVfC PLS_DIS 900mV BUF_OFF DC disable  04 LN 
python gain_measure_acq.py 05us 14mVfC PLS_EN  900mV BUF_OFF DC Internal 01 LN 
python gain_measure_acq.py 10us 14mVfC PLS_EN  900mV BUF_OFF DC Internal 02 LN 
python gain_measure_acq.py 20us 14mVfC PLS_EN  900mV BUF_OFF DC Internal 03 LN 
python gain_measure_acq.py 30us 14mVfC PLS_EN  900mV BUF_OFF DC Internal 04 LN 

python noise_acq.py        05us 14mVfC PLS_DIS 200mV BUF_OFF DC disable  01 LN 
python noise_acq.py        10us 14mVfC PLS_DIS 200mV BUF_OFF DC disable  02 LN 
python noise_acq.py        20us 14mVfC PLS_DIS 200mV BUF_OFF DC disable  03 LN 
python noise_acq.py        30us 14mVfC PLS_DIS 200mV BUF_OFF DC disable  04 LN 
python gain_measure_acq.py 05us 14mVfC PLS_EN  200mV BUF_OFF DC Internal 01 LN 
python gain_measure_acq.py 10us 14mVfC PLS_EN  200mV BUF_OFF DC Internal 02 LN 
python gain_measure_acq.py 20us 14mVfC PLS_EN  200mV BUF_OFF DC Internal 03 LN 
python gain_measure_acq.py 30us 14mVfC PLS_EN  200mV BUF_OFF DC Internal 04 LN 


