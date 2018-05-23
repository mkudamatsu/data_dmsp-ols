# Takes 168 seconds

print "Setting the working directory"
import os
work_dir = os.path.dirname(os.path.realpath(__file__)) # This method returns the directry path of this script.
os.chdir(work_dir)

print "Launching ArcGIS"
import arcpy

print "Enabling the Spatial Analyst extension"
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")

print "Setting the environment"
arcpy.env.overwriteOutput = True # Allow the overwriting of the output files
arcpy.env.workspace = "../b_temp/b_temp.gdb" # NEVER USE single backslash (\). # Set the working directory.

if not os.path.isdir("../temp/"): # Create the output directory if it doesn't exist
    os.makedirs("../temp/")

### Define the main function ###
def main():
  try:
    # Input 1: Azerbaijan's extent
    input_extent = "44 37 52 43" # Min longitude, Min latitude, Max longitude, Max latitude
    # Input 2: Nighttime light raster datasets
    satellite_years = [
        'F101992','F101993','F101994',
        'F121994','F121995','F121996','F121997','F121998','F121999',
        'F141997','F141998','F141999','F142000','F142001','F142002','F142003',
        'F152000','F152001','F152002','F152003','F152004','F152005','F152006','F152007',
        'F162004','F162005','F162006','F162007','F162008','F162009',
        'F182010','F182011','F182012','F182013'
        ]
    for satellite_year in satellite_years:

        print "Working on satellite-year " + satellite_year

        print "...Set the version number for stable_lights data"
        if satellite_year == "F182010":
            version = ".v4d"
        elif satellite_year[0:3] == 'F18':
            version = ".v4c"
        else:
            version = ".v4b"

        print "...Clipping stable_lights raster for " + satellite_year
        input_raster = "../orig/" + satellite_year + version + "_web.stable_lights.avg_vis.tif"
        output_raster = "../data/" + satellite_year + "_stable_lights_aze.tif"
        clip_raster(in_raster = input_raster, clipping_extent = input_extent, out_raster = output_raster)

        print "...Set the version number for pct_lights data"
        if satellite_year[0:3] == 'F18':
            version = ".v4c"
        else:
            version = ".v4b"

        print "...Clipping pct_lights raster for " + satellite_year
        if satellite_year == 'F182011':
            print "...We skip " + satellite_year + "because the pct_lights.tif is currently not available."
        else:
            input_raster = "../orig/" + satellite_year + version + ".pct_lights.tif"
            output_raster = "../temp/" + satellite_year + "_pct_lights_aze.tif"
            clip_raster(in_raster = input_raster, clipping_extent = input_extent, out_raster = output_raster)

    print "All done."

  # Return geoprocessing specific errors
  except arcpy.ExecuteError:
    print arcpy.GetMessages()
  # Return any other type of error
  except:
    print "There is non-geoprocessing error."
  # Check in extensions
  finally:
    arcpy.CheckInExtension("spatial")

# subfunctions
def clip_raster(in_raster, clipping_extent, out_raster):
  print "...Deleting the output if it exists"
  delete_if_exists(out_raster)

  print "...Clipping the raster"
  arcpy.Clip_management(in_raster, clipping_extent, out_raster) # http://desktop.arcgis.com/en/arcmap/10.3/tools/data-management-toolbox/clip.htm

def delete_if_exists(file):
  if arcpy.Exists(file):
    arcpy.Delete_management(file)


### Execute the main function ###
if __name__ == "__main__":
    main()
