from qgis.core import *
from PyQt4 import QtGui
import os, time, datetime

program_start = datetime.datetime.now().time()
start_time = time.time()
print 'Program started at ', program_start

app = QtGui.QApplication([])
QgsApplication.setPrefixPath(r"C:\OSGeo4W\apps\qgis", True)
QgsApplication.initQgis()

folder = r'C:\Users\fpoli\Desktop\PyTest2'
layer = QgsVectorLayer(r'C:\Users\fpoli\Desktop\PyTest2\New_Shapefile(2).shp', "test", "ogr")
layerPath = r'F:\Files\GIS\New_Shapefile.shp'

if not layer.isValid():
  print "Layer failed to load!"
else:
    print 'Files loaded sucessfully!!!! \n'

extent = QgsVectorLayer(layerPath, '', 'ogr').extent()
request = QgsFeatureRequest()
request.setFilterRect(extent)

features_to_leave = []
features_to_delete = []
counter = 0
for feature in layer.getFeatures(request):

    #print "Feature ID %d: " % feature.id()
    attrs = feature.attributes()
    #print attrs[0]
    features_to_leave.append(attrs[0])

print 'These are features that are inside of the box, that we WANT TO KEEP:'
print features_to_leave, '\n'

for x in layer.getFeatures():
    attrs = x.attributes()

    if attrs[0] in features_to_leave:
        pass
    else:
        features_to_delete.append(attrs[0])

print 'These are features that are outside of the box, we WANT TO DELETE THESE:'
print features_to_delete, '\n'

for x in features_to_delete:

    name_checker = str(x) + '.tif'
    print 'this is name checker {}'.format(name_checker)
    for root, dir2, files in os.walk(folder):
        print 'This is the root directory at the moment..the following are files inside of it {}'.format(root)

        for b in files:
            local_folder = os.path.join(folder, root)
            print 'Here is name of file {}'.format(b)
            print 'Here is name of name checker {}'.format(name_checker)

            if b == name_checker:
                counter += 1
                print '{} needs to be deleted..'.format(b)
                #os.remove(os.path.join(local_folder, b))
                print 'Removed {} \n'.format(os.path.join(folder, b))

            else:
                print 'This file can stay {} \n'.format(b)


print 'FINISHED!! SUCESSFULLY DELETED {} FILES \n'.format(counter)
print("Program took --- {} seconds --- to complete" .format(time.time() - start_time))

QgsApplication.exitQgis()


