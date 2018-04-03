# Technical standards for regionalized LCIA method data interchange

*Version: 0.draft1*

## Motivation

There is currently no standardized data format for the exchange of regionalized life cycle impact assessment (LCIA) methods. This lack of standardization results in inconsistent implementation of LCIA methods and poor uptake of regionalization in general. This document provides a specification for a software- and database-independent data format for regionalized and site-generic LCIA methods. Its guiding principles are:

* Compatibility and consistency. This standard requires elementary flows be identified in both of the major nomenclature systems (ILCD and ecoinvent), making for easier implementation.
* Reuse of existing standards. This standard builds on top of existing widely-used standards for metadata ([datapackage](https://frictionlessdata.io/specs/data-package/)), [CSVs](https://tools.ietf.org/html/rfc4180), and GIS data ([geojson](http://geojson.org/), [GeoTIFF](https://en.wikipedia.org/wiki/GeoTIFF)).

## Summary

An LCIA method is a directory with a single file that describes the method (the metadata file `datapackage.json`) and at least one data file which gives characterization factors. Characterization factors (CFs) and their associated uncertainty distributions are provided as text in comma-separated value (CSV) files. Regionalized CFs are also provided in CSV files, while the spatial scale of a regionalized LCIA method is given in a separate file. The only exception to this pattern is for rasters, which due to technical reasons combine CFs and spatial support in a single file.

This data standard is designed for data exchange and archiving; use in LCA or other software will be most efficient when data is transformed to another format.

## Terminology

This document follows the terminology used in ISO standards and [RFC 2119](https://www.ietf.org/rfc/rfc2119.txt): “shall” indicates a **requirement** for adherence to the standard, while “should” indicates a recommended but non-mandatory provision of the standard. The term “may” is used in cases where no recommendation is made in this standard.

## Nomenclature

### Uncertainty

Uncertainty distributions **shall** be specified following the schema developed in the [UncertWeb](https://www.sciencedirect.com/science/article/pii/S1364815212000564) project. See the [todo] reference for UncertWeb terms.

### Units

This is less clear; see https://github.com/frictionlessdata/specs/issues/216.

## Folder structure

A regionalized LCIA method **shall** be distributed as a zipped directory in a single file. This directory **shall** include a metadata file (`datapackage.json`), and at least one raster or vector data file.

## Metadata file: `datapackage.json`

The `datapackage.json` file should follow the [datapackage standard](https://frictionlessdata.io/data-packages/), and should have the following structure:

::

    {
      "profile": "data-package",
      "name": "appropriate name for this collection of CF maps",
      "version": "version number; recommended to use integers starting from 1",
      "license": "license identifier from https://spdx.org/licenses/",
      "resources": [
        {
          "path": "filepath for vector file; should be in the same directory as this file",
          "name": "internal name for this set of CFs",
          "format": "geojson",
          "mediatype": "application/json"
          "spatial-profile": "vector",
          "schema": {
            "fields": [
              {
                "name": "name of field; must be unique",
                "description": "description of field",
              }
            ]
          },
        },
        {
          "path": "tourism_districts.geojson",
          "name": "tourism_districts",
          "profile": "data-resource",
          "locations": {
            "type": "geojson"
          },
          "schema": {
            "fields": [
              {
                "name": "district-name",
                "type": "string",
                "format": "default",
                "constraints": {
                  "required": true,
                  "unique": true
                }
              }
            ]
          },
          "primaryKeys": [
            "district-name"
          ]
        }
      ]
    }



In addition to the raster file, a text file describing the raster file shall also be provided. Such a text file shall include the following information:

*   A description of each raster band. Each band will be specific to one elementary flow, and the documentation file shall include all information necessary to uniquely identify each elementary flow in both (standard) the ecoinvent (version 3) and ILCD nomenclatures. If a band contains uncertainty information, the uncertainty information shall be described in detail, including a short description of how the information was obtained, and how it can be interpreted.
*   The unit for each raster band, such as points or kg CO2-eq.
*   A link on where to get more information on the LCIA method used to obtain the characterization factors.

## Regionalized CFs stored in raster files

Raster files **shall** be provided as [GeoTIFF](https://en.wikipedia.org/wiki/GeoTIFF) files. Other formats may be provided in addition, such as [GeoPackage](http://www.geopackage.org/) raster files.

In addition to the raster band specifying the characterization factors, characterization factor uncertainty information **shall** be provided at the same spatial scale, either as another raster file or as a separate band in the same file. Multiple uncertainty bands per characterization factor may be provided, if needed to complete describe an uncertainty distribution; for example, the triangular distribution requires a minimum, mode, and maximum.

A raster file may include characterization factors for multiple elementary flows.

### Coordinate Reference System

The raster file **shall** include a valid coordinate reference system in its metadata. The spatial scale and coordinate reference system should be the same as the most representative model outputs and should be provided without interpolation, if possible.

### No data values

The TIFF tag [GDAL_NODATA](https://www.awaresystems.be/imaging/tiff/tifftags/gdal_nodata.html) **shall** be set. [Internal nodata masks](http://www.gdal.org/frmt_gtiff.html) may be included. The “no data” value should be a negative number chosen not to overlap with any other existing characterization factor values. Both -1 and -9999 are good choices. The no data value **shall** not overlap any valid data in cases where negative characterization factors are present.

The “no data” value **shall** not be any of the following:

*	Zero. Zero should always be a valid characterization factor value, and should be specified as such in areas where the LCIA model indicates no impact for a given elementary flow.
*	Not-a-Number (NaN). NaN values are not handled consistently across commonly used GIS programs.
*	-1.18 · 10^38, -2.23 · 10^308, or other very large positive or negative values. Such values can be modified and therefore corrupted during format conversions.

## Regionalized CFs stored in vector files

Vector files **shall** be provided in the GeoJSON format. GeoJSON files may be compressed. Other formats may be provided in addition, such as [GeoPackage](http://www.geopackage.org/) raster files.

In addition to the field specifying the characterization factors, characterization factor uncertainty information **shall** be provided at the same spatial scale, as separate columns in the same vector file.

All vector characterization factors with the same spatial scale should be provided in a single vector file. If technical limitations on the number of columns require splitting the impact category into multiple files, this shall be clearly explained in the metadata file.

### Coordinate Reference System

The vector file shall be provided with the coordinate reference system [WGS 84](https://en.wikipedia.org/wiki/World_Geodetic_System#A_new_World_Geodetic_System:_WGS_84). WGS 84 is not an equal area projection, and should not be used to calculate the areas of spatial units.

### No data values

“No data” values shall not be used in vector files. The spatial scale shall be chosen such that there is a valid characterization factor in each spatial unit. It is perfectly fine to split an impact category into separate native spatial scales for sets of elementary flows.

## Validation

Before public release, the above requirements shall be validated manually in QGIS, and, if available, other common GIS software such as ArcGIS.
