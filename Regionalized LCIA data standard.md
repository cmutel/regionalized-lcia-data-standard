# Technical standards for regionalized LCIA method data interchange

*Version: 0.draft-1*

## Motivation

There is currently no standardized data format for the exchange of regionalized life cycle impact assessment (LCIA) methods. This lack of standardization results in inconsistent implementation of LCIA methods and poor uptake of regionalization in general. This document provides a specification for a software- and database-independent data format for regionalized and site-generic LCIA methods. Its guiding principles are:

* Simplicity. Use the simplest and easiest approach and format whenever possible.
* Compatibility and consistency. This standard requires elementary flows be identified in both of the major nomenclature systems (ELCD and ecoinvent), making for easier implementation.
* Reuse of existing standards. This standard builds on top of existing widely-used standards for metadata ([datapackage](https://frictionlessdata.io/specs/data-package/)), [CSVs](https://tools.ietf.org/html/rfc4180), and GIS data ([geojson](http://geojson.org/), [GeoTIFF](https://en.wikipedia.org/wiki/GeoTIFF)).

## Summary

An LCIA method is a directory with a set of files:


  * `datapackage.json`: Describes the LCIA method
  * `<named vector file>.geojson`: Spatial scale of a vectorized (i.e. polygons, lines, or points) impact category
  * `<named data file>.csv`: Characterization factors (CFs) for `<named vector file>.geojson`.
  * `<named raster file>.tiff`: Spatial scale *and* CFs for a rasterized impact category.

The directory is zipped for data exchange.

Following this data format gives method developers several advantages:

* Software independence: This format is based on existing data science formats for exchanging data, and are software-neutral.
* Consistent implementation. Elementary flows in at least one of, and probably both ecoinvent and ELCD nomenclatures, are explicitly provided.
* Consistent coordinate reference systems (CRS). The CRS for vector datasets is required to be [WGS84](https://en.wikipedia.org/wiki/World_Geodetic_System) (i.e. latitude/longitude pairs), and the CRS for raster datasets is required to include a link to [spatialreference.org](http://spatialreference.org/), allowing for retrieval of CRS information in multiple formats.
* Consistent "no-data" value storage and retrieval. Guidelines are given on how to choose a good no-data value, and problematic values are avoided.
* Data integrity checks.
* Explicit versioning.

This data standard is designed for data *exchange* and *archiving*; use in LCA or other software will probably be more efficient when data is transformed to another format that includes spatial indices.

## Terminology

This document follows the terminology used in ISO standards and [RFC 2119](https://www.ietf.org/rfc/rfc2119.txt): “shall” indicates a **requirement** for adherence to the standard, while “should” indicates a recommended but non-mandatory provision of the standard. The term “may” is used in cases where no recommendation is made in this standard.

## Nomenclature

### Uncertainty

Uncertainty distributions **shall** be specified following the schema developed in the [UncertWeb](https://www.sciencedirect.com/science/article/pii/S1364815212000564) project. See the [UncertWeb dictionary](https://wiki.aston.ac.uk/foswiki/bin/view/UncertWeb/UncertMLDictionary) reference for UncertWeb terms. Here are some common uncertainty measures and distributions:

#### Normal distribution

* Name: "Normal"
* Fields: "mean", "variance"

### Units

This version of the standard does not include any requirements on how units are to be defined; instead, we wait until there is a clear decision for the [data package standard](https://github.com/frictionlessdata/specs/issues/216).

Characterization factors should be given in the unit of the matching elementary flow whenever possible.

## Folder structure

A regionalized LCIA method **shall** be distributed as a zipped directory in a single file. Individual impact categories can also distributed independently, again as zipped directories. It is up to the LCIA method developers to ensure metadata consistency if separate distribution is allowed.

This directory **shall** include a metadata file (`datapackage.json`), and at least one raster or vector data file.

## `datapackage.json`

The `datapackage.json` file should follow the [datapackage standard](https://frictionlessdata.io/data-packages/), and should have the following structure:

::

    {
      "profile": "data-package",
      "name" : "<a-unique-human-readable-and-url-usable-identifier>",
      "version": "<version number; recommended to use integers starting from 1>",
      "licenses": [{
        "name": "<short license identifier>",
        "path": "<URL of license text>",
        "title": "<full name of license>"
      }],
      "description": "<description of LCIA method; can include Markdown formatting>",
      "homepage": "<optional link to webpage for LCIA method>",
      "title" : "<a nice title>",
      "sources": [{
        "title": "<name of data source>",
        "path": "<URL of data source>"
      }],
      "contributors": [{
        "title": "<someone>",
        "email": "<some email>",
        "path": "<some URL>",
        "role": "<e.g. author>"
      }],
      "created": "<A datetime following RFC3339, e.g 1985-04-12T23:20:50.52Z>",
      "resources": [<list of resources, see below>]
    }

See the [data package](https://frictionlessdata.io/specs/data-package/) specification for notes and guidance on each of these properties.

This specification uses "`<>`" to indicate fields that **shall** be replaced by the method developers; fields without "`<>`" should be provided exactly as specified.

In this standard, the properties "profile", "name", "version", "licenses", and "description" are required. All other properties listed above are optional; additional properties may also be added.

If it is more appropriate, the "sources" and "contributors" properties can be specified per resource.

## Resources

### Common resource properties

A resource covers characterization factors with five common characteristics: the same spatial scale, the same uncertainty distribution, the same impact category, the same weighting, and the same normalization. It is also worth noting what does not have to be the same - there can be multiple elementary flows in one resource, or multiple archetypes for a single elementary flow. As such, the common properties of a `resource` look like this:

::

  {
    "distribution": "<name of an uncertainty distribution from UncertWeb specification; see uncertainty section>",
    "amount-field": "<name of field that best describes the amount field, i.e. mean, median, mode, or unknown>",
    "impact-category": ["<list of categories>", "<to whatever depth is necessary>"],
    "flows": [{
        "name": "<short name of elementary flow; must be unique>",
        "ecoinvent": [{
          "name": "<name of elementary flow in ecoinvent reference list>",
          "id": "<id of elementary flow in ecoinvent reference list>",
          "archetypes": [["<list of archetypes>"], ["<can have>", "<multiple archetypes>"]],
          "unit": "<name of elementary flow unit in ecoinvent reference list>"
        }],
        'ELCD': [{
          "name": "<name of elementary flow in ELCD reference list>",
          "id": "<id of elementary flow in ELCD reference list>",
          "archetypes": [["<list of archetypes>"], ["<can have>", "<multiple archetypes>"]],
          "unit": "<name of elementary flow unit in ELCD reference list>"
        }]
      }]
  }

### Elementary flows

### Vector spatial scales

Characterization factor data with vector spatial scales are given as a [tabular data resource](http://frictionlessdata.io/specs/tabular-data-resource/), with additional elements from the [spatial data package](https://research.okfn.org/spatial-data-package-investigation/), as recommended by the spatial data package preliminary investigation.

This standrad is more restrictive than the tabular data resource, in that CSV files **shall** follow the [standard dialect](http://paulfitz.github.io/dataprotocols/tabular-data-package/index.html#csv-files); custom dialects are not allowed.

::

  {
    "profile": "tabular-data-resource",
    "path": ["<csv filename>.csv"],
    "name": "<appropriate name>",
    "description": "<description of impact (sub)category; can include Markdown formatting>",
    "hash": "<MD5 hash of CSV file",
    "locations": [{
        "type": "boundary-id",
        "geojson-path": "<geojson filename>.geojson",
        "field": "feature",
        "version": "<optional version identifier for geojson source data>",
        "url": "<optional link to webpage for geojson source data>",
        "hash": "<MD5 hash of geojson file"
    }],
    "schema": {
      "fields": [
        {
          "name": "feature",
          "type": "string",
        },
      ],
      "primaryKey": "feature"
    }
  }

Vector files **shall** be provided in the GeoJSON format, and follow the GeoJSON specification. GeoJSON files may be compressed.

The GeoJSON specification requires that the [WGS 84](https://en.wikipedia.org/wiki/World_Geodetic_System#A_new_World_Geodetic_System:_WGS_84) CRS be used. WGS 84 is not an equal area projection, and should not be used to calculate the areas of spatial units.

“No data” values should not be used in vector files. The spatial scale shall be chosen such that there is a valid characterization factor in each spatial unit. It is perfectly fine to split an impact category into separate native spatial scales for sets of elementary flows.

### Raster spatial scales

Raster files **shall** be provided as [GeoTIFF](https://en.wikipedia.org/wiki/GeoTIFF) files.

The raster file **shall** include a valid coordinate reference system in its metadata. The spatial scale and coordinate reference system *should* be the same as the most representative model outputs and *should* be provided without interpolation if possible.

In addition to the raster band specifying the CF value, CF uncertainty information **shall** be provided as separate band(s) in the same file. Multiple uncertainty bands per CF may be provided, if needed to complete describe an uncertainty distribution; for example, the triangular distribution requires a minimum, mode, and maximum.

A raster file **shall** only include CFs for multiple elementary flows if the same values apply to all flows. For example, "Occupation, permanent crop, irrigated, extensive" and "Occupation, permanent crop, irrigated, intensive" may have the same CF values for a given LCIA method.

GeoTIFFs should be prepared to [optimize use in the cloud](http://www.cogeo.org/), i.e. the following GDAL options should be used ([more info](http://www.cogeo.org/providers-guide.html)): `-co TILED=YES -co COPY_SRC_OVERVIEWS=YES -co COMPRESS=DEFLATE`.

The GeoTIFF tag [GDAL_NODATA](https://www.awaresystems.be/imaging/tiff/tifftags/gdal_nodata.html) **shall** be set. [Internal nodata masks](http://www.gdal.org/frmt_gtiff.html) may be included.

### Site-generic characterization factors

In addition to the raster file, a text file describing the raster file shall also be provided. Such a text file shall include the following information:



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
          "primaryKey": [
            "district-name"
          ]
        }
      ]
    }

*   A description of each raster band. Each band will be specific to one elementary flow, and the documentation file shall include all information necessary to uniquely identify each elementary flow in both (standard) the ecoinvent (version 3.4) and ELCD (version 3.2) nomenclatures. If a band contains uncertainty information, the uncertainty information shall be described in detail, including a short description of how the information was obtained, and how it can be interpreted.
*   The unit for each raster band, such as points or kg CO2-eq.
*   A link on where to get more information on the LCIA method used to obtain the characterization factors.

## No-data values

The “no data” value should be a negative number chosen not to overlap with any other existing characterization factor values. Both -1 and -9999 are good choices. The no data value **shall** not overlap any valid data in cases where negative characterization factors are present.

The “no data” value **shall** not be any of the following:

*	Zero. Zero should always be a valid characterization factor value, and should be specified as such in areas where the LCIA model indicates no impact for a given elementary flow.
*	Not-a-Number (NaN). NaN values are not handled consistently across commonly used GIS programs.
*	-1.18 · 10^38, -2.23 · 10^308, or other very large positive or negative values. Such values can be modified and therefore corrupted during format conversions.

## Validation

Before public release, the above requirements **shall** be validated manually in [QGIS](https://www.qgis.org/en/site/), and, if available, other GIS software such as ArcGIS.

## Normalization and weighting

This version of the standard does not support providing separate normalization or weighting values.
