# This script merges rasters. The gdal_merge.py script from GDAL installation needs to be in your directory root folder then imported as a module.

import sys
sys.path.append('F:\Files\GIS\python_projects\open_source_geospatial')
import gdal_merge as gm
from osgeo import gdal
import time
import os
import shutil

gdal.PushErrorHandler('CPLQuietErrorHandler')
start_time = time.time()

input_directory = raw_input("Drag in your folder:  \n")
input_list = os.listdir(input_directory)

final_list = []

for x in input_list:
    if x.endswith('.tif'):
        final_list.append(os.path.join(input_directory, x))


def int_function():
    global output_full

    output_full = os.path.join(input_directory, 'Merged.tif')

    if len(final_list) == 2:
        filea = final_list[0]
        fileb = final_list[1]
        filec = ''
        filed = ''
    elif len(final_list) == 3:
        filea = final_list[0]
        fileb = final_list[1]
        filec = final_list[2]
        filed = ''
    elif len(final_list) == 4:
        filea = final_list[0]
        fileb = final_list[1]
        filec = final_list[2]
        filed = final_list[3]

    sys.argv = ['q', '-v', filea, fileb, filec, filed, "-o", output_full]
    gm.main()

    print 'Finished merging files...'


def move_files():
    print 'Moving files to new folder...'
    if not os.path.exists(os.path.join(input_directory, 'Merged')):

        os.mkdir(os.path.join(input_directory, 'Merged'))
        new_folder = os.path.join(input_directory, 'Merged')
        shutil.move(os.path.join(input_directory, output_full), new_folder)

    else:
        os.mkdir(os.path.join(input_directory, 'Merged_2'))
        new_folder = os.path.join(input_directory, 'Merged_2')
        shutil.move(os.path.join(input_directory, output_full), new_folder)

int_function()
move_files()

print '\nFinished ...'
print 'Program took {} seconds'.format(time.time() - start_time)
print 'See you later...'
time.sleep(2)

