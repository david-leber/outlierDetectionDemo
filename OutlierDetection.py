# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 23:04:37 2021

@author: David
"""

import pandas as pd

def findOutliers(df, level='Site'):
    
    dfByDate = df.groupby([level, 'Date']).sum()['Value'].reset_index()
    
    dfStats = dfByDate.groupby(level).agg({
        'Value': ['mean', 'std']}).reset_index()
    
    dfByDateWithStats = pd.merge(dfByDate, dfStats)
    
    print(dfByDateWithStats)