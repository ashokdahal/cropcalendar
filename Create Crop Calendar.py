#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import gdal
src_ds = gdal.Open(r"D:\chitwan_single.tif")
n_band=src_ds.RasterCount
if src_ds is not None: 
    print ("band count: " + str(src_ds.RasterCount))
ls=[]
raster_shape=src_ds.GetRasterBand(1).ReadAsArray().shape
for i in range(n_band):
    var='attr'+str(i)
    ls.append(np.array(src_ds.GetRasterBand(i+1).ReadAsArray()))
    print(i)


# In[2]:


trap=zip(*map(lambda x:x.flatten(),ls))


# In[3]:


import numpy as np
from scipy.signal import argrelextrema


# In[4]:


import statsmodels.api as sm
from scipy.signal import argrelextrema
from datetime import datetime
lowess = sm.nonparametric.lowess
eos1=[]
eos2=[]
eos3=[]
eos4=[]
sos1=[]
sos2=[]
sos3=[]
sos4=[]
min=[]
ls=np.array(list(range(n_band)))
x=0
for i in trap:
    arr=np.asarray(i).astype('float64') 
  
    print(ls.size,arr.size)
    #xout, yout, weigts = loess_1d(ls, arr, frac=0.3)
    #w=lowess(arr, ls, frac=0.2, it=100, delta=0.2, is_sorted=False, missing='drop', return_sorted=True)
    '''xout=[]
    yout=[]
    #if len(w)==0:
     #   continue
    #for el in w:
       xout.append(el[0])
        yout.append(el[1])
    #print(xout,yout)
    del i,arr,xout'''
    #del arr
    #arr=np.asarray(w).astype('float64') 
    y=argrelextrema(arr, np.greater)[0]
    x_max=argrelextrema(arr, np.less)[0]
    #del arr
    #conditions for the first SOS
    #print(x_max)
    #newArr = x_max[(x_max>4.0)&(x_max<15.0)][0]
    #............condition for EOS1..........#
    try:
        newArr = x_max[(x_max>15)&(x_max<40)][0]
        #print('here')
    except:
        newArr=np.nan
    #print(newArr)
    eos1.append(newArr)
    del newArr
    
    #............condition for EOS2..........#
    try:
        newArr = x_max[(x_max>40)&(x_max<66)][0]
        #print('here')
    except:
        newArr=np.nan
    #print(newArr)
    eos2.append(newArr)
    del newArr
    #............condition for EOS3..........#
    
    try:
        newArr = x_max[(x_max>66)&(x_max<75)][0]
        #print('here')
    except:
        newArr=np.nan
    #print(newArr)
    eos3.append(newArr)
    del newArr
    #............condition for EOS4..........#
    
    try:
        newArr = x_max[(x_max>75)&(x_max<95)][0]
        #print('here')
    except:
        newArr=np.nan
    #print(newArr)
    eos4.append(newArr)
    del newArr
    #...............EOS Complete......#
    
    #...............Condition for SOS1........#
    try:
        newArr = y[(y>1)&(y<18)][0]
    except:
        newArr=np.nan
        
    sos1.append(newArr)
    del newArr
    #...............Condition for SOS2........#
    
    try:
        newArr = y[(y>18)&(y<36)][0]
    except:
        newArr=np.nan
        
    sos2.append(newArr)
    del newArr
    #...............Condition for SOS3........#
    
    try:
        newArr = y[(y>36)&(y<54)][0]
    except:
        newArr=np.nan
        
    sos3.append(newArr)
    del newArr
        #...............Condition for SOS4........#
        
    try:
        newArr = y[(y>54)&(y<72)][0]
    except:
        newArr=np.nan
        
    sos4.append(newArr)
    del newArr
    #............EOS Compelete.......#
    
    print(x)
    x+=1
    del y,x_max
    


# In[5]:


#las=[]
#print(max)
eos1_ras=np.asarray(eos1).reshape(raster_shape)*5
eos2_ras=np.asarray(eos2).reshape(raster_shape)*5
eos3_ras=np.asarray(eos3).reshape(raster_shape)*5
eos4_ras=np.asarray(eos4).reshape(raster_shape)*5
sos1_ras=np.asarray(sos1).reshape(raster_shape)*5
sos2_ras=np.asarray(sos2).reshape(raster_shape)*5
sos3_ras=np.asarray(sos3).reshape(raster_shape)*5
sos4_ras=np.asarray(sos4).reshape(raster_shape)*5
#print(maximum)


# In[6]:


import rasterio as rio    

with rio.open(r"D:\chitwan\ndvi_series.tif") as src2:
    ras_data = src2.read()#GetRasterBand(1)
    #ras_data=ras_data_pre.GetRasterBand(1)
    ras_meta = src2.profile

# make any necessary changes to raster properties, e.g.:
ras_meta['dtype'] = "float64"
ras_meta['nodata'] = -99
ras_meta['count']=4

with rio.open(r"D:\chitwan\season_min_1.tif", 'w', **ras_meta) as dst:
    dst.write(sos1_ras,1)
with rio.open(r"D:\chitwan\season_min_2.tif", 'w', **ras_meta) as dst:
    dst.write(sos2_ras,1)
with rio.open(r"D:\chitwan\season_min_3.tif", 'w', **ras_meta) as dst:
    dst.write(sos3_ras,1)
with rio.open(r"D:\chitwan\season_min_4.tif", 'w', **ras_meta) as dst:
    dst.write(sos4_ras,1)
with rio.open(r"D:\chitwan\season_max_1.tif", 'w', **ras_meta) as dst:
    dst.write(eos1_ras,1)
with rio.open(r"D:\chitwan\season_max_2.tif", 'w', **ras_meta) as dst:
    dst.write(eos2_ras,1)
with rio.open(r"D:\chitwan\season_max_3.tif", 'w', **ras_meta) as dst:
    dst.write(eos3_ras,1)
with rio.open(r"D:\chitwan\season_max_4.tif", 'w', **ras_meta) as dst:
    dst.write(eos4_ras,1)
    


# In[15]:


import rasterio
from matplotlib import pyplot
flo=r"D:\chitwan\season_max_1.tif"
sav=r"D:\chitwan\season_max_1.png"
src = rasterio.open(flo)
'''mini= datetime.datetime.strptime(str(mini_in), '%y%m%d')
maxi=datetime.datetime.strptime(str(maxi_in), '%y%m%d')
diff=int((maxi-mini).days/5)
int0=mini.strftime("%y%m%d")
int1=(mini+ datetime.timedelta(days=diff)).strftime("%y%m%d")  
int2=(mini+ datetime.timedelta(days=diff*2)).strftime("%y%m%d")  
int3=(mini+ datetime.timedelta(days=diff*3)).strftime("%y%m%d")  
int4=(mini+ datetime.timedelta(days=diff*4)).strftime("%y%m%d")  
int5=(mini+ datetime.timedelta(days=diff*5)).strftime("%y%m%d")


from matplotlib.colors import from_levels_and_colors
cmap, norm = from_levels_and_colors([int(int0),int(int1),int(int2),int(int3),int(int4),int(int5)],['lightgreen','lawngreen','limegreen','forestgreen','darkgreen'])
#plt.imshow(data, cmap=cmap, norm=norm)
'''

pyplot.imshow(src.read(1), cmap='Greens')
#pyplot.legend()
pyplot.colorbar(format='%5.0f')
pyplot.axis('off')
pyplot.savefig(sav)
pyplot.show()
pyplot.close()


# In[17]:


import jinja2
import os
outdir=r"D:\chitwan"
#outdir
os.chdir(r"D:\Bhogendra Dai Deliverable\Without_report")
templateLoader = jinja2.FileSystemLoader(searchpath="./")
templateEnv = jinja2.Environment(loader=templateLoader)
TEMPLATE_FILE = "report_head.txt"
template = templateEnv.get_template(TEMPLATE_FILE)
html_file = open(outdir+"\\"+'report' + '.html', 'w')

outputText = template.render(start_date="2017-10-01",end_date="2019-03-28",ndvi_image="plot.png",sample_location="site.png")
#html_file.write(outputText)
max_seasons=['season_max_1','season_max_2','season_max_3','season_max_4']
for season in max_seasons:
    templateLoader2 = jinja2.FileSystemLoader(searchpath="./")
    templateEnv2 = jinja2.Environment(loader=templateLoader2)
    TEMPLATE_FILE = "report_body.txt"
    template = templateEnv.get_template(TEMPLATE_FILE)
    min_season=season.replace("max","min")
    season_nm=season.replace("_max_","  ")
    print(min_season)
    outputText2 = template.render(start_date="2019-09-01",end_date="2019-10-01",season=season_nm,ndvi_image="plot.png",season_date="Multiple Date",max_ndvi_image=season+".png",min_ndvi_image=min_season+".png")
    
    outputText=outputText+outputText2
    del outputText2
html_file.write(outputText)
html_file.close()

import pdfkit

path_wkthmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
pdfkit.from_file(outdir+"\\"+'report' + '.html', outdir+"\\"+'report' + '.pdf', configuration=config)


# In[ ]:




