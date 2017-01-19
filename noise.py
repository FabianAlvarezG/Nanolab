import numpy as np
import scipy.stats
import matplotlib.pyplot as plt
from fitter import Fitter
import os

def indexAt(scan):
    '''
    string --> int
    Recibe el nombre de un scan, y devuelve la posicion en que se separan las
    mediciones de making y breaking
    '''
    data = open(scan, 'r')
    lines = data.readlines()
    lines = lines[10:]
    try:
        index = lines.index('@ \r\n')
    except ValueError:
        index = lines.index('@\r\n')
    return index


# Se toma una muestra de ruido de cada una de las trazas y se junta todo en
# un archivo
files = os.listdir('Gold')
noise_sample = []

for filename in files[0:100]:
    scan = 'Gold/' + filename
    data = np.loadtxt(scan, comments='@', skiprows=10)

    n = indexAt(scan)
    data = data[0:n, :]

    cond = data[:, 1]
    negative_index = np.where(cond <= 0)
    cond = np.delete(cond, negative_index)

    cond_sample = cond[1200:-1]

    noise_sample = np.append(noise_sample, cond_sample)

#Lo que se fiteara será el log de la conductancia
log_data = np.log10(noise_sample)

#De todos las distribuciones de la libreria Scipy, la johnson SU es la que
#que mejor ajusta el histograma. Para corroborar esto, usar libreria fitter
#Fit de los parametros de la ditribucion
a, b, mu, sigma = scipy.stats.johnsonsu.fit(log_da ta)
params = (a, b, mu, sigma)

#Aplicacion del test de K-S para corroboar que el fit es bueno
kstest = scipy.stats.kstest(log_data, 'johnsonsu', params)
m = len(log_data)
critical_value = 1.358 / np.sqrt(m)
#Con lo anterior da que es un buen ajuste con un valor de significacion del 5
#por ciento
