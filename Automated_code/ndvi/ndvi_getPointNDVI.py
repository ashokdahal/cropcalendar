def getpointNDVI(stacked,images,cords,band_name,sf):
    import pandas as pd
    import ee
    from datetime import datetime as dt
    import numpy as np
    ee.Initialize()
    co_df=pd.DataFrame(cords, columns=['LON','LAT'])
    print(co_df)
    #ID_List=[]
    #df=pd.DataFrame()
    FID=0
    #points=ee.Geometry.MultiPoint(cords)
    #print(points.geometries())
    #pixels=list(range(0, len(cords)))
    #df = pd.DataFrame(columns=pixels)
    image=images[0]
    im = ee.Image(image)
    #date = dt.fromtimestamp(im.get("system:time_start").getInfo() / 1000.)
    projection = im.select('B1').projection().getInfo()['crs']
    data_dic={}
    #print(date,projection)
    for cord in cords:
        lon=cord[0]
        lat=cord[1]
        print(lon,lat)
        pointn = ee.Geometry.Point(lon, lat)
        data = stacked.reduceRegion(ee.Reducer.first(),pointn,1,crs=projection)
        data_dic[FID]=data.getInfo()
        del data
        FID+=1
        per=(float(FID)/float(len(cords)))*100
        print(per,'%')
    df=pd.DataFrame.from_dict(data_dic)
    print(df)
    return co_df,df
