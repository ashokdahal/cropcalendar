def extract_time_series(lat, lon, start, end, product_name, band_name, sf, mask):
    import ndvi_getCoords
    from datetime import datetime as dt
    import ndvi_getPointNDVI
    import ee 
    ee.Initialize()
    # Set up point geometry
    #point = ee.Geometry.Point(lon, lat)
    #define the geometry
    geometry = ee.FeatureCollection('users/ashok_dahal/'+mask)
    #s2_raw=ee.ImageCollection("COPERNICUS/S2_SR").filterDate('2019-01-01', '2019-05-01')
    # Obtain image collection for all images within query dates
    #coll = ee.ImageCollection(product_name).filterDate(start, end).filterBounds(geometry)
    coll = ee.ImageCollection(product_name).filterDate(start, end).filterBounds(geometry)#.select('NDVI')
    '''def computeNDVI(image):
        return image.addBands(image.normalizedDifference(['B3', 'B8']).rename('NDVI'))
    coll.map(computeNDVI)'''
    images = [item.get('id') for item in coll.getInfo().get('features')]
    
    def calculateNDVI(scene):
        dateString = ee.Date(scene.get('system:time_start')).format('yyyy-MM-dd')
        ndvi = scene.normalizedDifference(['B8', 'B4']).rename(dateString)
        return ndvi
    NDVIcollection = coll.map(calculateNDVI)
    #NDVIcollection
    def stackCollection(collection):
        first = ee.Image(collection.first()).select([])
        def appendBands (image, previous):
            return ee.Image(previous).addBands(image)
        return ee.Image(collection.iterate(appendBands, first))
    stacked = stackCollection(NDVIcollection)

    points_list=ndvi_getCoords.coordlist(ee.Image(images[0]),geometry)
    
    print(points_list)
    co_df,df=ndvi_getPointNDVI.getpointNDVI(stacked,images,points_list,band_name,sf)
    return co_df,df
'''  for image in images:
        iss = ee.Image(image)
        ndvi=iss.normalizedDifference(['B8','B4']).rename('NDVI')
        im=iss.addBands(ndvi)
        
        # Obtain date from timestamp in metadata
        date = dt.fromtimestamp(im.get("system:time_start").getInfo() / 1000.)
        date_store.append(np.datetime64(date))
        projection = im.select(band_name).projection().getInfo()['crs']
        # Extract pixel value
        data = im.select(band_name)\
        .reduceRegion(ee.Reducer.first(),
                      point,
                      1,
                      crs=projection)\
        .get(band_name)
        store.append(data.getInfo())'''

    # Scale the returned data based on scale factor
    #store = [x * sf if isinstance(x, float) else np.nan for x in store]

    # Convert output into pandas data frame
    #df = pd.DataFrame(index=date_store, data=store, columns=['NDVI'])

    #return df
