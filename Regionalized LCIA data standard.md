# Technical standards for regionalized LCIA method data

This document follows the terminology used in ISO standards and RFC 2119: “shall” indicates a requirement for adherence to the standard, while “should” indicates a recommended but non-mandatory provision of the standard. The term “may” is used in cases where no recommendation is made in this standard.

This document does not require an exact format for regionalized LCIA metadata, but makes a strong recommendation for the datapackage metadata format.

## Regionalized CFs stored in raster files

Raster files shall be provided as GeoTIFF files. Other formats may be provided in addition, such as GeoPackage raster files.

In addition to the raster band specifying the characterization factors, characterization factor uncertainty information shall be provided at the same spatial scale, either as another raster file or as a separate band in the same file (in case detailed uncertainty information is not available and only a standard deviation or similar can be reported). Multiple uncertainty bands per characterization factor may be provided.

A raster file may include multiple bands for characterizing different elementary flows.
Coordinate Reference System

The raster file shall include a valid coordinate reference system in its metadata. Using WGS 84 is strongly encouraged but not required; it is preferable to maintain the native spatial scale of raster files if projection to WGS 84 would require interpolation.

### No data values

Note: This section may be revised in the future as software support for either writing and reading internal nodata masks in GeoTIFFs, or reading and writing GeoPackage raster files, improves.

The TIFF tag GDAL_NODATA shall be set. The “no data” value should be a negative number chosen not to overlap with any other existing characterization factor values. Both -1 and -9999 are good choices. Special care shall be taken to avoid overlaps between valid data and the “no data” value in cases where negative characterization factors are present. The “no data” value shall not be any of the following:

*	Zero. Zero should always be a valid characterization factor value, and should be specified as such in areas where the LCIA model indicates no impact due to elementary flows.
*	NaN. NaN values are not handled consistently across commonly used GIS programs.
*	-1.18 · 1038, -2.23 · 10308, or other large positive or negative values. Such values can be modified and therefore corrupted during format conversions.
Documentation file

In addition to the raster file, a text file describing the raster file shall also be provided. Such a text file shall include the following information:

*	A description of each raster band. Each band will be specific to one elementary flow, and the documentation file shall include all information necessary to uniquely identify each elementary flow in both (standard) the ecoinvent (version 3) and ILCD nomenclatures. If a band contains uncertainty information, the uncertainty information shall be described in detail, including a short description of how the information was obtained, and how it can be interpreted.
*	The unit for each raster band, such as points or kg CO2-eq.
*	A link on where to get more information on the LCIA method used to obtain the characterization factors.

## Regionalized CFs stored in vector files

Vector files shall be provided in the GeoPackage format.

In addition to the column specifying the characterization factors, characterization factor uncertainty information shall be provided at the same spatial scale, as separate columns in the same vector file.

All vector characterization factors with the same spatial scale should be provided in a single vector file. If technical limitations on the number of columns require splitting the impact category into multiple files, this shall be clearly explained in the documentation file.

### Coordinate Reference System

The vector file shall be provided with the coordinate reference system WGS 84. WGS 84 is not an equal area projection, and therefore projection will be necessary for calculations with require calculating the areas of spatial units.

### Documentation file

In addition to the vector file, a text file shall also be provided. Such a text file shall include the following information:

*	A description of each column. Each column will be specific to one elementary flow, and the documentation file shall include all information necessary to uniquely identify each elementary flow in both the ecoinvent (version 3) and ILCD nomenclatures. If a column contains uncertainty information, the uncertainty information shall be described in detail, including a short description of how the information was obtained, and how it can be interpreted.
*	A link on where to get more information on the LCIA method used to obtain the characterization factors.

### No data values

“No data” values shall not be used in vector files. The spatial scale shall be chosen such that there is a valid characterization factor in each spatial unit. It is perfectly fine to split an impact category into separate native spatial scales for each elementary flow.

### Validation

Before public release, the above requirements shall be validated manually in QGIS, and, if available, other common GIS software such as ArcGIS.
