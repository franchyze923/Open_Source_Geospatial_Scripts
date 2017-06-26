import subprocess
import os

ogr2ogr_location = r'C:\Program Files\QGIS 2.18\bin\ogr2ogr.exe'
gdal_warp_location = r'C:\Program Files\QGIS 2.18\bin\gdalwarp.exe'

print "\nWelcome to Fran's Geospatial Utility Tool\n"

what_to_do = raw_input('Press 1 to reproject a raster or vector \nPress 2 to convert a kml to shapefile ')

while True:

    if what_to_do == '1' or what_to_do == '2':
        break
    else:
        what_to_do = raw_input('Input is incorrect, valid inputs are 1 or 2 ')

if what_to_do == '1':

    reproject_input = raw_input('\nDrag in your raster or vector file ').strip('"').strip('"')

    utm_codes = {1: (32601, 32701), 2: (32602, 32702), 3: (32603, 32703), 4: (32604, 32704), 5: (32605, 32705),
                 6: (32606, 32706), 7: (32607, 32707), 8: (32608, 32708), 9: (32609, 32709),
                 10: (32610, 32710),
                 11: (32611, 32711), 12: (32612, 32712), 13: (32613, 32713), 14: (32614, 32714), 15: (32615, 32715),
                 16: (32616, 32716), 17: (32617, 32717), 18: (32618, 32718),
                 19: (32619, 32719),
                 20: (32620, 32720), 21: (32621, 32721), 22: (32622, 32722), 23: (32623, 32723), 24: (32624, 32724),
                 25: (32625, 32725), 26: (32626, 32726), 27: (32627, 32727),
                 28: (32628, 32728),
                 29: (32629, 32729), 30: (32630, 32730), 31: (32631, 32731), 32: (32632, 32732), 33: (32633, 32733),
                 34: (32634, 32734), 35: (32635, 32735), 36: (32636, 32736),
                 37: (32637, 32737),
                 38: (32638, 32738), 39: (32639, 32739), 40: (32640, 32740), 41: (32641, 32741), 42: (32642, 32742),
                 43: (32643, 32743), 44: (32644, 32744), 45: (32645, 32745),
                 46: (32646, 32746),
                 47: (32647, 32747), 48: (32648, 32748), 49: (32649, 32749), 50: (32650, 32750), 51: (32651, 32751),
                 52: (32652, 32752), 53: (32653, 32753), 54: (32654, 32754),
                 55: (32655, 32755),
                 56: (32656, 32756), 57: (32657, 32757), 58: (32658, 32758), 59: (32659, 32759), 60: (32660, 32760)}

    while True:

        vector_extension_list = ('.shp', '.SHP')
        raster_extension_lsit = ('.tiff', '.TIFF', '.tif', '.TIF')

        utm_zone = raw_input('\nEnter UTM Zone number. Just the number ').strip("'").strip('"')

        while True:

            if utm_zone.isdigit():
                utm_zone = int(utm_zone)
                break
            else:
                utm_zone = raw_input('Enter UTM number, not string. ').strip("'").strip('"')

        while True:
            if 1 <= utm_zone < 61:
                break
            else:
                utm_zone = raw_input('Enter UTM number in range 0-60 ').strip("'").strip('"')

                while True:

                    if utm_zone.isdigit():
                        utm_zone = int(utm_zone)
                        break
                    else:
                        utm_zone = raw_input('Enter UTM number, not string. ').strip("'").strip('"')

        n_or_s = raw_input('\nEnter N or S ').strip('"').strip("'").lower()
        n_or_s_upper = n_or_s.upper()

        while True:

            if n_or_s == 'n' or n_or_s == 's':
                break
            else:
                n_or_s = raw_input('Enter N or S ').strip('"').strip("'").lower()

        if n_or_s == 'n':

            utm_code = utm_codes[utm_zone][0]
        else:
            utm_code = utm_codes[utm_zone][1]

        if reproject_input.endswith(vector_extension_list):

            print '\nReprojecting Vector...'

            out_file = os.path.join(os.path.dirname(reproject_input), 'Reprojected_{0}_{1}_'.format(utm_zone, n_or_s_upper) + os.path.basename(reproject_input))
            command1 = [ogr2ogr_location, out_file, '-t_srs', 'EPSG:{}'.format(utm_code), reproject_input]
            subprocess.check_call(command1)

            break

        elif reproject_input.endswith(raster_extension_lsit):
            print '\nReprojecting Raster'

            out_file = os.path.join(os.path.dirname(reproject_input), 'Reprojected_{0}{1}_'.format(utm_zone, n_or_s_upper) + os.path.basename(reproject_input))
            command1 = [gdal_warp_location, '-t_srs', 'EPSG:{}'.format(utm_code), reproject_input, out_file]
            subprocess.check_call(command1)
            break

        else:
            reproject_input = raw_input('You did not input a .shp file or .tif file, please input one ').strip('"').strip("'")

if what_to_do == '2':

    kml_input = raw_input('\nDrag in your .kml').strip('"').strip("'")
    print kml_input

    while True:

        if kml_input.endswith('kml') or kml_input.endswith('kmz'):

            out_file = os.path.join(os.path.dirname(kml_input), 'Shape_' + os.path.basename(os.path.splitext(kml_input)[0]))
            command1 = [ogr2ogr_location, '-f', 'ESRI Shapefile', '-skipfailures', out_file, kml_input]
            subprocess.check_call(command1)
            break


