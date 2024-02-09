import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import scienceplots
import math


plt.style.use(['science','no-latex','nature','retro'])

font = {'size'   : 11}

matplotlib.rc('font', **font)
plt.rc('axes', labelsize=11)
matplotlib.rc('xtick', labelsize=11) 
matplotlib.rc('ytick', labelsize=11)
plt.rc('legend', fontsize=11)    


df = pd.read_csv('hubble_constant_B.csv')

plt.ylim(ymin=0,ymax=22_000)
plt.xlim(xmin=0,xmax=350)

x = df['distance']
x_err = df['distance_error']
y = df['velocity']
y_err = df['velocity_error']

n = len(x)

#plt.scatter(x,y,s=64)
plt.errorbar(x, y, xerr=x_err,yerr=y_err, fmt='o')

x = np.array(x)
x = x[:,np.newaxis]
a, R, _, _ = np.linalg.lstsq(x, y)

x = np.insert(x, 0, 0, axis=0)

plt.plot(x, a*x,'black')

#plt.legend(['Single Author','Domestic Collaboration','International Collaboration'], ncol=3, title='Collaboration Type', bbox_to_anchor=(0.87, 1.125))
plt.title('Type 1a Supernova from 2020-2021')
plt.ylabel('Velocity from redshift / km s-1')
plt.xlabel('Distance from magnitude / Mpc')

#plt.xticks(ticks=range(0,len(x)+1,1),rotation=0)
plt.yticks(np.arange(0, 22_000, 5000.0))

rss = 0
for i in range(n):
	calc = a[0] * x[i]
	act = y[i]

e = math.sqrt(R/n)

'''
slopeh = (y.iloc[-1]+e)/x[1]
slopel = (y.iloc[-1]-e)/x[1]

print(y,y.iloc[-1])


plt.plot(x, slopeh*x,'blue','-')
plt.plot(x, slopel*x,'blue','-')
'''

y = np.array(y)

print(a,R)
print(1 - R / (y.size * y.var()))

plt.show()
