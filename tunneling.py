import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize

cali = .02
piezospeed = 200.0


scan= 'Gold/scan170111_59_111.dat'

def indexAt(scan):
    '''
    string --> int
    Recibe el nombre de un scan, y devuelve la posicion en que se separan las
    mediciones de making y breaking
    '''
    data = open(scan,'r')
    lines = data.readlines()
    lines = lines[10:]
    try:
        index = lines.index('@ \r\n')
    except ValueError:
        index = lines.index('@\r\n')
    return index

data = np.loadtxt(scan,comments='@',skiprows=10)
n = indexAt(scan)
data = data[0:n,:]

dist = data[:,0]
cond = data[:,1]

#Fiteo
def tunnel_model(dist , amp, phi):
    return amp * np.exp(- phi * dist)


plt.plot(dist,tunnel_model(dist,1,1))
plt.show()
