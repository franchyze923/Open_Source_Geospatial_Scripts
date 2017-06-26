# This script looks for values of 0 in the cells of a raster. It writes the results to a .txt.

from osgeo import gdal
import numpy as np
import os
import time

start_time = time.time()
input_directory = raw_input("Drag in your folder:  \n")
input_list = os.listdir(input_directory)

zero_value = []

for x in input_list:
    if x.endswith('.tif'):
        print '{}\n'.format(x)
        src_ds = gdal.Open(os.path.join(input_directory, x))
        num_bands = src_ds.RasterCount
        counter = 0
        zero_list = []
        print 'Raster band count = {}'.format(num_bands)

        rast_array = np.array(src_ds.GetRasterBand(1).ReadAsArray())

        print rast_array

        for b in rast_array:
            print b
            if 0 in b:
                print 'This array contains a zero!!!!!'
                zero_list.append(b)
            else:
                print 'This array does not contain a zero'
            counter += 1
            print '{}\n'.format(counter)
        zero_count = len(zero_list)
        zero_value.append(x)
        zero_value.append(zero_count)
    else:
        pass

print zero_value
thefile = open('test.txt', 'w')
for c in str(zero_value):
    thefile.write(c)

print '\nFinished ...'
print 'Program took {} seconds'.format(time.time() - start_time)
print 'See you later...'
time.sleep(15)