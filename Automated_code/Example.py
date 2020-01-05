#!/usr/bin/env python
# coding: utf-8

# In[2]:


import sys
sys.path.append('ndvi')
import ndvi_getStart
import ndvi_getEnd
import ndvi_getFeatBound
import ndvi_getCoords
import ndvi_getCropCalendar
import ndvi_getPointNDVI
import ndvi_getTimeSeries
import ndvi_saveDatabase
import ndvi_saveExcel


# In[3]:


if __name__ == "__main__":


    latitude = 27.757079899550654
    longitude = 85.38746094213771
    feature_bound='sample1'#getfeatbound()
    start_date = '2019-05-01'#getstart()
    end_date = '2019-09-26'#getend()
    product = 'COPERNICUS/S2_SR' 
    band = 'NDVI'
    scale_factor = 0.02
    smooth_factor=0.25

    # Extract data and obtain pd.DataFrame
    df_cord,df_ndvi = ndvi_getTimeSeries.extract_time_series(latitude,
                                 longitude,
                                 start_date,
                                 end_date,
                                 product,
                                 band,
                                 scale_factor,
                                 feature_bound)
    
    #crop_calendar=ndvi_getCropCalendar.get_crop_calendar(df_cord,df_ndvi,smooth_factor)
    #output.plot()


# In[9]:


crop_calendar=ndvi_getCropCalendar.get_crop_calendar(df_cord,df_ndvi,smooth_factor)


# In[12]:


ndvi_saveExcel.dfToCSV(r'D:/','G5',crop_calendar)


# In[13]:


ndvi_saveDatabase.savePostgres(crop_calendar,'G5','localhost','5432','postgres','gicait123','postgres')


# In[ ]:




