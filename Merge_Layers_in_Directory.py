import os, ogr, osr

outputName = 'merged.shp'
directory = r"E:\metadata_2\data\folder"
fileEndsWith = '.shp'
driverName = 'ESRI Shapefile'
geometryType = ogr.wkbPolygon

out_driver = ogr.GetDriverByName( driverName )

output_location = os.path.join(directory, outputName) ####this is how you specify location of output file

if os.path.exists(output_location):
    out_driver.DeleteDataSource(output_location) ## dont know what this does.. it doens overwrite like i thought

out_ds = out_driver.CreateDataSource(output_location)
out_layer = out_ds.CreateLayer(output_location, geom_type=geometryType)

fileList = os.listdir(directory)

for file in fileList:
    if file.endswith(fileEndsWith):
        ds = ogr.Open(os.path.join(directory, file))
        lyr = ds.GetLayer()
        print 'Merging {}'.format(file)
        for feat in lyr:
            out_feat = ogr.Feature(out_layer.GetLayerDefn())
            out_feat.SetGeometry(feat.GetGeometryRef().Clone())
            out_layer.CreateFeature(out_feat)
            out_layer.SyncToDisk()

print '\nFinished Merging, created new file located at {}'.format(output_location)