from datetime import datetime
import itertools

def squaresum( values):
    sum = 0.0
    for x in values:
        sum += x * x   
    return sum

def productsum( xvalues, yvalues):
    sum = 0.0
    for x,y in zip(xvalues, yvalues):
        sum += x * y
    return sum

def sum(values):
    sum = 0.0
    for x in values:
        sum += x
    return sum

def variance( values):
    n = len(values)
    if n == 0:
        return None
    return (1.0/(n - 1))*(squaresum(values) - (sum(values)*sum(values))/n)

def covariance( xvalues, yvalues ):
    n = len(xvalues)
    if n == 0:
        return None
    return (1.0/(n - 1))*(productsum( xvalues, yvalues)-((1.0/n)*sum(xvalues)*sum(yvalues)))

def regressioncoefficient( xvalues, yvalues):
    cov = covariance( xvalues, yvalues )
    if cov:
        return cov / variance( xvalues )    
    else:
        return None

def regressionconstant ( xvalues, yvalues):
    n = len( xvalues)
    if n == 0:
        return None
    return (sum(yvalues) / n) - (regressioncoefficient( xvalues, yvalues) * (sum( xvalues)/ n))

def calculateregression( xvalues, yvalues):
    b = regressioncoefficient( xvalues, yvalues )
    k = regressionconstant ( xvalues, yvalues)
    if b:
        ylist = []
        for x in xvalues:
            y = b * x + k
            ylist.append(y)
        return ylist
    else:
        return None

def calculatetimeseries( isodates, yvalues ):
    xlist = []
    for isodate in isodates:
        d = datetime.fromisoformat(isodate)
        x = d.toordinal()
        xlist.append(x)
    return calculateregression( xlist, yvalues)

if __name__ == "__main__":
    x = [ 2.8, 2.9, 3.0, 3.1, 3.2, 3.2, 3.2, 3.3, 3.4 ]
    y = [ 27.0, 23.0, 30.0, 28.0, 30.0, 32.0, 34.0, 33.0, 30.0 ]

    var = variance(x)
    cov = covariance(x,y)
    b = regressioncoefficient( x,y)
    k = regressionconstant( x, y)
    ytrend = calculateregression( x, y)
    print( f"Variance: {var}  Covariance: {cov}  b = {b}  k = {k}")

    for xv, yv, yt in zip(x, y, ytrend):
        print( f"{xv} {yv} {yt}")
    
    x = [ 
            "2025-05-01 12:45", 
            "2025-05-02 15:45", 
            "2025-05-05 12:45", 
            "2025-05-07 08:45", 
            "2025-05-12 12:00", 
            "2025-05-14 12:45", 
            "2025-05-18 12:45", 
            "2025-05-20 12:45", 
            "2025-05-22 12:45", 
        ]

    xlist = []
    for isodate in x:
        d = datetime.fromisoformat(isodate)
        xval = d.toordinal()
        xlist.append(xval)

    var = variance(xlist)
    cov = covariance(xlist,y)
    b = regressioncoefficient( xlist,y)
    k = regressionconstant( xlist, y)
    ytrend = calculatetimeseries( x, y)
    print( f"Variance: {var}  Covariance: {cov}  b = {b}  k = {k}")

    for xv, yv, yt in zip(x, y, ytrend):
        print( f"{xv} {yv} {yt}")


