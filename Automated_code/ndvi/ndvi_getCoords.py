import ee
ee.Initialize()
def coordlist(image,geometry):
    img=image.select('B4')
    coordsImage = ee.Image.pixelLonLat().reproject(img.projection())
    coordsList = coordsImage.reduceRegion(ee.Reducer.toList(2), geometry).values().get(0)

    coordsList = ee.List(coordsList)

    return(coordsList.getInfo())