# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 10:46:26 2019

@author: Dell
"""

'''

The moving average convergence divergence  is similar in
spirit to an absolute price oscillator in that it establishes the difference between a fast
exponential moving average and a slow exponential moving average. However, in the case
of MACD, we apply a smoothing exponential moving average to the MACD value itself in
order to get the final signal output from the MACD indicator. Optionally, you may also
look at the difference between MACD values and the EMA of the MACD values (signal)
and visualize it as a histogram.[ A properly configured MACD signal can successfully
capture the direction, magnitude, and duration of a trending instrument price]

'''

import pandas as pd
import matplotlib.pyplot as plt

#load data
fanmilk=pd.read_excel(r'C:\Users\Dell\Downloads\fan.xlsx') 
adjustedClose=fanmilk['Closing Price VWAP (GHS)'].tail(365)



#Create variables for fast EMA
nFast=10#umOfPeriodsForFast
'''

the shorter the time period,
the more reactive the EMA is to new price observations; in other words, the EMA
converges to new price observations faster and forgets older observations faster, also
referred to as Fast EMA.

'''
smoothingConstantFast=2/(nFast+1)
EMApriceFast=0

#Create variables for Slow EMA
nSlow=40
''' 
The longer the time period, the less reactive the EMA is to new
price observations; that is, EMA converges to new price observations slower and forgets
older observations slower, also referred to as Slow EMA.

'''
smoothingConstantSlow=2/(nSlow+1)
EMApriceSlow=0

#MACD smoothing constant
nMACD=20
smoothingConstantMACD=2/(nMACD+1)
emaMACD=0

#Create lists to hold newly calculated values
EMAfastValues=[]
EMAslowValues=[]
MACDvalues=[]
MACDsignal=[]
MACDhistogram=[]

#Calulate fast and close prices
for price in adjustedClose:
    if EMApriceFast==0:
        EMApriceFast=price
        EMApriceSlow=price
    
    else:
        EMApriceFast=(price - EMApriceFast) * smoothingConstantFast + EMApriceFast
        EMApriceSlow=(price - EMApriceSlow) * smoothingConstantSlow + EMApriceSlow
        
    EMAfastValues.append(EMApriceFast)
    EMAslowValues.append(EMApriceSlow)
    MACD=EMApriceFast-EMApriceSlow
    
    if emaMACD==0:
        emaMACD=MACD
    else:
        emaMACD=(MACD-emaMACD)*smoothingConstantMACD+emaMACD
    
    MACDvalues.append(MACD)
    MACDsignal.append(emaMACD)
    MACDhistogram.append(MACD-emaMACD)
    
#create dataframe of values    
df=pd.DataFrame(adjustedClose,index=fanmilk['Date'].tail(365))
df['EMAfast']=EMAfastValues
df['adjustedPrice']=adjustedClose
df['EMAslow']=EMAslowValues
df['MACDvalues']=MACDvalues
df['MACDsignal']=MACDsignal
df['MACDhistogram']=MACDhistogram

close=df['adjustedPrice']
EMAfast=df['EMAfast']
EMAslow=df['EMAslow']
MACDvalues=df['MACDvalues']
MACDsignal=df['MACDsignal']
MACDhistogram=df['MACDhistogram']

#plot figures
fig=plt.figure(figsize=(8,6))

axis=fig.add_subplot(311,ylabel='Stock Prices')
close.plot(ax=axis,color='g',lw=2,legend=True)
EMAfast.plot(ax=axis,color='b',lw=2,legend=True)  
EMAslow.plot(ax=axis,color='r',lw=2,legend=True)

axis2=fig.add_subplot(312,ylabel='MACD')
MACDvalues.plot(ax=axis2,color='r',lw=2,legend=True)
MACDsignal.plot(ax=axis2,color='g',lw=2,legend=True)

axis3=fig.add_subplot(313,ylabel='MACD')
MACDhistogram.plot(ax=axis3,color='r',kind='bar',legend=True,use_index=False)
axis3.set_xticks(axis3.get_xticks()[::10])

plt.show()
        
    
