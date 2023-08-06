# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 18:26:54 2020

@author: Avery
"""
import pandas as pd
import numpy as np

def count_tickers(data):
    """
    Count the number of tickers in a yfinance.download.
    
    Parameters:
        data (dataFrame) -- dataFrame returned by yfinance.download(...)
    """
    count = 0
    metric = data.columns[0][0]
    for col in data.columns:
        if (col[0] == metric):
            count += 1
    return count

def clean_columns(data):
    """
    Untuple the dataframe data from a yfinance.download call.
    
    Downloading mutliple tickers simultaneously using yfinance creates a
    dataframe tuple columns in the form (<metric>, <ticker).
    This function moves the ticker to a column and returns a list of
    dataframes in which the ticker has been moved to a column.
    
    Parameters:
        data (dataFrame) -- dataFrame returned by yfinance.download(...)
    """
    frameList = []
    for i in range(0, count_tickers(data)):
        curTicker = data.columns[i][1] #ticker is always the second element of the tuple column
        df = data.copy()
        for col in df.columns:
            if (col[1] != curTicker):
                df = df.drop(col, axis=1)
        df.columns = [x[0] for x in df.columns]
        df["Ticker"] = [curTicker for x in df['Close']]
        frameList.append(df)
    
    return frameList

def movingAverageNP(npAry, period):
    """
    Calculate and return the moving average of a numpy array or pandas series
    
    Raises AttributeError if wrong type is passed in
    Parameters:
        npAry (np.array) -- numpy array to calculate moving average for
        period (int) -- the length of the moving average
    """
    retAry = np.nancumsum(npAry, dtype=float)
    retAry[period:] = retAry[period:] - retAry[:-period]
    retAry[:period-1] = np.nan
    return retAry / period

def movingAveragePD(pdSeries, period):
    """
    Calculate and return the moving average of a numpy array or pandas series
    
    Parameters:
        valList (np.array, pd.series) -- moving average is calculated for this
        period (int) -- the length of the average
    """
    return pdSeries.rolling(period).mean()

def emaNP(valList, period):
    """
    Calculate and return the exponential moving average of a numpy array
    
    Parameters:
        valList (np.array) -- numpy array to calculate moving average for
        period (int) -- the length of the average
    """
    emaVals = np.empty_like(valList)
    emaVals[0] = valList[0] #nothing to average for first value
    alpha = (2 / (period + 1))
    for i in range(1, len(valList)):
            emaVal = ((valList[i] - emaVals[i - 1])) * float(alpha) + emaVals[i - 1]
            emaVals[i] = emaVal
    return emaVals

def emaPD(pdSeries, period):
    """
    Calculate and return the exponential moving average of a numpy array
    
    Parameters:
        pdSeries (pd.series) -- pandas series to calculate moving average for
        period (int) -- the length of the average
    """
    return pdSeries.ewm(span=period, adjust=False).mean()

#calculates the current value minus the last value in a numpy array
#this needs to use numpy.roll
def calcSlope(npAry):
    """
    Calculate and return the instantaneous slope of a numpy array.
    
    Parameters:
        valList (np.array) -- numpy array to calculate slopes for
    """
    ret = npAry - np.roll(npAry, 1)
    ret[0] = 0
    return ret

def addMovingAverage(df, period, col="Close", dropna = False):
    """
    Add the moving average to a datafrom based on input column
    
    parameters:
        df (dataFrame) -- dataframe to calculate and append the indicator to
        period (int) -- the peiod of the moving average
        col (string) -- the column to compute the moving average of
        dropna (bool) -- whether to drop NaN rows and reindex afterwards
    """
    header = str(col) + " SMA(" + str(period) + ")"
    df[header] = df[col].rolling(period).mean()
    if (dropna):
        df.dropna(inplace = True)
        df.reset_index(drop = True, inplace = True)

def calc_Stochastic_K(df, period, close="Close", high="High", low="Low"):
    """
    Calculate unsmoothed stochastic K for a dataframe object.
    
    Returns a pandas Series
    Parameters:
        df (dataFrame) -- dataframe to calculate and append the indicator to
        period (int) -- the length of the lookback
        close (str) -- the "close" column used in stochastic calculation
        high (str) -- the "high" column used in stochastic calculation
        low (str) -- the "low" column used in stochastic calculation
    """
    closeSeries = df[close]
    highSeries = df[high].rolling(period).max()
    lowSeries = df[low].rolling(period).min()
    return (closeSeries - lowSeries) / (highSeries - lowSeries)

def addStochastic(df, period, kSmooth, d, close="Close", high="High", low="Low"):
    """
    Calculate and append the stochastic indicator to a dataframe object.
    
    Parameters:
        df (dataFrame) -- dataframe to calculate and append the indicator to
        period (int) -- the length of the lookback
        kSmooth (int) -- smoothing value for %K
        d (int) -- smoothing value for %D
        column (string) -- column name to use for input. Default is "Close"
    """
    kVals = calc_Stochastic_K(df, period, close, high, low)
    percentKVals = movingAveragePD(kVals, kSmooth)
    header = 'Stochastic %K (' + str(period) + ',' + str(kSmooth) + ',' + str(d) + ')'
    df[header] = percentKVals
    header = 'Stochastic %D (' + str(period) + ',' + str(kSmooth) + ',' + str(d) + ')'
    df[header] = movingAveragePD(percentKVals, d)

def calc_MACD(series, fast, slow):
    fastEMA = emaPD(series, fast)
    slowEMA = emaPD(series, slow)
    return fastEMA - slowEMA

#adds MACD to dataframe
def addMACD(df, fast, slow, signalSmooth, column = "Close"):
    """
    Calculate and append the MACD indicator to a dataframe object.
    
    Parameters:
        df (dataFrame) -- dataframe to calculate and append the indicator to
        fast (int) -- period of fast ema
        slow (int) -- period of slow ema
        signalSmooth (int) -- smoothing used to calculate signal line
        column (string) -- column name to use for input. Default is "Close"
    """
    macdVals = calc_MACD(df[column], fast, slow)
    signalVals = emaPD(macdVals, signalSmooth)
    histVals = macdVals - signalVals
    header = "MACD (" + str(fast) + "," + str(slow) + "," + str(signalSmooth) + ")"
    df[header] = macdVals
    df[header + " Signal"] = signalVals
    df[header + " Histogram"] = histVals

#populate successes. Populate array with 1 if entryColumn value + risk*targetPercent is hit
#before hitting min of barRisk
#add max stop loss so stop loss isn't giant
#add an entry_offset and only count if it's filled the next day.
    #this would require a success (1) failure (-1) and no entry (0)
def addLongSuccess(df, barRisk, targetPercent, entryColumn = "Close"):
    """
    Calculate and append a column win/loss column to a dataframe object.
    
    The entry is the value of entryColumn for the current bar.
    The minimum of the last "barRisk" bars as the stop loss.
    The first target is defined as follows:
        (entry - stop-loss) * targetPercent + entry
    If the high of any of the next bars hits the first target before the low
    falls below the stop loss, it is considered a success
    If the firstTarget and stoploss are hit on the same bar, it is not
    considered a success
    Parameters:
        df (dataFrame) -- dataframe to calculate and append the indicator to
        barRisk (int) -- number of bars to look back to calculate stop-loss
        targetPercent (int) -- percentage used to calculate the frist target
        column (string) -- column name to use for entry. Default is "Close"
    """
    successes = np.zeros_like(df[entryColumn].values)
    for i in range(len(df[entryColumn])):
        entry = df[entryColumn][i]
        stopLoss = df["Low"][i - barRisk:i + 1].min()
        risk = entry - stopLoss
        target = risk * targetPercent / 100.0 + entry
        j = i + 1
        success = None
        while (success == None and j < len(df[entryColumn])):
            if (df["Low"][j] < stopLoss):
                success = False
            elif (df["High"][j] >= target):
                success = True
                successes[i] = 1
            j += 1
    header = "Long r=" + str(barRisk) + " " + str(targetPercent) + "%"
    df[header] = successes

#need function to calculate winnings using some first exit and stop loss method
    
def changeColumnToDate(df, col="Date"):
    """
    Change a specified column of a dataframe from a string to a datetime
    
    Parameters:
        df (dataFrame) -- dataframe containing column to be converted
        col (str) -- column to converst from string to datetime
    """
    if (type(df.loc[0,col]) == np.datetime64):
        print("Already in date form")
        return
    df.loc[:,col] = pd.to_datetime(df.loc[:,col])

def clearDataLessThan(df, compareVal, col="Date"):
    """
    Return dataframe that has all rows removed with column value < compareVal
    
    Parameters:
        df (dataFrame) -- dataframe who's values will be compared
        compareVal (float, datetime) -- value to compare to df column values
        col (str) -- column indentifier of the column to compare
    """
    indexList = []
    for i in range(len(df[col])): #len(df["Date"])
        if (df[col][i] < compareVal):
            indexList.append(i)
    ret = df.drop(indexList)
    return ret.reset_index(drop = True)

def addPercentageChange(df, start="Open", end="Close"):
    """
    Add a percentage change series to a dataframe
    
    Parameters:
        df (dataFrame) -- dataframe to calculate and append the % change to
        start (string) -- string identifying the column containing start values
        end (string) -- string identifying the column containing end values
    """
    retSeries = df[start].rsub(df[end])
    retSeries = df[start].rdiv(retSeries)
    retSeries = retSeries.rmul(100)
    header = start + "/" + end + "%Change"
    df[header] = retSeries

def percentageOfColumn(df, col, percentOfCol):
    """
    Add a percentage of colmn to a dataframe object (col / percentOfCol)
    
    Parameters:
        df (dataframe) -- dataframe to calculate and append the indicator to
        col (str) -- divsor column identifier
        percentOfCol -- dividend column identifier
    """
    retSeries = df[col].rdiv(df[percentOfCol])
    retSeries = retSeries.rmul(100)
    header = col + "% of " + percentOfCol
    df[header] = retSeries

def consecutiveBarCount(df, start = "Open", end = "Close"):
    """
    Add a column for number of positive or negative bars
    
    The count will be negative for consecutive red bars and postive for
    consecutive green bars
    Parameters:
        df (dataframe) -- dataframe to calculate and append the column to
        start (str) -- string identifying the "Open" or starting value
        end (str) -- string identifying the "Close" or the ending value
    """
    diff = df.loc[:,start].rsub(df.loc[:,end])
    count = 0
    for i in range(len(diff)):
        if ((count < 0 and diff.at[i] > 0) or (count > 0 and diff.at[i] < 0)):
            count = 0
        if (diff.at[i] > 0):
            count = count + 1
        if (diff.at[i] < 0):
            count = count - 1
        diff.at[i] = count
    return diff
    #if (diff):