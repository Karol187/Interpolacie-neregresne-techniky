# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 17:40:36 2020

@author: kocok
"""

import interpolation
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
# setting of basemap
plt.rcParams['figure.figsize'] =20,7
meridians = np.arange(16.,35.,1.)
pararels = np.arange(46.,50.,1.)
d03={'projection': 'lcc',
     'llcrnrlon': 16.804249173287925,
     'llcrnrlat': 47.67911406210376,
     'urcrnrlon': 22.66823971637524,
     'urcrnrlat': 49.53739914689373,
     'resolution': 'i',
     'lat_1': 46.24470138549805,
     'lat_2': 46.24470138549805,
     'lat_0': 46.24470138549805,
     'lon_0': 17.0,
     'rsphere': 6370000.0}
mapb=Basemap(**d03)



def maps_of_interpolations(DF,f, name,interpolation_type) :
    """
    funkcia, ktora zobrazi mapu IDW alebo kriging interpolaciu nameranych koncentracii 
    """
    print('###########################')
    print('leaving one map for: ' + interpolation_type)      
    
   
    if interpolation_type == 'IDW':
         mapb.drawcountries()
         mapb.pcolormesh(f.variables['LON'][0,0,:,:],f.variables['LAT'][0,0,:,:],interpolation.idw_interpolation(DF,f),cmap=plt.cm.jet,latlon=True) 
         mapb.readshapefile('C:/Users/kocok/Desktop/Shapefile0/slovensko','slovensko', drawbounds= True,linewidth=4)
         plt.colorbar(label=name+ ' [$\mu$g.$m^{-3}$]',extend='max')
         plt.title('IDW interpolácia nameraných koncentrácií ' +name+ ' za rok 2017',fontsize=15)
         plt.clim(0,40)         
         mapb.scatter(DF['lon_x'].values, DF['lat_x'].values,c=DF['pollutant'].values,s=30 , latlon=True,cmap='jet',alpha=1, edgecolors='black')
         plt.clim(0,40)
         #plt.show() 
         plt.savefig('Idw interpolacia nameranych koncentrácii.png',bbox_inches='tight',dpi=600)
         #plt.savefig('Idw p4.png',bbox_inches='tight',dpi=600)
         plt.clf()
    elif interpolation_type == 'kriging':
         mapb.drawcountries()
         mapb.pcolormesh(f.variables['LON'][0,0,:,:],f.variables['LAT'][0,0,:,:],interpolation.kriging_interpolation(DF,f),cmap=plt.cm.jet,latlon=True) 
         mapb.readshapefile('C:/Users/kocok/Desktop/Shapefile0/slovensko','slovensko', drawbounds= True,linewidth=4)
         plt.colorbar(label=name+ ' [$\mu$g.$m^{-3}$]',extend='max')
         plt.title('OK interpolácia nameraných koncentrácií ' +name+ ' za rok 2017',fontsize=15)
         plt.clim(0,40)
         mapb.scatter(DF['lon_x'].values, DF['lat_x'].values,c=DF['pollutant'].values,s=30 , latlon=True,cmap='jet',alpha=1, edgecolors='black')
         plt.clim(0,40)
         #plt.show() 
         plt.savefig('OK interpolacia nameranych koncentrácii.png',bbox_inches='tight',dpi=600)
         plt.clf()
def maps_of_interpolations_model_residuals(DF,f,MODEL_POLLUTANT,name, interpolation_type):  
    """
    funkcia, ktora zobrazi mapu IDW alebo kriging interpolacie rezidui. Rezidua su rozdiely medzi nameranymi hodnotami a hodnotzmi z CMAQ mmodelu
    """
    print('###########################')
    print('leaving one map for: ' + interpolation_type)      
    
    
    if interpolation_type == 'IDW':
         mapb.drawcountries()
         mapb.pcolormesh(f.variables['LON'][0,0,:,:],f.variables['LAT'][0,0,:,:],interpolation.idw_interpolation_model_residuals(DF,f,MODEL_POLLUTANT)[2],cmap=plt.cm.jet,latlon=True) 
         mapb.readshapefile('C:/Users/kocok/Desktop/Shapefile0/slovensko','slovensko', drawbounds= True,linewidth=4)
         plt.colorbar(label=name+ ' [$\mu$g.$m^{-3}$]')
         plt.title('IDW interpolácia rezíduí',fontsize=15)
         mapb.scatter(DF['lon_x'].values, DF['lat_x'].values,c=interpolation.idw_interpolation_model_residuals(DF,f,MODEL_POLLUTANT)[4],s=30 , latlon=True,cmap='jet',alpha=1, edgecolors='black')
         #plt.show() 
         plt.savefig('idw interpolacia reziduii.png',bbox_inches='tight',dpi=600)
         plt.clf()
    elif interpolation_type == 'kriging':
         mapb.drawcountries()
         mapb.pcolormesh(f.variables['LON'][0,0,:,:],f.variables['LAT'][0,0,:,:],interpolation.kriging_interpolation_model_residuals(DF,f,MODEL_POLLUTANT)[2],cmap=plt.cm.jet,latlon=True) 
         mapb.readshapefile('C:/Users/kocok/Desktop/Shapefile0/slovensko','slovensko', drawbounds= True,linewidth=4)
         plt.colorbar(label=name + ' [$\mu$g.$m^{-3}$]')
         plt.title('OK interpolácia rezíduí',fontsize=15)
         plt.clim(min(interpolation.idw_interpolation_model_residuals(DF,f,MODEL_POLLUTANT)[4]),max(interpolation.idw_interpolation_model_residuals(DF,f,MODEL_POLLUTANT)[4]))
         mapb.scatter(DF['lon_x'].values, DF['lat_x'].values,c=interpolation.idw_interpolation_model_residuals(DF,f,MODEL_POLLUTANT)[4],s=30 , latlon=True,cmap='jet',alpha=1, edgecolors='black')
         
         #plt.show()   
         plt.savefig('ok interpolacia reziduii.png',bbox_inches='tight',dpi=600)
         plt.clf()

         
def maps_of_interpolations_model_plus_residuals(DF,f,MODEL_POLLUTANT,name, interpolation_type):  
    """
    funkcia, ktora zobrazi mapu CMAQ +idw alebo kriging interpolaciu rezidui.
    """
    print('###########################')
    print('leaving one map for: ' + interpolation_type)      
    
    
    if interpolation_type == 'CMAQ+IDW':
         mapb.drawcountries()
         mapb.pcolormesh(f.variables['LON'][0,0,:,:],f.variables['LAT'][0,0,:,:],interpolation.idw_interpolation_model_residuals(DF,f,MODEL_POLLUTANT)[3],cmap=plt.cm.jet,latlon=True)
         mapb.readshapefile('C:/Users/kocok/Desktop/Shapefile0/slovensko','slovensko', drawbounds= True,linewidth=4)
         plt.colorbar(label=name+ ' [$\mu$g.$m^{-3}$]',extend='max')
         plt.title('Chemicko-transportný model + IDW interpolácia rezíduí',fontsize=15)  
         plt.clim(0,40)
         mapb.scatter(DF['lon_x'].values, DF['lat_x'].values,c=DF['pollutant'].values,s=30 , latlon=True,cmap='jet',alpha=1, edgecolors='black')
         plt.clim(0,40)
         #plt.show() 
         plt.savefig('cmaq+idw reziduii.png',bbox_inches='tight',dpi=600)
         plt.clf()
    elif interpolation_type == 'CMAQ+kriging':
         mapb.drawcountries()
         mapb.pcolormesh(f.variables['LON'][0,0,:,:],f.variables['LAT'][0,0,:,:],interpolation.kriging_interpolation_model_residuals(DF,f,MODEL_POLLUTANT)[3],cmap=plt.cm.jet,latlon=True) 
         mapb.readshapefile('C:/Users/kocok/Desktop/Shapefile0/slovensko','slovensko', drawbounds= True,linewidth=4)
         plt.colorbar(label=name+ ' [$\mu$g.$m^{-3}$]',extend='max')
         plt.title('Chemicko-transportný model + OK interpolácia rezíduí',fontsize=15)
         plt.clim(0,40)
         mapb.scatter(DF['lon_x'].values, DF['lat_x'].values,c=DF['pollutant'].values,s=30 , latlon=True,cmap='jet',alpha=1, edgecolors='black')
         plt.clim(0,40)
         #plt.show()
         plt.savefig('cmaq+ok reziduii.png',bbox_inches='tight',dpi=600)
         plt.clf()

def map_CMAQ(DF,f,MODEL_POLLUTANT,name):
    """
    funkcia, ktora zobrazi mapu modelu CMAQ
    """
    print('###########################')
    print('leaving one map for: CMAQ ')
    mapb.drawcountries()
    mapb.pcolormesh(f.variables['LON'][0,0,:,:],f.variables['LAT'][0,0,:,:],MODEL_POLLUTANT,cmap=plt.cm.jet,latlon=True)
    mapb.readshapefile('C:/Users/kocok/Desktop/Shapefile0/slovensko','slovensko', drawbounds= True,linewidth=4)
    plt.colorbar(label=name+ ' [$\mu$g.$m^{-3}$]',extend='max')
    plt.title('Chemicko-transportný model',fontsize=15)
    plt.clim(0,40)
    mapb.scatter(DF['lon_x'].values, DF['lat_x'].values,c=DF['pollutant'].values,s=30 , latlon=True,cmap='jet',alpha=1, edgecolors='black')
    plt.clim(0,40)
    #plt.show() 
    plt.savefig('cmaq.png',bbox_inches='tight',dpi=600)
    plt.clf()
    










    
