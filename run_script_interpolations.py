# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 17:16:02 2020

@author: kocok
"""

import pandas as pd
import numpy as np
import netCDF4
import validation_interpolation
import interpolation_maps

DF=pd.read_csv(r"C:\Users\kocok\Desktop\Bakalarska praca hlavne programy\inputs\tabulka_surova_PM10.csv",delimiter=',')
#DF=pd.read_csv(r"C:\Users\kocok\Desktop\Bakalarska praca hlavne programy\inputs\tabulka_surova_NO2_2017.csv",delimiter=',')
f = netCDF4.Dataset(r"C:\Users\kocok\Desktop\Bakalarska praca hlavne programy\inputs\GRIDCRO2D_2017-01-01.nc") 
MODEL_POLLUTANT=np.float32(np.load(r"C:\Users\kocok\Desktop\Bakalarska praca hlavne programy\inputs\mapa_pm10_v6.npy"))

DF['pollutant']=DF['PM10']
DF['lat_x']=DF['lat_x']
DF['lon_x']=DF['lon_x']
name='PM$_{10}$'
#name='NO$_{2}$'
interpolation_maps.maps_of_interpolations(DF,f,name,interpolation_type='IDW')
interpolation_maps.maps_of_interpolations(DF,f,name,interpolation_type='kriging')
interpolation_maps.map_CMAQ(DF,f,MODEL_POLLUTANT,name)
interpolation_maps.maps_of_interpolations_model_residuals(DF,f,MODEL_POLLUTANT,name,interpolation_type='IDW')
interpolation_maps.maps_of_interpolations_model_residuals(DF,f,MODEL_POLLUTANT,name,interpolation_type= 'kriging')
interpolation_maps.maps_of_interpolations_model_plus_residuals(DF,f,MODEL_POLLUTANT,name,interpolation_type= 'CMAQ+IDW')
interpolation_maps.maps_of_interpolations_model_plus_residuals(DF,f,MODEL_POLLUTANT,name,interpolation_type= 'CMAQ+kriging')
validation_interpolation.validation_of_interpolations(DF,f,interpolation_type='IDW')
validation_interpolation.validation_of_interpolations(DF,f,interpolation_type='kriging')
validation_interpolation.validation_CMAQ(DF,f,MODEL_POLLUTANT)
validation_interpolation.validation_of_interpolations_model_residuals(DF,f,MODEL_POLLUTANT,interpolation_type= 'CMAQ+IDW')
validation_interpolation.validation_of_interpolations_model_residuals(DF,f,MODEL_POLLUTANT,interpolation_type= 'CMAQ+kriging')

