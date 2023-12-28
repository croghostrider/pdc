import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# define mixing model
def mixer(x,t,Tf,Caf):
    # Inputs (2):
    # Tf = Feed Temperature (K)
    # Caf = Feed Concentration (mol/m^3)
    # States (2):
    # Concentration of A (mol/m^3)
    Ca = x[0]
    return 1 * (Caf - Ca)

# Initial Condition
Ca0 = 0.0
# Feed Temperature (K)
Tf = 300
# Feed Concentration (mol/m^3)
Caf = 1
# Time Interval (min)
t = np.linspace(0,10,100)

# Simulate mixer
Ca = odeint(mixer,Ca0,t,args=(Tf,Caf))

# Construct results and save data file
# Column 1 = time
# Column 2 = concentration
data = np.vstack((t,Ca.T)) # vertical stack
data = data.T             # transpose data
np.savetxt('data.txt',data,delimiter=',')

# Plot the results
plt.plot(t,Ca,'r-',linewidth=3)
plt.ylabel('Ca (mol/L)')
plt.legend(['Concentration'],loc='best')
plt.xlabel('Time (hr)')
plt.show()