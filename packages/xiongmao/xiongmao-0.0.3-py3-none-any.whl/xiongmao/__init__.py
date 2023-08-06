#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 14:47:33 2020

Bind Pandas methods to dataframe for simpler use.

General fn bound to Methods
xTab - bound crosstab to df
todf - bound dataframe constructor to series


@author: jcl
"""

import pandas as pd
from pandas import DataFrame # import DataFrame separately to act on
from pandas import Series

def xTab(self, vertical, horizontal):
    """
    Parameters
    ----------
    vertical: string
        column name for vertical.
    horizontal: string
        column name for horizontal.

    Returns
    -------
    Dataframe representing the crosstab of self.vertical, self.horizontal
    """

    try:
        return pd.crosstab(self[vertical], self[horizontal])
    except:
        return None


def todf(self, nameL=None):
    """
    Parameters
    ----------
    self 

    Returns
    -------
    Dataframe
    If a nameL is provided, columns are renamed to nameL
    """
    if isinstance(self, pd.DataFrame):
        if nameL:
            if len(self.columns) == len(nameL):
                tR = self.copy()
                tR.columns = nameL

    elif isinstance(self, pd.Series):
        tR = pd.DataFrame(self)
        if nameL:
            if len(nameL) == 1:
                tR.columns = nameL

    else:
        return None

    return tR

DataFrame.xTab = xTab # give the xTab method to DataFrame
DataFrame.todf = todf
Series.todf = todf


if __name__ == "__main__":
    exampleD = {"sv": "a a a a a b b b b b".split() \
                , "x": [1, 2, 3, 2, 3, 4, 4, 5, 6, 1]}

    # either one of these works
    # exampleR = DataFrame(exampleD)
    exampleR = pd.DataFrame(exampleD) 
    
    # classic crosstab calls are messy
    classicR = pd.crosstab(exampleR.query("x < 6").x \
                           , exampleR.query("x < 6").sv)
    # xTab calls are neater
    simpleR = exampleR.query("x < 6").xTab("x", "sv")

    # showing that the crosstabs are the same
    print ((simpleR == classicR).min().min())

    print (exampleR.sv.value_counts().todf().reset_index())
