# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 07:57:50 2021

@author: David
"""


import numpy as np
import pandas as pd

def generateFleet():

    siteList = [
        ('BRCP', 1),
        ('BRPP', 0.75),
        ('BRPO', 0.75),
        ('MBPP', 0.9),
        ('BPEP', 0.6),
        ('SAR', 0.5),
        ('SCP', 2),
        ('FEP', 0.3),
        ('AMPP', 0.3),
        ('NDG', 0.8),
        ('FAW', 0.4)]

    startDate = np.datetime64('2010-01')
    endDate = np.datetime64('2020-12')
    
    dateRange = pd.date_range(start=startDate, end=endDate, freq='M')
    
    allBudgets = []
    for site, scale in siteList:
        curBudget = makeBudget(site, scale, dateRange)
        allBudgets.append(curBudget)
        
    allBudgets = pd.concat(allBudgets)
    
    return allBudgets


def makeBudget(siteName, scale, dateRange):
    
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
    
    dfAgg = [None]
    
    for curEnergy in energyList:
        dfAgg.append(makeBudget_byLineItem('Energy', dateRange, curEnergy, 3e5*scale, 5e4*scale))
        
    for curCat in catList:
        dfAgg.append(makeBudget_byLineItem('Catalyst', dateRange, curCat, 2e5*scale, 5e4*scale))
        
    for curChem in chemList:
        dfAgg.append(makeBudget_byLineItem('Chemical', dateRange, curCat, 2e5*scale, 1e4*scale))
        
    for curMat in materialsList:
        dfAgg.append(makeBudget_byLineItem('Shipping Material', dateRange, curCat, 1e5*scale, 5e3*scale))
        
    for curFixed in fixedList:
        dfAgg.append(makeBudget_byLineItem('Fixed Cost', dateRange, curCat, 1e6*scale, 1e4*scale))
        
    dfAgg = pd.concat(dfAgg)
    
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
