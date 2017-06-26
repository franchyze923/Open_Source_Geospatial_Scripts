## This script takes a rectangle shapefile and splits it up into even parts based on number input by user. 

from osgeo import ogr, osr
import os, sys
import argparse

parser = argparse.ArgumentParser(description='Shapefile Splitter', version='0.9')
parser.add_argument('Shapefile', nargs=1, type=str, help='Path to Shapefile')
parser.add_argument('SplitNum', nargs=1, type=int, help='Number of boxes you want to make')

if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)

args = vars(parser.parse_args())

inShapefile = args['Shapefile'][0]
split_number = args['SplitNum'][0]

inDriver = ogr.GetDriverByName("ESRI Shapefile")
inDataSource = inDriver.Open(inShapefile, 0)
inLayer = inDataSource.GetLayer()

sourceprj = inLayer.GetSpatialRef()
fullPrj = sourceprj.GetAttrValue('authority', 1)

extent = inLayer.GetExtent()
extent = list(extent)

xmin, xmax, y_min, y_max = extent[0], extent[1], extent[2], extent[3]

x_diff = xmax-xmin
x_increase = x_diff/split_number
new_xmax = xmin + x_increase

for x in range(split_number):

    ring = ogr.Geometry(ogr.wkbLinearRing)
    ring.AddPoint(extent[0], extent[2])
    ring.AddPoint(new_xmax, extent[2])
    ring.AddPoint(new_xmax, extent[3])
    ring.AddPoint(extent[0], extent[3])
    ring.AddPoint(extent[0], extent[2])
    poly = ogr.Geometry(ogr.wkbPolygon)
    poly.AddGeometry(ring)

    outShapefile = os.path.join(os.path.dirname(inShapefile), 'Box_{}.shp'.format(str(x)))
    outDriver = ogr.GetDriverByName("ESRI Shapefile")
    out_shape_prj = outShapefile[:-4]+'.prj'

    if os.path.exists(outShapefile):
        outDriver.DeleteDataSource(outShapefile)

    outDataSource = outDriver.CreateDataSource(outShapefile)
    outLayer = outDataSource.CreateLayer(r"fff", geom_type=ogr.wkbPolygon)

    idField = ogr.FieldDefn("id", ogr.OFTInteger)
    outLayer.CreateField(idField)
    spatialRef = osr.SpatialReference()
    spatialRef.ImportFromEPSG(int(fullPrj))
    spatialRef.MorphToESRI()

    prj_file_path = out_shape_prj
    prj_file = open(prj_file_path, 'w')
    prj_file.write(spatialRef.ExportToWkt())
    prj_file.close()

    featureDefn = outLayer.GetLayerDefn()
    feature = ogr.Feature(featureDefn)
    feature.SetGeometry(poly)
    feature.SetField("id", 1)
    outLayer.CreateFeature(feature)

    extent[0] = extent[0] + x_increase
    new_xmax = new_xmax + x_increase

