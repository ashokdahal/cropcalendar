#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sys
import arcpy
arcpy.CheckOutExtension("Spatial")
def rasterize (indir,outdir,season):

    output_data = outdir+"\\"+season+".tif"
    input_data= indir+'\\'+season+".shp"
    #Output_variance_of_prediction_raster=""
    #arcpy.gp.Kriging_sa(input_data, "Max_NDVI", output_data, "Spherical 0.000001", "1.0", "VARIABLE 12", Output_variance_of_prediction_raster)
    arcpy.FeatureToRaster_conversion(input_data, "date", output_data, "10.0")


if __name__ == "__main__":
    indir = sys.argv[1]
    outdir = sys.argv[2]
    season=sys.argv[3]
    rasterize (indir,outdir,season)
    

