# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 14:29:52 2020

@author: kocok
"""

import interpolation
import numpy as np

def validation_of_interpolations(DF,f, interpolation_type) :
    """
    funkcia, ktora validuje interpolaciu nameranych koncentracii, 
    interpolacia je bud IDW alebo kriging.
    """
    print('###########################')
    print('leaving one validation for: ' + interpolation_type)      
    
    predicted_value=[]# this is the list of arrays, each array has 1 station dropped.
    for i, row in DF.iterrows():
        DF1=DF.drop([i])
        ix, iy = interpolation.getclosest_ij(f.variables['LAT'][0,0,:,:],f.variables['LON'][0,0,:,:],row['lat_x'],row['lon_x'] )
        if interpolation_type == 'IDW':
           value = interpolation.idw_interpolation(DF1,f)[ix,iy]
        elif interpolation_type == 'kriging':
           value = interpolation.kriging_interpolation(DF1,f)[ix,iy]
        predicted_value.append(value)  
        print('EOI = {}, model = {}, measured = {} '.format(row['EOI'],value,row['pollutant']))
        #print('{}      {}      {}      {}'.format(row['name'], row['EOI'], value,  row['pollutant']))
    predicted_value=np.array(predicted_value)    
    RMSE=((np.sum((DF['pollutant']-predicted_value)**2))*(1/len((DF['pollutant']-predicted_value))))**0.5
    BIAS=np.sum((predicted_value-DF['pollutant']))/predicted_value.shape[0]
    r=np.corrcoef(predicted_value,DF['pollutant'] )[0,1]
    print('RMSE={}, BIAS={}, r={}'.format(RMSE,BIAS,r))
    
def validation_of_interpolations_model_residuals(DF,f,MODEL_POLLUTANT, interpolation_type): 
    """
    funkcia, ktora validuje CMAQ+interpolaciu rezidui, 
    interpolacia rezidui je bud IDW alebo kriging.
    """      
    print('###########################')
    print('leaving one validation for: ' + interpolation_type)      
    
    predicted_value=[]# this is the list of arrays, each array has 1 station dropped.
    for i, row in DF.iterrows():
        DF1=DF.drop([i])
        ix, iy = interpolation.getclosest_ij(f.variables['LAT'][0,0,:,:],f.variables['LON'][0,0,:,:],row['lat_x'],row['lon_x'] )
        if interpolation_type == 'CMAQ+IDW':
           value = interpolation.idw_interpolation_model_residuals(DF1,f,MODEL_POLLUTANT)[3][ix,iy]
        elif interpolation_type == 'CMAQ+kriging':
           value = interpolation.kriging_interpolation_model_residuals(DF,f,MODEL_POLLUTANT)[3][ix,iy]
        predicted_value.append(value)  
        print('EOI = {}, model = {}, measured = {} '.format(row['EOI'],value,row['pollutant']))
        #print('{}      {}      {}      {}'.format(row['name'], row['EOI'], value,  row['pollutant']))
    predicted_value=np.array(predicted_value)    
    RMSE=((np.sum((DF['pollutant']-predicted_value)**2))*(1/len((DF['pollutant']-predicted_value))))**0.5
    BIAS=np.sum((predicted_value-DF['pollutant']))/predicted_value.shape[0]
    r=np.corrcoef(predicted_value,DF['pollutant'] )[0,1]
    print('RMSE={}, BIAS={}, r={}'.format(RMSE,BIAS,r))
    
def validation_CMAQ(DF,f,MODEL_POLLUTANT):    
    """
    funkcia, ktora validuje CMAQ 
    """      
    print('###########################')
    print('leaving one validation for: CMAQ')   
    
    predicted_value=[]# this is the list of arrays, each array has 1 station dropped.
    for i, row in DF.iterrows():
        DF1=DF.drop([i])
        ix, iy = interpolation.getclosest_ij(f.variables['LAT'][0,0,:,:],f.variables['LON'][0,0,:,:],row['lat_x'],row['lon_x'] )
        value = MODEL_POLLUTANT[ix,iy]
        predicted_value.append(value)  
        print('EOI = {}, model = {}, measured = {} '.format(row['EOI'],value,row['pollutant']))
        #print('{}      {}      {}      {}'.format(row['name'], row['EOI'], value,  row['pollutant']))
    predicted_value=np.array(predicted_value)    
    RMSE=((np.sum((DF['pollutant']-predicted_value)**2))*(1/len((DF['pollutant']-predicted_value))))**0.5
    BIAS=np.sum((predicted_value-DF['pollutant']))/predicted_value.shape[0]
    r=np.corrcoef(predicted_value,DF['pollutant'] )[0,1]
    print('RMSE={}, BIAS={}, r={}'.format(RMSE,BIAS,r))
    