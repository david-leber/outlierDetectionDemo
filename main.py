# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 23:12:52 2021

@author: David
"""

from generateFleet import generateFleet


myFleet = generateFleet()

siteStats = myFleet.groupby('Site').sum().sort_values('Value', ascending=False)
print(siteStats['Value'])