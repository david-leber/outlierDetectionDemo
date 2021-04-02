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
    
    """
    chanceToHaveGrowth = .1
    chanceToHaveZero = .01
    chanceToHaveStepChange = .1
    
    stepChangeRange = .3
    """
    
    chanceToHaveOutlier = 0.01  # .01
    outlierRange = [1.2, 5]
    
    chanceToRamp = 0.3  # .3
    rampRange = [.8, 1.2]
    rampTime = [6, 60]
    
    chanceToOffsetCosts = .03
    
    values = np.random.normal(average, deviation, (len(dateRange,)))
    values[values<0] = 0
    
        
    while np.random.uniform() < chanceToRamp:
        randomDate = int(np.random.choice(len(values), size=1))
        endDate = randomDate + np.random.randint(*rampTime)
        rampAmount = np.random.uniform(*rampRange)
        rampFactors = __generateRamp(len(values), randomDate, endDate, rampAmount)
        
        values = values * rampFactors
    
    while np.random.uniform() < chanceToOffsetCosts:
        randomDate = int(np.random.choice(len(values)-1, size=1))
        values[randomDate+1] += values[randomDate]
        values[randomDate] = 0
    
    while np.random.uniform() < chanceToHaveOutlier:
        # Pick a date randomly
        randomDate = int(np.random.choice(len(values), size=1))
        values[randomDate] = values[randomDate]*np.random.uniform(
            outlierRange[0], outlierRange[1])
        
    data = {
        'Date': dateRange,
        'Value': values
    }
    
    dfOut = pd.DataFrame(data)
    dfOut['Line Item'] = lineItem
    dfOut['Category'] = category
    
    return dfOut

def __generateRamp(length, startIndex, endIndex, rampAmount):
    
    ramp = np.ones((length,))
    ramp[endIndex:] = rampAmount
    print("Ramping to", rampAmount, " from", startIndex, " to", endIndex)
    
    for i in range(startIndex, min(endIndex, length)):
        ramp[i] = i*(rampAmount-1)/(endIndex-startIndex)+1
    
    return ramp
