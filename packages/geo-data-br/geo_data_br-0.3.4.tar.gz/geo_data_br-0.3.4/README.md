# Geo-localized data in Brazil

Python lib for easily dealing with Geo-localized Data in Brazil

We have implemented more than 200 dimensions of geolocalized data from www.atlasbrasil.org.br

It contains a detailed set of demographic information such as gender, age, income, education, inequality and many other interesting things.

# Installation

## Installing the `geo_data_br` lib

First install [geopandas](http://geopandas.org/install.html) using conda:

    conda install geopandas

Then,

    pip3 install geo_data_br

# Features

## Getting data from list of points

Given a list of latitude and longitude points we can use the lib to retrieve the corresponding data.

    import geo_data_br.points
    points_of_interest = [(-59.23352, -3.35030), (-60.17875, -3.27442)]
    demographics_on_poi = geo_data_br.points.data_on_points(points_of_interest)
    demographics_on_poi.gini
    >>> 0    0.59
    >>> 1    0.51
    >>> Name: gini, dtype: float64

    demographics_on_poi.espvida
    >>> 0    72.91
    >>> 1    68.70
    >>> Name: espvida, dtype: float64


# Contributing
