# Converts EXIF GPS data into a CSV that can be imported into a Google maps layer

# Based on https://developer.here.com/blog/getting-started-with-geocoding-exif-image-metadata-in-python3

# Modified for Huawei P30 Pro
# Tested on Windows 10 x64, Python 3.9.1 

from PIL import Image
from PIL.ExifTags import TAGS
from PIL.ExifTags import GPSTAGS
import pprint
import os
import csv

def get_exif(filename):
    image = Image.open(filename)
    image.verify()
    return image._getexif()

def get_geotagging(exif):
    if not exif:
        raise ValueError("No EXIF metadata found")

    geotagging = {}
    for (idx, tag) in TAGS.items():
        if tag == 'GPSInfo':
            if idx not in exif:
                raise ValueError("No EXIF geotagging found")

            for (key, val) in GPSTAGS.items():
                if key in exif[idx]:
                    geotagging[val] = exif[idx][key]

    return geotagging

def get_labeled_exif(exif):
    labeled = {}
    for (key, val) in exif.items():
        labeled[TAGS.get(key)] = val

    return labeled

def get_decimal_from_dms(dms, ref):

    degrees = dms[0]
    minutes = dms[1] / 60.0
    seconds = dms[2] / 3600.0

    if ref in ['S', 'W']:
        degrees = -degrees
        minutes = -minutes
        seconds = -seconds

    return round(degrees + minutes + seconds, 5)

def get_coordinates(geotags):
    lat = get_decimal_from_dms(geotags['GPSLatitude'], geotags['GPSLatitudeRef'])

    lon = get_decimal_from_dms(geotags['GPSLongitude'], geotags['GPSLongitudeRef'])

    return (lat,lon)

pp = pprint.PrettyPrinter(indent=4)

# exif = get_exif('IMG_20191105_200411_1.jpg')
# labeled = get_labeled_exif(exif)
# pp.pprint(labeled)

# geotags = get_geotagging(exif)
# pp.pprint(geotags)

# geotags = get_geotagging(exif)
# pp.pprint(get_coordinates(geotags))

def extractCoordinatesFromImagesToCSV(image_path, csv_filename):

    with open(csv_filename, 'w', newline='') as csvfile:
        my_writer = csv.writer(csvfile, delimiter=',')

        my_writer.writerow(['filename','latitude','longitude'])
    
        directory = image_path

        for entry in os.scandir(directory):
            if (entry.path.endswith(".jpg") and entry.is_file()):
                filename = entry.path

                try:

                    exif = get_exif(filename)
                    geotags = get_geotagging(exif)
                    ll = get_coordinates(geotags)

                    filename_short = filename.split('\\')[-1]

                    my_writer.writerow([filename_short,ll[0],ll[1]])

                except:
                    print("Error for file: "+filename)

#extractCoordinatesFromImagesToCSV(r'C:\Users\tester\Downloads\Neuseeland 2019', 'new_zealand_coords.csv')
#extractCoordinatesFromImagesToCSV(r'C:\Users\tester\Downloads\Singapur 2019', 'singapore_coords.csv')