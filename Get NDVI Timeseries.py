#!/usr/bin/env python
# coding: utf-8

# In[26]:


import ee 
ee.Initialize()
start='2017-10-01'
end='2019-02-28'
geometry=ee.FeatureCollection('users/ashok_dahal/chitwan') #chitwan
coll = ee.ImageCollection("COPERNICUS/S2").filterDate(start, end).filterBounds(geometry) #ee.ImageCollection(product_name).filterDate(start, end).filterBounds(geometry)#.select('NDVI')
'''def computeNDVI(image):
    return image.addBands(image.normalizedDifference(['B3', 'B8']).rename('NDVI'))
coll.map(computeNDVI)'''
#images = [item.get('id') for item in coll.getInfo().get('features')]

def calculateNDVI(scene):
    dateString = ee.Date(scene.get('system:time_start')).format('yyyy-MM-dd')
    print(dateString)
    ndvi = scene.normalizedDifference(['B8', 'B4']).rename(dateString)
    return ndvi
NDVIcollection = coll.map(calculateNDVI)
#NDVIcollection
'''def stackCollection(collection):
    first = ee.Image(collection.first()).select([])
    def appendBands (image, previous):
        return ee.Image(previous).addBands(image)
    return ee.Image(collection.iterate(appendBands, first))
stacked = stackCollection(NDVIcollection)'''
stacked=NDVIcollection.toBands()


# In[27]:


stacked.bandNames().getInfo()


# In[28]:


from geetools import tools

region = tools.geometry.getRegion(geometry)


# In[29]:


task_config = {
    'scale': 100,  
    'region': region
    }

task = ee.batch.Export.image(stacked, 'exportExample', task_config)

task.start()


# In[34]:


task.status()


# In[11]:


from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)


# In[35]:


file_list = drive.ListFile({'q': "'root' in parents"}).GetList()
file_list[0]['id']


# In[36]:


file3 = drive.CreateFile({'id': file_list[0]['id']})
print('Downloading file %s from Google Drive' % file3['title']) # 'hello.png'
file3.GetContentFile(r'D:\chitwan\ndvi_series.tif')


# In[ ]:




