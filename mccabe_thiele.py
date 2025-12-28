import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

plt.rcParams["figure.figsize"] = (10,5)

plt.rcParams["figure.figsize"] = (8,8)

l = [0, 0.055, 0.321, 0.442, 0.570, 0.753, 0.817, 0.825, 0.924, 1]
g = [0, 0.126, 0.505, 0.636, 0.743, 0.870, 0.900, 0.912, 0.966, 1]
sigma = [0.1,1,1,1,1,1,1,1,1,0.1]
def vergleich(x, o, p, q):
    return o*x**2 + p*x + q
myline = np.linspace(0, 1, 100)
param, param_cov = curve_fit(vergleich, l, g, sigma=sigma)
o,p,q = param

# versuch 2
xk = 0.919
xs = 0.393
xf = 0.5
nu = 6.12
f = 1.096

vg = np.array([0,nu/(nu+1), +xk/(nu+1)]) #coeff of VG
sg = np.array([0,f/(f-1), -xf/(f-1)])    #coeff of SG

# Get both intersection points and select the correct one
px_all = np.roots(vg-sg)  # This gives both roots
# Choose the one that's not xk (or based on your logic)
px = px_all[0] if abs(px_all[0] - xk) > 0.01 else px_all[1]
py = f/(f-1)*px - xf/(f-1)  # Fixed: was 0.5, should be xf

#px = np.roots(vg-sg)  #intersect VG-SG, x value
#py = f/(f-1)*px - 0.5/(f-1) #intersect VG-SG, x value
def v(x, nu=nu, xk=xk): #VG
    return nu/(nu+1)*x +xk/(nu+1)
def s(x, f=f, xf=xf): #SG
    return f/(f-1)*x -xf/(f-1)
nu2 = s(0)
def a(x, nu2=nu2, xs=xs): #AG
    return nu2/(nu2-1)*x -xs/(nu2-1)

#bilanzgerade
bx = np.roots(param-sg)[1]
by = s(bx)
def bgr(x):
    return (xk-by)/(xk-bx)*x + (xk-bx)

x = [xk]
y = [xk]
while x[-1] > xs:
    y.append(y[-1])
    new = np.roots(param-[0,0,y[-1]])
    x.append(new[1])
    x.append(new[1])
    if x[-1] >= px:
        y.append(v(x[-1]))
    else:
        y.append(a(x[-1])) if x[-1] > xs else y.append(x[-1])
x,y

plt.plot(myline, vergleich(myline, o,p,q), 'k')
plt.plot(myline, myline, 'k')
plt.xlabel(r'$mol\%_{EtOH}$ (l) [mol/mol]', fontsize = 15)
plt.ylabel(r'$mol\%_{EtOH}$ (g) [mol/mol]', fontsize = 15)
plt.plot([xk,xk], [0, xk], 'g:') #x_kopf
plt.plot([xs,xs], [0, xs], 'g:') #x_sumpf
plt.plot([xf,xf], [0, xf], 'g:') #x_feed
plt.annotate('$mol\%_E$', xy=(xk+0.015,0), size=15)
plt.annotate('$mol\%_S$', xy=(xs+0.015,0), size=15)
plt.annotate('$mol\%_F$', xy=(xf+0.015,0), size=15)
plt.plot([xk,px], [xk, py], 'y-.') #verstäerkergerade
plt.plot([xf,px], [xf, py], 'm-') #schnittpunktgerade
plt.plot([bx,px], [by, py], 'm-.')
plt.plot([xs,px], [xs, py], 'y-.') #abtriebsgerade
plt.plot(x, y, 'r-')
plt.plot([xk, 0], [xk, bgr(0)], 'y-.')
plt.savefig('mctd-er.svg')