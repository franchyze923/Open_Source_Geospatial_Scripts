from osgeo import ogr

shapefile = r"F:\Files\GIS\python_projects\open_source_geospatial\data\one.shp"
driver = ogr.GetDriverByName("ESRI Shapefile")
dataSource = driver.Open(shapefile, 0)
layer = dataSource.GetLayer()
layerDefinition = layer.GetLayerDefn()

layer_list = []

def get_fields():

    for i in range(layerDefinition.GetFieldCount()):
        layer_name = layerDefinition.GetFieldDefn(i).GetName()

        layer_list.append(layer_name)

def get_features():
    total_count = 0

    for x in layer_list:
        print 'THIS IS THE FIELD - {} \n'.format(x)

        for feature in layer:
            feat = feature.GetField(x)
            print 'FIELD - {} : FEATURE VALUE - {}'.format(x, feat)
            total_count += 1
            print 'Total feature count {}'.format(total_count)
        layer.ResetReading()  # reset the read position to the start

get_fields()
get_features()



