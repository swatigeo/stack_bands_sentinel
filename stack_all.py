'''to stack all the images in TIFF or IMG format'''
import os, fnmatch,sys,subprocess,time
from time import time
from osgeo import gdal,ogr
from array import array		
import gdal
import rasterio
import rasterio.env
import subprocess
fformat='*.jp2'

working_dir='...\\...\\...\\In'
output_dir='...\\...\\...\\op'


def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
                break
    return result

raster_list =find(fformat, working_dir)

# generating output in default *.jp2 format
for r in raster_list:
    data=os.path.dirname(r) #take full path without filename
   
    y=r[:-6]
    
    file_list=[(y+'02.jp2'),(y+'03.jp2'),(y+'04.jp2'),(y+'08.jp2')]   
    with rasterio.open(os.path.join(data,file_list[0])) as src0:
        print(file_list[0])
        meta = src0.meta
    meta.update(count = len(file_list))
    y1=os.path.basename(r)
    y1=y1[:-8]
    y1_o=os.path.join(output_dir,y1+".jp2")
    #with rasterio.Env():
    with rasterio.open(y1_o, 'w',**meta) as dst:

        for id, layer in enumerate(file_list, start=1):
            
            with rasterio.open(layer) as src1:
                c=dst.write_band(id, src1.read(1))
                
 #for generating output in TIFF        
    tempcmd='gdal_translate -of GTiff -ot UInt16'+" " +y1_o+" "+ os.path.join(output_dir,y1+".tif")
    subprocess.call(tempcmd,shell=True) #call command in cmd 
    
   
# for creating output in img format and cmd for generating pyramid layers

    tempcmd='gdal_translate  -of HFA -ot UInt16'+" " +y1_o+" "+ os.path.join(output_dir,y1+".img")
    subprocess.call(tempcmd,shell=True)
    
    cmd='gdaladdo -r '+'average'+' -b 1 -b 2 -b 3 '+os.path.join(output_dir,y1+".img")+' --config HFA_USE_RRD YES  2 4 8 16 32 64 128 256'   
    subprocess.call(cmd,shell=True)#call command in cm
    
    

report_file=os.path.join(output_dir,'report.txt')
e=open(report_file,'w')
e.write("required files are generated")
errorflag=0
i=0                
"""                
                
          
