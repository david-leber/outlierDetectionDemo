# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 23:12:52 2021

@author: David
"""

from generateFleet import generateFleet
import OutlierDetection
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

myFleet = generateFleet()

# OutlierDetection.findOutliers(myFleet)


level = 'Site'
dfByDate = myFleet.groupby([level, 'Date']).sum()['Value'].reset_index()

dfStats = dfByDate.groupby(level).agg({
    'Value': ['mean', 'std']}).reset_index()
dfStats.columns = [level, 'avg', 'std']

dfByDateWithStats = pd.merge(dfByDate, dfStats)

dfByDateWithStats['stdFromAvg'] = (dfByDateWithStats['Value']-dfByDateWithStats['avg'])/dfByDateWithStats['std']
dfByDateWithStats['outlier_3s'] = np.abs(dfByDateWithStats['stdFromAvg'])>=3
dfByDateWithStats['outlier_r4s'] = \
    (dfByDateWithStats['stdFromAvg']>=2) & (dfByDateWithStats['stdFromAvg'].shift(1)<=-2) | \
    (dfByDateWithStats['stdFromAvg']<=-2) & (dfByDateWithStats['stdFromAvg'].shift(1)>=2) | \
    (dfByDateWithStats['stdFromAvg']>=2) & (dfByDateWithStats['stdFromAvg'].shift(-1)<=-2) | \
    (dfByDateWithStats['stdFromAvg']<=-2) & (dfByDateWithStats['stdFromAvg'].shift(-1)>=2)
dfByDateWithStats['sideOfAverage'] = dfByDateWithStats['stdFromAvg'] / np.abs(dfByDateWithStats['stdFromAvg'])
dfByDateWithStats['rollingSideOfAverage'] = dfByDateWithStats['sideOfAverage'].rolling(window=10).sum()
dfByDateWithStats['outlier_10x'] = np.abs(dfByDateWithStats['rollingSideOfAverage'])>=10

outliers = dfByDateWithStats[
    (dfByDateWithStats['outlier_3s']) | 
    (dfByDateWithStats['outlier_10x']) | 
    (dfByDateWithStats['outlier_r4s']) 
]

print("Num outliers found: ", len(outliers))

for site in outliers['Site'].unique():
    
    curSiteData = dfByDateWithStats[dfByDateWithStats['Site']==site]
    curSiteOutliers = outliers[outliers['Site']==site]
    
    plt.figure()
    plt.plot(curSiteData['Date'], curSiteData['Value'])
    plt.plot(curSiteData['Date'], curSiteData['avg'], 'k')
    plt.plot(curSiteData['Date'], curSiteData['avg']+3*curSiteData['std'], 'b-')
    plt.plot(curSiteData['Date'], curSiteData['avg']-3*curSiteData['std'], 'b-')
    plt.plot(curSiteOutliers.loc[curSiteOutliers['outlier_3s'], 'Date'], curSiteOutliers.loc[curSiteOutliers['outlier_3s'], 'Value'], 'r.')
    plt.plot(curSiteOutliers.loc[curSiteOutliers['outlier_r4s'], 'Date'], curSiteOutliers.loc[curSiteOutliers['outlier_r4s'], 'Value'], 'g.')
    plt.plot(curSiteOutliers.loc[curSiteOutliers['outlier_10x'], 'Date'], curSiteOutliers.loc[curSiteOutliers['outlier_10x'], 'Value'], 'c.')
plt.title(site)