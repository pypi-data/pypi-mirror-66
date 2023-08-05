import pandas as pd
import numpy as np
#from scipy import interpolate
#from scipy.interpolate import interp1d
import seaborn as sns
#from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
#from matplotlib.pyplot import figure
#from statsmodels.graphics.tsaplots import plot_acf
#from matplotlib.lines import Line2D
import xarray as xr
#import matplotlib.collections as collections
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.cm as mpl_cm
import iris
import iris.quickplot as qplt
import os
    
def plt_make_ticks(lat):
    
    latrange=np.abs(np.max(lat)-np.min(lat))
    
    res=int((latrange*0.4))
    
    xticks=np.arange(-180,360,res)
    yticks=np.arange(-90,90,res)
    
    return xticks,yticks
    
def get_divider(num):
    dividers=[]
    if num > 1:
       # check for factors
        for i in range(2,num):
            if (num % i) == 0:
                dividers.append(i)
    else:
        dividers.append(1)

    return np.array(dividers)

def color_range(data,range_in,option='std'):
    """
    calc colorrange
    """
    if range_in[1]==0:
        if option == 'std':
            std=np.nanquantile(data, .25)        
            med=np.nanmedian(data)
            std=med-std
            minv=med-3*std
            maxv=med+3*std

        elif option =='minmax':
            minv=np.nanmin(data)
            maxv=np.nanmax(data)
    else:
        minv=range_in[0]
        maxv=range_in[1]   
    return minv,maxv
    
    

def fit_2D_dimension(num):
    
    dividers=get_divider(num)
    if len(dividers)>0:
        x=dividers[np.argmin(np.abs((dividers-np.sqrt(num))))]
        y=int(num/x)
    else:
        num=num+1
        x,y,num = fit_2D_dimension(num)
    return x,y,num

def gl_props(gl,scaler):
    gl.xlabel_style = {'size': 80*scaler}
    gl.ylabel_style = {'size': 80*scaler}
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    gl.ylabels_left = True
    gl.ylabels_right = False    
    return gl

def plt_xr_map_ax(ax,fig,data,lat,lon,land_50m,title,year,range_in,unit,
                  function='scatter',msize=0.3,color_map=''):
    """
    ax-object for xr_map plot
    """
    xticks,yticks=plt_make_ticks(lat)
    
    ax.add_feature(land_50m)
    ax.coastlines('10m')
    ax.set_aspect(aspect=1.6)
    minv,maxv = color_range(data,range_in,option='std')
    if function=='scatter':
        im = ax.scatter(lon,lat,c=data,s=msize,vmin=minv,vmax=maxv,cmap=color_map,transform=ccrs.Geodetic())
    elif function =='contour':
        ax.contourf(lon,lat,data,transform=ccrs.PlateCarree())        

    gl=ax.gridlines(draw_labels=True,xlocs=xticks, ylocs=yticks, alpha=0.25)
    gl=gl_props(gl,0.15)
    #ax.set_title(title)
    clb = fig.colorbar(im, ax=ax, orientation='vertical',shrink=0.7)
    clb.ax.set_title(unit)    
    plt.text(0.5, 1.12, title,
         horizontalalignment='center',
         fontsize=15,
         transform = ax.transAxes)
    plt.text(0.8, 0.15, year,
         horizontalalignment='center',
         fontsize=15,
         transform = ax.transAxes)    
    #cbar=fig.colorbar(im,cax=ax, orientation='vertical',shrink=0.5)   
    #cbar.ax.set_xlabel('RMS [mm/year]')    

    
    return ax

def make_map_data(ds,vari,date_ini,function):
    print(date_ini)
    
    if vari=='no_var':
        ds_f=ds
    else:
        ds_f=ds[vari] 
    if 'time' in ds.dims:
  
    
        if function=='scatter':
            lat=ds_f.loc[date_ini].lat.values.flatten()
            lon=ds_f.loc[date_ini].lon.values.flatten()
            data=ds_f.loc[date_ini].values.flatten()            
            #lat=ds_f.where(ds_f.time==date_ini,drop=True).lat.values.flatten()
            #lon=ds_f.where(ds_f.time==date_ini,drop=True).lon.values.flatten()
            #data=ds_f.where(ds_f.time==date_ini,drop=True).values.flatten()
        elif function =='contour':
            lat=ds_f.where(ds_f.time==date_ini,drop=True).lat.values
            lon=ds_f.where(ds_f.time==date_ini,drop=True).lon.values
            data=ds_f.where(ds_f.time==date_ini,drop=True).values  
    else:
        if function=='scatter':
            print(vari)
            lat=ds_f.lat.values.flatten()
            lon=ds_f.lon.values.flatten()
            data=ds_f.values.flatten()        
   
    return lat,lon,data,ds_f

def adjust_array_len(arrayin,plot_number):
    
    len_ar=len(arrayin)
    if len_ar < plot_number and len_ar > 1:
        arrayin = arrayin*int((plot_number/len_ar+1))
    elif len_ar < plot_number and len_ar == 1:
        arrayin = arrayin*plot_number
    return arrayin
    
    

def arrays_options(ds,var,time_in,ranges,units):
    
    if time_in[0]==0 and 'time' in ds.dims:
        time_in=[ds.time[0].values]
    
    plot_number=len(var)*len(time_in)
    ranges = adjust_array_len(ranges,plot_number)
    units = adjust_array_len(units,plot_number)  
    
    if len(var) == plot_number:  
        time_in = adjust_array_len(time_in,plot_number)          
    elif len(time_in) == plot_number:
        var = adjust_array_len(var,plot_number)           
    else:
        var = adjust_array_len(var,plot_number)   
        time_in = adjust_array_len(time_in,plot_number)    
        
        
        
#    if time_in[0]==0:
#        time_in=[ds.time[0].values]#

#    if len(time_in)>1:
#        date_in=time_in
#        var=var * len(time_in)
#        plot_number=len(time_in)
#    elif len(var)>1:
#        date_in=time_in * len(var)
#        plot_number=len(var)
#        if time_in[0]==0:
#            date_in=[]
#            for i in range(plot_number):
#                date_in.append(ds.var[i-1].time[0].values)            
#    else:
#        print('auto-print')
#        date_in=time_in * 1
#        var=var * 1
#        plot_number=1    
#    if (plot_number > 1) and (len(ranges)<2):
#        ranges=[[0,0]]*plot_number
#    if plot_number is not len(units):
#        units=units*plot_number  
    return plot_number,var,time_in,ranges,units

def plt_xr_map(ds,var=['ssh'],time=[0],ranges=[[0,0]],units=[''],
               domain='auto',save='False',save_dir='',save_name='',msize=0.3):
    """
    plot map of xr at timestep
    
    var: list of variables in data
    time: list of time-steps to plot
    ranges: list of [vmin,vmax] values of plotted data-range
    units: list of units
    domain: lon, lat domain [lonmin,lonmax,latmin,latmax]
    save: bool (save figure)
    save_dir: save-directory
    
    
    """

    cmap=mpl_cm.get_cmap('brewer_RdBu_11')
    proj=ccrs.PlateCarree()
    land_50m = cfeature.NaturalEarthFeature('physical', 'land', '10m',
                                    edgecolor='face',
                                    facecolor='#f7f7f7')#cfeature.COLORS['land'])

    # to be automised (loop over axis)
    print(var)
    plot_number,var,date_in,ranges,units=arrays_options(ds,var,time,ranges,units)

    function='scatter'
    xp,yp,nump=fit_2D_dimension(plot_number)
    size=7
    fig =plt.figure(figsize=(xp*size*1.1, yp*size))
    
    
    for i in range(1,plot_number+1):
        date_ini=pd.Timestamp(date_in[i-1])
        vari=var[i-1]
        lat,lon,data,ds_f=make_map_data(ds,vari,date_ini,function)
        print('date: ',date_ini)
        if 'long_name' in ds_f.attrs:
            title=ds_f.long_name        
        else:
            title=vari   
        if 'units' in ds_f.attrs:
            units[i-1]=ds_f.units        
        year=str(date_ini.month)+'-'+str(date_ini.year)
        #unit=
        ax=plt.subplot(xp,yp,i,projection=proj)    
        ax=plt_xr_map_ax(ax,fig,data,lat,lon,land_50m,title,year,ranges[i-1],units[i-1],function=function,color_map=cmap,msize=msize)
    #plt.tight_layout()

    plt.subplots_adjust(wspace=0.07, hspace=0.03)
    
    if save_dir=='':
        save_dir = os.path.dirname(os.path.realpath('__file__'))
        save_name=var[0]
    
    if save:
        plt.savefig(save_dir+'/'+save_name)
        

    
    
    
    
    