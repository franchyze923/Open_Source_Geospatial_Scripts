import Queue
import threading
from threading import current_thread
import subprocess
import os
import time

gdal_warp_location = r'C:\OSGeo4W\bin\gdalwarp.exe'  ## Set variable equal to the location of the gdal/ogr tool you want to use.

directory = raw_input('Drag in Directory containing data: \n').strip('"')
dir_list = os.listdir(directory)
start_time = time.time()

q = Queue.Queue()

for i in dir_list:  ##THIS IS WHERE WE ADD JOBS TO QUEUE
    full_path = os.path.join(directory, i)
    print 'Adding {} to the Queue'.format(full_path)
    q.put(full_path)

##This is the actual job

def worker():

    while True:

        item = q.get()
        print 'Processing {}...'.format(item)
        print current_thread().name
        file_namer = os.path.basename(item)

        command1 = [gdal_warp_location, '-t_srs', 'EPSG:2016', item, os.path.join(directory, 'Reprojected_{}'.format(file_namer))]
        subprocess.check_call(command1)
        q.task_done()

hardcode_cpu_numb = 5
print '\nCreating {} threads - '.format(hardcode_cpu_numb)

for i in range(hardcode_cpu_numb):
    t = threading.Thread(target=worker)
    t.daemon = True
    t.start()

q.join()

print "\nPROCESSED {0} FILES!!".format(len(dir_list))
print '\nProgram took {} seconds to complete...\n'.format(time.time() - start_time)
