def getpointNDVI(images,cords,band_name,sf):
    import pandas as pd
    import ee
    from datetime import datetime as dt
    import numpy as np
    ee.Initialize()
    co_df=pd.DataFrame(cords, columns=['LON','LAT'])
    print(co_df)
    ID_List=[]
    df=pd.DataFrame()
    FID=0
    #points=ee.Geometry.MultiPoint(cords)
    #print(points.geometries())
    for cord in cords:
        store = []
        date_store = []
        lon=cord[0]
        lat=cord[1]
        print(lon,lat)
        pointn = ee.Geometry.Point(lon, lat)
        for image in images:
            iss = ee.Image(image)
            ndvi=iss.normalizedDifference(['B8','B4']).rename('NDVI')
            im=iss.addBands(ndvi)
            projection = im.select(band_name).projection().getInfo()['crs']
            
            # Obtain date from timestamp in metadata
            date = dt.fromtimestamp(im.get("system:time_start").getInfo() / 1000.)
            date_store.append(np.datetime64(date))
            
            # Extract pixel value
            data = im.select(band_name)\
            .reduceRegion(ee.Reducer.first(),
                          pointn,
                          1,
                          crs=projection)\
            .get(band_name)
            store.append(data.getInfo())
        # Scale the returned data based on scale factor
        if FID<1:
            store = [x * sf if isinstance(x, float) else np.nan for x in store]
            print(store)
    # Convert output into pandas data frame
            df = pd.DataFrame(index=date_store, data=store, columns=[FID])
        else:
            store = [x * sf if isinstance(x, float) else np.nan for x in store]
            print(store)
    # Convert output into pandas data frame
            df[FID] = store
        FID=FID+1
    return co_df,df
        
        
        