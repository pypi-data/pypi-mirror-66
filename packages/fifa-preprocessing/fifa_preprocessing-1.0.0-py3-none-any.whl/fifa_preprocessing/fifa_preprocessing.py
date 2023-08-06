#!/usr/bin/python
# -*- coding: utf-8 -*-
"""This module provides methods conceived to preprocess data stored
in a csv file etc., with the intent to perform data analysis and
Machine Learning.

It was originally created to preprocess data from the EA Sports'
FIFA 19 for a Machine Learning project to predictplayers' wages
by regression. Therefore it contains functions that can be
universally used for data preprocessing but also functions that
are made specifically with the FIFA 19 data set in mind.

This module requires that `pandas` be installed within the Python
environment this module is being run in.

Functions
---------
exclude_goalkeepers(data_frame)
    Delete goalkeepers from the data.
money_format(money)
    Return integer value of the monetary amount.
rating_format(rating)
    Express rating string as an integer.
work_format(work)
    Code amplitude string as an integer.
to_int(not_int)
    Floor floating point numbers.
apply_format(data_frame, column_names, format_method)
    Apply `format_method` to `data_frame` columns.
to_dummy(data_frame, column_names)
    Dummy code categorical variables.
split_work_rate(data_frame)
    Split the players' work rate column.
preprocess(source_file)
    Preprocess the FIFA 19 data from the path by default.
"""
import math
import pandas as pd


def exclude_goalkeepers(data_frame):
    """Remove goalkeepers and return the DataFrame.

    Go through the `data_frame` find all the tuples with the players'
    Position column set to "GK" and remove them. Return the `data_frame`
    with no goalkeeper tuples.

    Parameters
    ----------
    data_frame : pandas.DataFrame
        DataFrame containing FIFA19 data set including goalkeepers.

    Returns
    -------
    data_frame : pandas.DataFrame
        DataFrame containing FIFA19 data set with goalkeepers' tuples
        removed.

    Notes
    -----
    This function can be used when preprocessing the FIFA19 dataset to
    perform Machine Learning as a goalkeeper is a peculiar player  and
    all his properties vary compared to other positions on the field.
    
    Examples
    --------
    >>> data = pd.read_csv("data.csv")
    >>> print(data[['Name', 'Position']][0:5]) #print first few rows
                    Name Position
    0           L. Messi       RF
    1  Cristiano Ronaldo       ST
    2          Neymar Jr       LW
    3             De Gea       GK
    4       K. De Bruyne      RCM
    >>> data = exclude_goalkeepers(data)
    >>> print(data[['Name', 'Position']][0:5]) #print the same number of rows
                    Name Position
    0           L. Messi       RF
    1  Cristiano Ronaldo       ST
    2          Neymar Jr       LW
    4       K. De Bruyne      RCM
    5          E. Hazard       LF
    """
    goalkeepers = data_frame[data_frame['Position'] == 'GK']
    data_frame.drop(goalkeepers.index, inplace=True)
    return data_frame


def money_format(money):
    """Return the integer value of a monetary amount string.
    
    Remove euro currency sign from `money` and letters expressing the
    order of magnitude from the passed in string, e.g. "K" for thousands
    and "M" for milions. Cast the string into an integer. Returned values
    are expressed in thousands of euros.

    Parameters
    ----------
    money : str
        String containing monetary amount with a currency sign and
        order of magnitude abbreviation.
    
    Returns
    -------
    money : int
        Integer value of the monetary amount.

    Examples
    --------
    >>> v = money_format("€500K")
    >>> print(v)
    500

    >>> v = money_format("€70.5M")
    >>> print(v)
    70500
    """
    money = money.replace('€', '')
    if 'M' in money:
        money = money.replace('M', '')
        return int(float(money)*1000)
    money = money.replace('K', '')
    return int(money)

    
def rating_format(rating):
    """Return an integer equal to the string represented sum.

    Cast a string expressing a sum of integers delimited by a plus sign,
    e.g. 81+3, into an integer equal to a sum of the two numbers and
    return the integer.

    Parameters
    ----------
    rating : str
        String representing a sum of two integers with a plus sign
        inbetween.

    Returns
    -------
    rating : int
        Integer value of the sum of the numbers. Integer is equal to zero
        if the type of the input is not string.

    Notes
    -----
    This function is used in the FIFA19 data set to convert the player's
    special rating format in the game to an integer to get the proper
    understanding of the data when performing Machine Learning.

    Examples
    --------
    >>> r = rating_format("81+3")
    >>> print(r)
    84
    """
    if type(rating) is not str:
        return 0
    elif '+' in rating:
        plus = rating.index('+')
        base = int(rating[:plus])
        add = int(rating[plus + 1:])
        return base + add
    else:
        return int(rating)


def work_format(work):
    """Return a numerical interpretation of a categorical variable.

    Take in a string representing a categorical variable representing
    an amplitude of a phenomenon as "High", "Medium" and any other word,
    e.g. "Low", and return an integer representing the amplitude: 2, 1, 0
    respectively.
    
    Parameters
    ----------
    work : str
        String representing a categorical variable.

    Returns
    -------
    int
        Integer value of the work rate: 0, 1 or 2.

    Notes
    -----
    This function is used on the FIFA19 data set to convert the description
    of player's work rate ("High", "Medium" and "Low") into an integer in
    order to enable some of the Machine Learning algorithms to make use of
    the properties.

    Examples
    --------
    >>> w = work_format("High")
    >>> print(w)
    2

    >>> w = work_format("Low")
    >>> print(w)
    0

    >>> w = work_format("Poor")
    >>> print(w)
    0
    """
    if work == 'High':
        return 2
    elif work == 'Medium':
        return 1
    else:
        return 0


def to_int(not_int):
    """Return the integer value of a floating point number.
    
    Return the floored integer value of a floating point number. Return
    0 if `not_int` is a NaN.
    
    Parameters
    ----------
    not_int : not_integer
        Not_integer means all those types -- float, NaN -- to be converted
        into an integer.

    Returns
    -------
    int
	Integer value of the parameter.

    See Also
    --------
    numpy.nan : Nan stands for not a number.
    
    Examples
    --------
    >>> n = to_int(17.5)
    >>> print(n)
    17

    >>> import numpy
    >>> n = to_int(numpy.nan)
    >>> print(n)
    0
    """
    if math.isnan(not_int):
        return 0
    else:
        return int(not_int)


def apply_format(data_frame, column_names, format_method):
    """Apply a formatting function to a DataFrame column and return.

    Simplify applying format modifications to the data stored in columns
    of `data_frame`. Check if the parameters are of the right type, apply
    `format_method` to the columns of `data_frame` whose labels are passed
    in `column names`. Return the DataFrame with the applied changes.

    Parameters
    ----------
    data_frame : pandas.DataFrame
        DataFrame containing the data to be modified.
    column_names : list
        List of string labels of columns in `data_frame` to be modified.
    format_method : function
        Function to be applied to the columns of `data_frame`, whose labels
        are listed in `column_names`.

    Returns
    -------
    data_frame : pandas.DataFrame
        The passed in DataFrame with the formatting changes applied to
        its columns.

    See Also
    --------
    pandas.apply

    Examples
    --------
    >>> data = pd.read_csv("data.csv")
    >>> print(data[['Wage']][0:3]) #print first few lines
        Wage
    0  €565K
    1  €405K
    2  €290K
    >>> data = apply_format(data, ['Wage'], money_format)
    >>> print(data[['Wage']][0:3])
       Wage
    0   565
    1   405
    2   290
    """
    for column in column_names:
        if isinstance(column, str) and (column in data_frame) and callable(format_method):
            data_frame[column] = data_frame[column].apply(format_method)
    return data_frame


def to_dummy(data_frame, column_names):
    """Return the DataFrame with dummy coded categorical variables.

    Add dummy coded categorical variables columns of `data_frame`. Remove
    the categorical variable columns. Return the modified DataFrame.
    
    Parameters
    ----------
    data_frame : pandas.DataFrame
        DataFrame containing the data to be dummy coded.
    column_names : list
        List of string labels of columns in `data_frame` to be dummy coded.
    
    Returns
    -------
    data_frame : pandas.DataFrame
        The passed in DataFrame with the dummy coded categorical variables.

    See Also
    --------
    pandas.get_dummies, pandas.concat

    Notes
    -----
    Thanks to dummy coding, statistical analysis may be performed on
    categorical data.

    [1] "Dummy coding refers to the process of coding a categorical
    variable into dichotomous variables. For example, we may have data
    about participants' religion, with each participant coded as follows:

        A categorical or nominal variable with three categories

                        ==========      =======
                        Religion	Code
                        ==========      =======
                        Christian	1
                        Muslim		2
                        Atheist		3
                        ==========      =======

    This is a nominal variable (see level of measurement) which would be
    inappropriate as a predictor in MLR. However, this variable could be
    represented using a series of three dichotomous variables (coded as
    0 or 1), as follows:

        Full dummy coding for a categorical variable with three categories"

                ==========	==========	==========	==========
                Religion	Christian	Muslim		Atheist
                ==========	==========	==========	==========
                Christian	1		0		0
                Muslim		0		1		0
                Atheist		0		0		1	
                ==========	==========	==========	==========

    References
    ----------
    [1] https://en.wikiversity.org/wiki/Dummy_variable_(statistics)
    """
    for column in column_names:
        if isinstance(column, str) and column in data_frame:
            dummies = pd.get_dummies(data_frame[column])
            data_frame = pd.concat([data_frame, dummies], axis=1)
            data_frame = data_frame.drop([column], axis=1)
    return data_frame


def split_work_rate(data_frame):
    """Split 'Work Rate' column into two and return the DataFrame.
    
    Split 'Work Rate' column of `data_frame` into 'Defensive Work Rate'
    and 'Offensive Work Rate', apply `work_format` function to the 
    columns and return the modified DataFrame.

    Parameters
    ----------
    data_frame : pandas.DataFrame
        DataFrame containing a 'Work Rate' column to be split.

    Returns
    -------
    data_frame : pandas.DataFrame
        The DataFrame with the 'Work Rate' column split into formatted
        defensive and offensive work rate columns.

    See Also
    --------
    apply_format, work_format

    Notes
    -----
    This function can be used to split and format work rate column into
    defensive and offensive work rates of a player as they are stored in
    one column in the FIFA19 data set.

    Examples
    --------
    >>> data = pd.read_csv("data.csv")
    >>> print(data[['Work Rate']][0:3]) #print first few rows
            Work Rate
    0  Medium/ Medium
    1       High/ Low
    2    High/ Medium
    >>> data = split_work_rate(data)
    >>> print(data[['Defensive Work Rate', 'Offensive Work Rate']][0:3])
       Defensive Work Rate  Offensive Work Rate
    0                    1                    1
    1                    2                    0
    2                    2                    1
    """
    data_frame.rename(columns={'Work Rate': 'Work'}, inplace=True)
    data_frame[['Defensive Work Rate', 'Offensive Work Rate']] = data_frame.Work.str.split('/ ', expand=True)
    data_frame = data_frame.drop('Work', axis=1)
    return apply_format(data_frame, ['Defensive Work Rate', 'Offensive Work Rate'], work_format)


def preprocess(data):
    """Preprocess data to enable its analysis.

    Perform optimal preprocessing on the FIFA 19 data set. Drop irrelevant
    attributes. Convert attribute types, e.g. categorical data into numerical
    or floating point numbers carrying integers into integers. Manage column
    representation of attributes. Return the preprocessed DataFrame,
    ready to perform data analysis on it.

    Parameters
    ----------
    data : pandas.DataFrame
        Data to preprocess.

    Returns
    -------
    data : pandas.DataFrame
        Preprocessed data, ready to perform analysis on it.

    See Also
    --------
    pandas.DataFrame.drop, pandas.DataFrame.dropna
    exclude_goalkeepers, apply_format, money_format, to_int,
    to_dummy, split_work_rate
    """
    # Drop useless attributes.
    # Unnamed: 0 is an index (0 - n).
    # ID is FIFA19's internal id.
    # Photo, Flag and Club Logo are images.
    # Real Face - Yes/No value if the game uses a 3D scan of the actual face of the player.
    # Loaned From is usually missing, duration of the contract and
    # date of joining the club are not essential.
    # Name and body parameters are not correlated to wage.
    data = data.drop(['Unnamed: 0', 'ID', 'Name', 'Photo', 'Flag', 'Club Logo',
                        'Loaned From', 'Height', 'Weight', 'Body Type', 'Real Face',
                        'Joined', 'Contract Valid Until'], axis=1)

    # Exclude goalkeepers as they constitute a special class of players and may
    #  confuse algorithms analyzing it.
    data = exclude_goalkeepers(data)
    
    # Compute ratings on specific positions on the field and on football skills.
    for label in data.columns[15:41]:
        data[label] = data[label].apply(rating_format)
    for label in data.columns[41:75]:
        data[label] = data[label].apply(to_int)

    # Drop rows with missing values.
    data.dropna(inplace=True)

    # Convert monetary amounts.
    data = apply_format(data, ['Wage', 'Value', 'Release Clause'], money_format)

    # Convert floats to int as the nature of this information ('Jersey Number',
    # 'International Reputation', 'Skill Moves', 'Weak Foot') is discrete.
    data = apply_format(data, ['Jersey Number', 'International Reputation',
                                 'Skill Moves', 'Weak Foot'], to_int)

    # Convert categorical data to dummy variables in order to enable its analysis.
    data = to_dummy(data, ['Preferred Foot', 'Club', 'Position', 'Nationality'])

    # Split work rate into defensive and offensive work rate.
    data = split_work_rate(data)

    return data

