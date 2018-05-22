print "Setting the working directory"
import os
work_dir = os.path.dirname(os.path.realpath(__file__)) # This method returns the directry path of this script.
os.chdir(work_dir)
print work_dir

if not os.path.isdir("../orig/"): # Create the output directory if it doesn't exist
    os.makedirs("../orig/")

if not os.path.isdir("../data/"): # Create the output directory if it doesn't exist
    os.makedirs("../data/")

if not os.path.isdir("../docs/"): # Create the output directory if it doesn't exist
    os.makedirs("../docs/")

### Define the main function ###
def main():
    try:
        satellite_years = [
            'F101992','F101993','F101994',
            'F121994','F121995','F121996','F121997','F121998','F121999',
            'F141997','F141998','F141999','F142000','F142001','F142002','F142003',
            'F152000','F152001','F152002','F152003','F152004','F152005','F152006','F152007',
            'F162004','F162005','F162006','F162007','F162008','F162009',
            'F182010','F182011','F182012','F182013'
            ]
        for satellite_year in satellite_years[-2:]:
            print "working on "+ satellite_year
            print "Set the version number"
            if satellite_year[0:3] == 'F18':
                version = ".v4c"
            else:
                version = ".v4b"
            print "Download the tar file"

            # Setting input and output
            filename = satellite_year + version + ".avg_lights_x_pct.tgz"
            url = "https://ngdc.noaa.gov/eog/data/web_data/v4avg_lights_x_pct/" + filename
            downloaded_tar = "../temp/" + filename
            # Process
            download_data(url, downloaded_tar)

            print "Extract all files" # Extracting only necessary files (the .extract() function) does not work. So we extract all and then delete those unnecessary.
            # Setting input and output
            input_tar = downloaded_tar
            tempdir = "../temp/"
            uncompress_tar(input_tar, tempdir)

            print "Save files that we need in the appropriate folders"
            # The pct data
            if satellite_year != 'F182011': # For this satellite-year, the pct_lights.tif is missing, confirmed by NOAA staff on 22 May 2018
                light_tif = satellite_year + version + ".pct_lights.tif"
                print light_tif
                os.rename(tempdir+light_tif, "../orig/"+light_tif)
            # Readme
            readme_txt = "README_avg_lights_x_pct.txt"
            if not os.path.isfile("../docs/"+readme_txt): # Only for the first loop
                os.rename(tempdir+readme_txt, "../docs/"+readme_txt)

            print "Delete the other files that we do not need"
            for file in os.listdir(tempdir):
                print file
                os.remove(tempdir+file)

        print "Deleting temp dir"
        os.rmdir(tempdir)

        print "All done."

    # Return any other type of error
    except:
        print "There is an error."

### Define the subfunctions ###
def download_data(url, output):
    print "...downloading and saving the file"
    import urllib
    urllib.urlretrieve(url, output)

def uncompress_tar(in_tar, outdir):
    print "...creating the output directory if it doesn't exist"
    if not os.path.isdir(outdir): # Create the output directory if it doesn't exist
        os.makedirs(outdir)
    print "...importing the tarfile module"
    import tarfile
    print "...creating a TarFile object"
    tar = tarfile.open(in_tar, "r:gz") ## create a TarFile Object, which allows us to use special functions for interacting with the tar file. The mode is "r:gz", which reads a gzip compression
    print "...extracting all files"
    tar.extractall(path = outdir)

### Execute the main function ###
if __name__ == "__main__":
    main()
