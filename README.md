This repository downloads DMSP-OLS data for all satellite-years available and makes them ready for use in ArcGIS.

It also deblurrs the original data with the methodology proposed by [Abrahams, Oram, and Lozano-Garcia (2018)](http://doi.org/10.1016/J.RSE.2018.03.018).

Prerequisites

ArcGIS 10 (which comes with Python 2.7)

Matlab R2016b or higher

Matlab Image Processing Toolbox

Matlab Mapping Toolbox

Matlab Statistics and Machine Learning Toolbox

Note: The pct_lights data for F182011 is missing (confirmed by NOAA staff on 22 May, 2018). As the deblurring process requires the pct_lights data, the year 2011 nighttime light data cannot be deblurred at this moment.
