::Cd = 150pF
python ADC_CFG_INIT.py LN BJT NoSDC
python noise_acq.py        05us 14mVfC PLS_DIS 900mV BUF_OFF DC disable  01 LN  S1C130
python noise_acq.py        10us 14mVfC PLS_DIS 900mV BUF_OFF DC disable  02 LN  S1C130
python noise_acq.py        20us 14mVfC PLS_DIS 900mV BUF_OFF DC disable  03 LN  S1C130
python noise_acq.py        30us 14mVfC PLS_DIS 900mV BUF_OFF DC disable  04 LN  S1C130
python gain_measure_acq.py 05us 14mVfC PLS_EN  900mV BUF_OFF DC Internal 01 LN  S1C130
python gain_measure_acq.py 10us 14mVfC PLS_EN  900mV BUF_OFF DC Internal 02 LN  S1C130
python gain_measure_acq.py 20us 14mVfC PLS_EN  900mV BUF_OFF DC Internal 03 LN  S1C130
python gain_measure_acq.py 30us 14mVfC PLS_EN  900mV BUF_OFF DC Internal 04 LN  S1C130
python gain_fit_plot.py LN S1C130
python enc_plot.py LN S1C130
python enc_plot_tps.py LN S1C130

