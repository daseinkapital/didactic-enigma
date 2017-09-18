# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
import numpy as np
import copy

class Command(BaseCommand):
    args = '<none>'
    help = 'Runs algorithms on the data to detect disease anamolies.'
    
    def handle(self, *args, **options):

#        def f(x):
#            return math.sin(x[0]) * math.cos(x[1]) * (1. / (abs(x[2]) + 1))
#    
#        print(nelder_mead(f, np.array([0., 0., 0.])))
        
#        series = [3,10,12,13,12,10,12]
        series = [30,21,29,31,40,48,53,47,37,39,31,29,17,9,20,24,27,35,41,38,
          27,31,27,26,21,13,21,18,33,35,40,36,22,24,21,20,17,14,17,19,
          26,29,40,31,20,24,18,26,17,9,17,21,28,32,46,33,23,28,22,27,
          18,8,17,21,31,34,44,38,31,30,26,32]
        
#        reg = double_exponential_smoothing(series, alpha=0.9, beta=0.9)
        reg = triple_exponential_smoothing(series, slen=12, alpha=0.716, beta=0.029, gamma=0.993, n_preds=24)        
        Mse = MSE(reg, series)
        print("MSE is " + str(Mse))
        
        mead_coefficients = nelder_mead_smoothing(optimize_triple, np.array([0., 0., 0.]), series)
        print(mead_coefficients[0])
 
"""
Averages
"""
#averaging function reduces imports (allows for moving average, defaults to
#regular average)
def average(series, n=None):
    if n is None:
        return average(series, len(series))
    return float(sum(series[-n:]))/n
 
# weighted average, weights is a list of weights
def weighted_average(series, weights):
    result = 0.0
    weights.reverse()
    for n in range(len(weights)):
        result += series[-n-1] * weights[n]
    return result

"""
Triple Exponential Smoothing Helper Functions
"""
#defines the trend across the seasons
def initial_trend(series, slen, trend="add"):
    sum = 0.0
    for i in range(slen):
        if trend == "add":
            sum += float(series[i+slen] - series[i]) / slen
        elif trend == "mult":
            sum += float(series[i+slen]/series[i]) / slen
    return sum / slen

#creates the seasonal components
def initial_seasonal_components(series, slen):
    seasonals = {}
    season_averages = []
    n_seasons = int(len(series)/slen)
    # compute season averages
    for j in range(n_seasons):
        season_averages.append(sum(series[slen*j:slen*j+slen])/float(slen))
    # compute initial values
    for i in range(slen):
        sum_of_vals_over_avg = 0.0
        for j in range(n_seasons):
            sum_of_vals_over_avg += series[slen*j+i]-season_averages[j]
        seasonals[i] = sum_of_vals_over_avg/n_seasons
    return seasonals

"""
Exponential Smoothing Algorithms
"""

# given a series and alpha, return series of smoothed points
def single_exponential_smoothing(series, alpha):
    result = [series[0]] # first value is same as series
    for n in range(1, len(series)):
        result.append(alpha * series[n] + (1 - alpha) * result[n-1])
    return result


# given a series and alpha and beta parameters, return series of smoothed points
def double_exponential_smoothing(series, alpha, beta, trend="add"):
    result = [series[0]]
    for n in range(1, len(series)+1):
        if n == 1:
            if trend == "add":
                level, trend = series[0], series[1] - series[0]
            elif trend == "mult":
                level, trend = series[0], series[1]/series[0]
        if n >= len(series): # we are forecasting
          value = result[-1]
        else:
          value = series[n]
        last_level, level = level, alpha*value + (1-alpha)*(level+trend)
        trend = beta*(level-last_level) + (1-beta)*trend
        result.append(level+trend)
    return result

# given a series and alpha, beta, and gamma parameters, returns smoothed points with a forecasted prediction
def triple_exponential_smoothing(series, slen, alpha, beta, gamma, n_preds, trend="add"):
    result = []
    seasonals = initial_seasonal_components(series, slen)
    for i in range(len(series)+n_preds):
        if i == 0: # initial values
            smooth = series[0]
            trend = initial_trend(series, slen, trend=trend)
            result.append(series[0])
            continue
        if i >= len(series): # we are forecasting
            m = i - len(series) + 1
            result.append((smooth + m*trend) + seasonals[i%slen])
        else:
            val = series[i]
            last_smooth, smooth = smooth, alpha*(val-seasonals[i%slen]) + (1-alpha)*(smooth+trend)
            trend = beta * (smooth-last_smooth) + (1-beta)*trend
            seasonals[i%slen] = gamma*(val-smooth) + (1-gamma)*seasonals[i%slen]
            result.append(smooth+trend+seasonals[i%slen])
    return result


"""
Goal Seeking Error Calculators
"""
#returns the Mean Square Error for the regression
def MSE(reg, data):
    sum = 0
    for i in range(len(data)):
        sum += (data[i] - reg[i])*(data[i] - reg[i])
    return sum / len(data)
        

#returns the Mean Absolute Deviation for the regression
def MAD(reg, data):
    sum = 0
    for i in range(len(data)):
        sum += abs(data[i] - reg[i])
    return sum / len(data)
    

#returns the Mean Absolute Percent Error for the regresssion
def MAPE(reg, data):
    sum = 0
    for i in range(len(data) - 1):
        sum += abs((data[i + 1] - reg[i + 1])/reg[i + 1])
    return sum / len(data)

"""
Functions for optimizing smoothing
"""
def optimize_double(series, array, trend, optimizer="MSE"):
    reg = double_exponential_smoothing(series, array[0], array[1], trend)
    if optimizer is "MSE":
        return MSE(reg, series)
    elif optimizer is "MAD":
        return MAD(reg, series)
    elif optimizer is "MAPE":
        return MAPE(reg, series)

def optimize_triple(series, array, trend, optimizer="MSE", slen=12):
    reg = triple_exponential_smoothing(series, slen, array[0], array[1], array[2], trend=trend)
    if optimizer is "MSE":
        return MSE(reg, series)
    elif optimizer is "MAD":
        return MAD(reg, series)
    elif optimizer is "MAPE":
        return MAPE(reg, series)


"""
Optimization algorithms
"""

#optimization for smoothing (only works on double or triple smoothing)
def nelder_mead_smoothing(f, x_start, data, optimizer="MSE", trend_type="add",
                step=0.1, no_improve_thr=10e-6,
                no_improv_break=10, max_iter=0,
                alpha=1., gamma=2., rho=-0.5, sigma=0.5):
    '''
        @param f (function): function to optimize, must return a scalar score
            and operate over a numpy array of the same dimensions as x_start
        @param x_start (numpy array): initial position
        @param data (list): original data
        @optimizer (str): takes value "MSE", "MAD", or "MAPE"
            defaults to MSE
        @param trend_type (string): either "add" or "mult" for type of trend
            defaults to add
        @param step (float): look-around radius in initial step
        @no_improv_thr,  no_improv_break (float, int): break after no_improv_break iterations with
            an improvement lower than no_improv_thr
        @max_iter (int): always break after this number of iterations.
            Set it to 0 to loop indefinitely.
        @alpha, gamma, rho, sigma (floats): parameters of the algorithm
        return: tuple (best parameter array, best score)
    '''

    # init
    dim = len(x_start)
    prev_best = f(data, x_start, trend=trend_type)
    no_improv = 0
    res = [[x_start, prev_best]]

    for i in range(dim):
        x = copy.copy(x_start)
        x[i] = x[i] + step
        score = f(data, x, trend=trend_type)
        res.append([x, score])

    # simplex iter
    iters = 0
    while 1:
        # order
        res.sort(key=lambda x: x[1])
        best = res[0][1]

        # break after max_iter
        if max_iter and iters >= max_iter:
            return res[0]
        iters += 1

        # break after no_improv_break iterations with no improvement
        print('...best so far:', best)

        if best < prev_best - no_improve_thr:
            no_improv = 0
            prev_best = best
        else:
            no_improv += 1

        if no_improv >= no_improv_break:
            return res[0]

        # centroid
        x0 = [0.] * dim
        for tup in res[:-1]:
            for i, c in enumerate(tup[0]):
                x0[i] += c / (len(res)-1)

        # reflection
        xr = x0 + alpha*(x0 - res[-1][0])
        rscore = f(data, xr, trend=trend_type)
        if res[0][1] <= rscore < res[-2][1]:
            del res[-1]
            res.append([xr, rscore])
            continue

        # expansion
        if rscore < res[0][1]:
            xe = x0 + gamma*(x0 - res[-1][0])
            escore = f(data, xe, trend=trend_type)
            if escore < rscore:
                del res[-1]
                res.append([xe, escore])
                continue
            else:
                del res[-1]
                res.append([xr, rscore])
                continue

        # contraction
        xc = x0 + rho*(x0 - res[-1][0])
        cscore = f(data, xc, trend=trend_type)
        if cscore < res[-1][1]:
            del res[-1]
            res.append([xc, cscore])
            continue

        # reduction
        x1 = res[0][0]
        nres = []
        for tup in res:
            redx = x1 + sigma*(tup[0] - x1)
            score = f(data, redx, trend=trend_type)
            nres.append([redx, score])
        res = nres