# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 23:12:52 2021

@author: David
"""

import numpy as np
import pandas as pd

siteList = [
    'BRCP',
    'BRPP',
    'BRPO',
    'MBPP',
    'BPEP',
    'SAR',
    'SCP',
    'FEP',
    'AMPP'
    'NDG',
    'FAW']

chemList = [
    'Caustic',
    'Sulfuric Acid',
    'DMF',
    'DMS',
    'Antifoam']

catList = [
    'Alumina',
    'HDPE',
    'LDPE',
    'Poly',
    'Clay']

materialsList = [
    'Railcars',
    'Pallets',
    'Plastic Wrap',
    'Film Wrap',
    'Crates',
    'Barrels']

energyList = [
    'Steam',
    'Fuel',
    'Electric']

fixedList = [
    'SWB',
    'Maintenance',
    'Amortization']


startDate = np.datetime64('2010-01')
endDate = np.datetime64('2020-12')

dateRange = pd.date_range(start=startDate, end=endDate, freq='M')


def makeBudget(siteName, dateRange):
    
    dfAgg = None
    
    for curEnergy in energyList:
        df = makeBudget_byLineItem('Energy', dateRange, curEnergy, 3e5, 5e4)
        
        if dfAgg is None:
            dfAgg = df
        else:
            dfAgg = pd.concat([dfAgg, df])
        
    for curCat in catList:
        df = makeBudget_byLineItem('Catalyst', dateRange, curCat, 2e5, 5e4)
        dfAgg = pd.concat([dfAgg, df])
        
    for curChem in chemList:
        df = makeBudget_byLineItem('Chemical', dateRange, curCat, 2e5, 1e4)
        dfAgg = pd.concat([dfAgg, df])
        
    for curMat in materialsList:
        df = makeBudget_byLineItem('Shipping Material', dateRange, curCat, 1e5, 5e3)
        dfAgg = pd.concat([dfAgg, df])
        
    for curFixed in fixedList:
        df = makeBudget_byLineItem('Fixed Cost', dateRange, curCat, 1e6, 1e4)
        dfAgg = pd.concat([dfAgg, df])
    
    dfAgg['Site'] = siteName
    
    return dfAgg    
    
        
def makeBudget_byLineItem(category, dateRange, lineItem, average, deviation):
    
    values = np.random.normal(average, deviation, (len(dateRange,)))
    values[values<0] = 0
    
    data = {
        'Date': dateRange,
        'Value': values
    }
    
    dfOut = pd.DataFrame(data)
    dfOut['Line Item'] = lineItem
    dfOut['Category'] = category
    
    return dfOut

brcpBudget = makeBudget('BRCP', dateRange)
