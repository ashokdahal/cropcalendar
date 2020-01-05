var s2 = ee.ImageCollection("COPERNICUS/S2"),
    bound = ee.FeatureCollection('users/ashok_dahal/mechi'),
    point=ee.Geometry.Point([80.58,28.8]);

var filteredIC = s2.filterBounds(point)
    .filterDate('2017-10-01', '2019-02-28')
    //.sort('CLOUD_COVER')

var addDataBands = function(image) {
  var ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI');
  return image.addBands(ndvi)
              .addBands(image.metadata('system:time_start').divide(1e18).rename('time'));
};

// Function to smooth time series
// stacks windows of linear regression results
// requires that a variable 'data' exists with NDVI and time bands
function smoother(t){
  // helper function to apply linear regression equation
  function applyFit(img){
      return img.select('time').multiply(fit.select('scale')).add(fit.select('offset'))
              .set('system:time_start',img.get('system:time_start')).rename('NDVI');
  }
  t = ee.Date(t);
  
  var window = data.filterDate(t.advance(-windowSize,'day'),t.advance(windowSize,'day'));
    
  var fit = window.select(['time','NDVI'])
    .reduce(ee.Reducer.linearFit());
    
  return window.map(applyFit).toList(5);
}

// function to reduce time stacked linear regression results
// requires that a variable 'fitIC' exists from the smooter function
function reduceFits(t){
  t = ee.Date(t);
  var dates=t.format('DD');
  return fitIC.filterDate(t.advance(-windowSize,'day'),t.advance(windowSize,'day'))
              .mean().set('system:time_start',t.millis()).rename(dates);
}

var data = filteredIC.map(addDataBands);
print(data);

var dates = ee.List(data.aggregate_array('system:time_start'));
//print(ee.date(1507006975670));
var windowSize = 30; //days on either side

var fitIC = ee.ImageCollection(dates.map(smoother).flatten());

var smoothed = ee.ImageCollection(dates.map(reduceFits));


//var mergeBands = function(image, previous) {
//  return ee.Image(previous).addBands(image.select(['NDVI'],['smoothed']));
//};
var geometry=ee.FeatureCollection('users/ashok_dahal/nepal');
var exp=smoothed.toBands();//smoothed.select(['NDVI'],['smoothed']).toBands();//smoothed.toBands();
//var merged = smoothed.iterate(mergeBands, ee.Image([]));
exp=exp.clip(geometry)
//exp=exp.toUint16()
Export.image.toDrive({
  image: exp,
  description: 'chitwan',
  scale: 100,
  maxPixels: 507303336000//,
  //region: exp.geometry()
});
print("done");

Map.addLayer(exp,{min:0,max:1.0},'Smoothed');
