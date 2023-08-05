# fifa_preprocessing
This module provides methods conceived to preprocess data stored in a csv file etc., with the intent to perform data analysis and Machine Learning.

## Table of contents
* [General Info](#general-info)
* [Technologies](#technologies)
* [Data](#data)
* [Running](#running)
* [Functions](#functions)
* [Testing](#testing)
* [Status](#status)
* [Authors](#authors)
* [License](#license)


## General Info
It was originally created to preprocess data from the EA Sports' FIFA 19 for a Machine Learning project to predict players' wages by regression. Therefore it contains functions that can be universally used for data preprocessing but also functions that are made specifically with the FIFA 19 data set in mind.

## Technologies
It was written in Python 3.6 and requires 'pandas' to be installed in used environment. Also it requires 'matplotlib.pyplot' be installed if it is run as main.
Used libraries:
* math
* pandas

To install use:
```
$ import math
$ import pandas as pd
```
## Data
Data set used in this project is shared by Karan Gadiya on https://www.kaggle.com/karangadiya/fifa19 licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0
International License][cc-by-nc-sa].

## Running
If program is run directly it will return a graph. 

If being imported, it will display all possible functions.

## Functions
Already done functions:
* Loading data set from Fifa 19
* Removing goalkeepers from data
* Some data type converters

## Testing
To execute tests on the mudule's functions run:
```
$ python3 -m doctest -v preprocessing.py 
```

## Status
Project is curently in progress.

## Authors
Piotr Frątczak, Jakub Płudowski

## License
Shield: [![CC BY-NC-SA 4.0][cc-by-nc-sa-shield]][cc-by-nc-sa]

This work is licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0
International License][cc-by-nc-sa].

[![CC BY-NC-SA 4.0][cc-by-nc-sa-image]][cc-by-nc-sa]

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png
[cc-by-nc-sa-shield]: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg
