import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.optimize import minimize
from scipy.interpolate import interp1d

# Import CSV data file
url = 'http://apmonitor.com/pdc/uploads/Main/tclab_data3.txt'
data = pd.read_csv(url)
t = data['Time'].values
u = data['Q1'].values
yp = data['T1'].values
u0=u[0]; yp0=yp[0]

# specify number of steps
ns = len(t)
delta_t = t[1]-t[0]
# create linear interpolation of the u data versus time
uf = interp1d(t,u)

# define first-order plus dead-time approximation    
def fopdt(y,t,uf,Km,taum,thetam):
    # arguments
    #  y      = output
    #  t      = time
    #  uf     = input linear function (for time shift)
    #  Km     = model gain
    #  taum   = model time constant
    #  thetam = model time constant
    # time-shift u
    try:
        um = uf(0.0) if (t-thetam) <= 0 else uf(t-thetam)
    except:
        #print('Error with time extrapolation: ' + str(t))
        um = u0
    return (-(y-yp0) + Km * (um-u0))/taum

# simulate FOPDT model with x=[Km,taum,thetam]
def sim_model(x):
    # input arguments
    Km = x[0]
    taum = x[1]
    thetam = x[2]
    # storage for model values
    ym = np.zeros(ns)  # model
    # initial condition
    ym[0] = yp0
    # loop through time steps    
    for i in range(0,ns-1):
        ts = [t[i],t[i+1]]
        y1 = odeint(fopdt,ym[i],ts,args=(uf,Km,taum,thetam))
        ym[i+1] = y1[-1]
    return ym

# define objective
def objective(x):
    # simulate model
    ym = sim_model(x)
    # calculate objective
    obj = 0.0
    for i in range(len(ym)):
        obj = obj + (ym[i]-yp[i])**2    
    # return result
    return obj

# initial guesses
x0 = np.zeros(3)
x0[0] = 1.0 # Km
x0[1] = 120.0 # taum
x0[2] = 5.0 # thetam

# show initial objective
print(f'Initial SSE Objective: {str(objective(x0))}')

# optimize Km, taum, thetam
#solution = minimize(objective,x0)

# Solve with bounds on variables
bnds = ((0.4, 1.0), (50.0, 250.0), (0.0, 30.0))
solution = minimize(objective,x0,bounds=bnds,method='SLSQP')
x = solution.x

# show final objective
print(f'Final SSE Objective: {str(objective(x))}')