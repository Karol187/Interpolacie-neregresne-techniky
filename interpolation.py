# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 08:22:00 2020

@author: kocok
"""

import numpy as np
from pykrige.ok import OrdinaryKriging





def getclosest_ij(nlats,nlons,latpt,lonpt):# funkcia ktora najde i,j, index mriezky v 2D poliach latudude a Lontitude
    # find squared distance of every point on grid
    dist_sq = (nlats-latpt)**2 + (nlons-lonpt)**2  
    # 1D index of minimum dist_sq element
    minindex_flattened = dist_sq.argmin()    
    # Get 2D index for latvals and lonvals arrays from 1D index
    return np.unravel_index(minindex_flattened, nlats.shape)

#IDW INTERPOLATION FUNKCTION
#############################
# Distance calculation, degree to km (Haversine method)
def harvesine(lon1, lat1, lon2, lat2):
    #start_time_of_harvesine = time.time()
    rad = np.pi / 180  # degree to radian
    R = 6378.1  
    dlon = (lon2 - lon1) * rad
    dlat = (lat2 - lat1) * rad
    a = (np.sin(dlat / 2)) ** 2 + np.cos(lat1 * rad) * \
        np.cos(lat2 * rad) * (np.sin(dlon / 2)) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    d = R * c
    #print('Harvesine {0:.3f}'.format(time.time() - start_time_of_harvesine))
    return(d)
# ------------------------------------------------------------
# IDW
def idwr(y, x, z, yi, xi):
    """
    inputs:
    x, y : lat_x, lat_y from dataframeupravene na mriezky  
    z : error concentrations of pollutant
    xi, yi : 1-D array of lon and lat 
    return 
    """
    d=np.array(list(map(lambda y,x: harvesine(y, x, yi, xi),y,x)))
    IDW = np.matmul(z,1/d**2)/np.sum(1/d**2,axis=0)

    return IDW;


def idw_interpolation(DF,f):
    """
    funkcia, ktora vyrata IDW interpolaciu nameranych koncentracii, 
    """
    x,y,z = list(DF['lat_x']),list(DF['lon_x']),list(DF['pollutant'])
    #GRID coordinates are xi and yi
    
    xi=f.variables['LAT'][0,0,:,:].flatten()
    yi=f.variables['LON'][0,0,:,:].flatten()
    
    IDW_POLLUTANT=np.asarray(idwr(y,x,z,yi,xi))
    IDW_POLLUTANT=np.reshape(IDW_POLLUTANT,(142,271))
    
    for i in range(0,len(x)):
        ix, iy = getclosest_ij(f.variables['LAT'][0,0,:,:],f.variables['LON'][0,0,:,:],x[i],y[i])
        IDW_POLLUTANT[ix,iy]=list(DF['pollutant'])[i]

    return IDW_POLLUTANT

def kriging_interpolation(DF,f):
    """
    funkcia, ktora vyrata Kriging interpolaciu nameranych koncentracii, 
    """
    x,y,z = list(DF['lon_x']),list(DF['lat_x']),list(DF['pollutant'])
    #xi,yi are new grid coordinates
    xi=np.linspace(np.min(f.variables['LON'][0,0,:,:].flatten()), np.max(f.variables['LON'][0,0,:,:].flatten()), 271)
    yi=np.linspace(np.min(f.variables['LAT'][0,0,:,:].flatten()), np.max(f.variables['LAT'][0,0,:,:].flatten()), 142)
    
    # OK is kriging funkction 
    OK = OrdinaryKriging(x, y, z, variogram_model='spherical')
    # z1 is kriging interpolation array 
    z1, ss1 = OK.execute('grid', xi, yi)
    KRIGING_POLLUTANT=z1
    
    return KRIGING_POLLUTANT

def idw_interpolation_model_residuals(DF,f,MODEL_POLLUTANT):  
    """
    funkcia, ktora odcita hodnoty z modelu CMAQ a interpoluje rezidua pomocou IDW interpolacie 
    """
    predpoved_modelu=[]
    # predpoved_modelu= hodnoty z modelu CMAQ
    for k, row in DF.iterrows():
        ix, iy = getclosest_ij(f.variables['LAT'][0,0,:,:],f.variables['LON'][0,0,:,:],row['lat_x'],row['lon_x'])
        hodnota=(MODEL_POLLUTANT[ix, iy])
        predpoved_modelu.append(hodnota)
    predpoved_modelu=np.array(predpoved_modelu)    
    residuals=DF['pollutant']-predpoved_modelu    
    #residuals = namerane hodnoty-hodnoty z CMAQ
    x,y,z = list(DF['lat_x']),list(DF['lon_x']),list(residuals)
    #GRID coordinates are xi and yi
    
    xi=f.variables['LAT'][0,0,:,:].flatten()
    yi=f.variables['LON'][0,0,:,:].flatten()
    
    IDW_RESIDUALS=np.asarray(idwr(y,x,z,yi,xi))
    IDW_RESIDUALS=np.reshape(IDW_RESIDUALS,(142,271))
    
    for i in range(0,len(x)):
        ix, iy = getclosest_ij(f.variables['LAT'][0,0,:,:],f.variables['LON'][0,0,:,:],x[i],y[i])
        IDW_RESIDUALS[ix,iy]=list(residuals)[i] 
    
    return predpoved_modelu, residuals, IDW_RESIDUALS, MODEL_POLLUTANT+IDW_RESIDUALS,z
    
    
def kriging_interpolation_model_residuals(DF,f,MODEL_POLLUTANT):   
    """
    funkcia, ktora odcita hodnoty z modelu CMAQ a interpoluje rezidua pomocou Kriging interpolacie 
    """
    predpoved_modelu=[]
     # predpoved_modelu= hodnoty z modelu CMAQ
    for k, row in DF.iterrows():
        ix, iy = getclosest_ij(f.variables['LAT'][0,0,:,:],f.variables['LON'][0,0,:,:],row['lat_x'],row['lon_x'])
        hodnota=(MODEL_POLLUTANT[ix, iy])
        predpoved_modelu.append(hodnota)
    predpoved_modelu=np.array(predpoved_modelu)    
    residuals=DF['pollutant']-predpoved_modelu    
     #residuals = namerane hodnoty-hodnoty z CMAQ
    x,y,z = list(DF['lon_x']),list(DF['lat_x']),list(residuals)
    #xi,yi are new grid coordinates
    xi=np.linspace(np.min(f.variables['LON'][0,0,:,:].flatten()), np.max(f.variables['LON'][0,0,:,:].flatten()), 271)
    yi=np.linspace(np.min(f.variables['LAT'][0,0,:,:].flatten()), np.max(f.variables['LAT'][0,0,:,:].flatten()), 142)
    
    # OK is kriging funkction 
    OK = OrdinaryKriging(x, y, z, variogram_model='spherical')
    # z1 is kriging interpolation array 
    z1, ss1 = OK.execute('grid', xi, yi)
   
    KRIGING_RESIDUALS=z1
   
    
    return predpoved_modelu, residuals, KRIGING_RESIDUALS, MODEL_POLLUTANT+KRIGING_RESIDUALS    
    
    
    
    