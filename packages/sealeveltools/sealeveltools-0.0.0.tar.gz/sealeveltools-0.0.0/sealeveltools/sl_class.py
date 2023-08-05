#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May  9 16:15:59 2019

@author: oelsmann
"""


import numpy as np
import pandas as pd
from scipy.stats import norm
from scipy.optimize import curve_fit

    
class slt_object:
    """
    sea_level_tool Object
    
    - accepts xr, pd or float objects
    - extracts necessary information for statistical tools to be applied (sl)
    - class sl needs slt_object
    
    information on data-set
    helps to understand and pack the data to be used by sl()
        typ = check_type(self.data)
        data = data        
        shape =
        flat_x =
        flat_y =
        flat_numeric_y =
        operator =
    
    """

    
    def __init__(self,data):   
        

        
        def understand_data(self):
            """
            understand data-type (if pandas timeseries or xr)
            and dimension
            """    

        self.data = data    
        
    
    @property
    def typ(self):
        """
        xr, pandas, float
        """

        str_typ = str(type(self.data))
        if str_typ=="<class 'pandas.core.frame.DataFrame'>":
            typ='pd'
        if str_typ=="<class 'pandas.core.series.Series'>":
            typ='pd'                
        elif str_typ=="<class 'float'>":
            typ='float'
        elif str_typ=='xarray.core.dataset.Dataset':
            typ='xra'
        elif str_typ== "<class 'xarray.core.dataarray.DataArray'>":
            typ='xr'
        return typ     
    
    @property    
    def var(self):
        if self.typ == 'xra':
            return list(self.data.keys())[0]
        elif self.typ == 'xr' or self.typ == 'pd':
            return self.data.name
        else:
            return ''
    
    
    @property
    def shape(self):
        if self.typ == 'xra':
            return self.data[self.var].values.shape            
        elif self.typ == 'xr':
            return self.data.values.shape
        elif self.typ == 'pd':
            return self.data.shape
        else:
            return ()        
        
        #return get_shape(self)   
    @property
    def flat_x(self):
        if self.typ == 'xra':

            if len(self.shape) > 2:
                 flat_x= self.data[self.var].values.reshape(self.shape[0],self.shape[1]*self.shape[2])
            else:           
                 flat_x= self.data[self.var].values
        elif self.typ == 'xr':

            if len(self.shape) > 2:
                 flat_x= self.data.values.reshape(self.shape[0],self.shape[1]*self.shape[2])
            else:           
                 flat_x= self.data.values                

        elif self.typ == 'pd':
             flat_x=self.data.index
        else:
             flat_x= self.data
        return flat_x        
        #return self.__flat_x
    @property
    def flat_y(self):
        if self.typ == 'xr' or self.typ == 'xra':
            if 'time' in self.data.dims:
                timeser = self.data.time
            else: 
                timeser=np.array([0])

        elif self.typ == 'pd':
            timeser =self.data.index
        else:
            timeser = np.array([0])
        if len(timeser) > 1:                
            timeser=pd.to_datetime(timeser.values)    
        return timeser
        #return self.__flat_y
    @property
    def flat_y_numeric(self):
        year=pd.Timedelta('365.2422 days')
        f=year.total_seconds()   
        if len(self.flat_y)>1:
            return (self.flat_y-pd.to_datetime('1990-01-01')).total_seconds().values/f
        else:
            return (pd.to_datetime('2000-01-01')-pd.to_datetime('1990-01-01')).total_seconds()/f                

        #return self.__flat_y_numeric     

            

class sl(slt_object):
    """
    statistical tools
    inherits attributes from sl_obj
    
    data = data-obj -> slt_object.data
    data2= 2nd obj tto be added, subtracted or correlated with
    """  
    
  
    
    def plot(self,**kwargs):   
        
        if not 'var' in kwargs:
            kwargs['var']=[self.var]
            if self.typ=='xr':
                kwargs['var']=['no_var']                
        plt_xr_map(self.data,**kwargs)
        
        
    def norm_data(self,data2):
        """
        
        """
        if data2.typ=='float':
            return data2
        
        elif data2.typ=='pd':
            data2.data=self.data*0+data2*(self.data*0+1).values[0,:,:,np.newaxis]
        
        else:
            data2.data=self.data*0+data2.data
        
        return data2
        
        
        

    def add(self,data2):
        data2_norm=norm_data(self,sl(data2))
        #self.data=xr.apply_ufunc(sl_trend_prepare, self.data,self.data.time,
        #                  input_core_dims=[["time"],["time"]],output_core_dims=[['var']],
        #                         kwargs=kwargs,dask = 'allowed', vectorize = True)     
        
        self.data=self.data+data2_norm.data
        
    def cor(self,data2):
        
        print(cor)
    
    def sub(self,data2):
        print(cor)    

    
    def detrend(self,**kwargs):
        """
        subtract trend and annual cycle
        
        **kwargs ={'de_season' : 'False','semi' : 'False'}
        """
        #kwargs.setdefault('detrend', True)        
        kwargs['dtrend']=True
        out=trend_sub(self,**kwargs) # function in sl_stats
    
        

        if len(self.shape)>2:
            detrend_arr=annual_cycle(self.flat_y_numeric,out['offset'].values[0,:,:,np.newaxis],
                     out['trend'].values[0,:,:,np.newaxis],
                     out['acos'].values[0,:,:,np.newaxis],
                     out['asin'].values[0,:,:,np.newaxis])        
            self.data=self.data-np.swapaxes(np.swapaxes(detrend_arr,0,2),1,2)
            
        else:
            detrend_arr=annual_cycle(self.flat_y_numeric,out['offset'].values[0,:,np.newaxis],
                     out['trend'].values[0,:,np.newaxis],
                     out['acos'].values[0,:,np.newaxis],
                     out['asin'].values[0,:,np.newaxis])             
            self.data=self.data-np.swapaxes(detrend_arr,0,1)
                              
        self.data.attrs={'standard_name': self.var, 'long_name': 'detrended '+self.var,'_FillValue' : 'nan'}                   
        return self  
    

    
    def trend(self,de_season=False,cubic=False,semi=False,
                       de_season_without_trend=False,trend_only=False):
        
        kwargs={'de_season':de_season,'cubic':cubic,'semi':semi,
                       'de_season_without_trend':de_season_without_trend,'trend_only':trend_only}
        
        self.data=trend_sub(self,**kwargs)  
        return self
    
    
    def selmon(self,months):
        
        months=np.asarray(months)
        out=self.data
        if self.typ == 'xr' or self.typ == 'xra':

            self.data=out[np.isin(pd.to_datetime(out.time.values).month,months),:,:]

        elif self.typ == 'pd':
            self.data=out[np.isin(pd.to_datetime(out.time.values).month,months)].dropna()
        else:
            '! no pandas or xarray data-type !'        
        return self         
        

    
    def yearmean(self,):
        if self.typ == 'xr' or self.typ == 'xra':
            self.data=self.data.resample(time="Y").mean()
        elif self.typ == 'pd':
            self.data=self.data.resample('Y').mean()
        else:
            '! no pandas or xarray data-type !'
        return self
 
    def monmean(self,):
        if self.typ == 'xr' or self.typ == 'xra':
            self.data=self.data.resample(time="M").mean()
        elif self.typ == 'pd':
            self.data=self.data.resample('M').mean()
        else:
            '! no pandas or xarray data-type !'
        return self       
  
    def seasmean(self,seas='DJF'):
        ll=['DJF','MAM','JJA','SON']
        ll2=[12,3,6,9]
        ll3=[3,6,9,12]
        
        if self.typ == 'xr' or self.typ == 'xra':
            month=ll3[ll.index(seas)]
            out=self.data.resample(time="QS-DEC").mean()
            if self.typ == 'xra': 
                out=out[self.var].shift(time=1)
            else:
                out=out.shift(time=1)
                
            time_new=out[pd.to_datetime(out.time.values).month==month,:,:]
            self.data=time_new.resample(time="Y").mean()
            
            
            
            
        elif self.typ == 'pd':
            month=ll2[ll==seas]
            out=self.data.resample("QS-DEC").mean()
            self.data=out.where(out.index.month==month).dropna().shift(2, freq ='MS').resample('Y').mean()

        else:
            '! no pandas or xarray data-type !'        
        return self   
    def timavg(self):
        if self.typ == 'xr' or self.typ == 'xra':
            self.data=self.data.mean(dim=['time'])
        elif self.typ == 'pd':
            self.data=self.data.mean(axis=0)
        else:
            '! no pandas or xarray data-type !'
        return self
    
 

    
class sat:
    """
    object contains time series and information for altimetry measurement
    
    """
    
    def __init__(self,mission,data,loc,dist_coast,frequency,correction_version,box_length):
        self.mission = mission
        self.loc = loc 
        self.data = data
        self.dist_coast =dist_coast
        self.frequency =frequency
        self.correction_version =correction_version
        self.box_length =box_length
        
        
        
class tidegauge:
    """
    object contains time series and information for tide gauge measurement
    
    """
    def __init__(self,name,data,loc,info,months,flag,tgindex):
        self.name = name
   
        if (flag == 0) or (flag == 2) or (flag == 3): # flag = 1: valid
            self.data = data
        else:
            self.data = np.nan              
        self.loc = loc #lat lon
        self.info = info
        self.months = months
        self.tgindex = tgindex
    def correct_xtr(self):  #exclude 999%percentiles
        self.data=gauss_percentiles(self.data)

        
        
def gauss_percentiles(data):
    
    gauss_fit = norm.fit(data.sealevel[~np.isnan(data.sealevel)])
    quant_gauss_up=norm.ppf(0.9998,gauss_fit[0],gauss_fit[1])
    quant_gauss_down=norm.ppf(0.0002,gauss_fit[0],gauss_fit[1])
    correct=data.mask(data.sealevel>quant_gauss_up)
    correct=correct.mask(correct.sealevel<quant_gauss_down)    
    return correct        
