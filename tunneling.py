import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize
import scipy.stats
import noise

cali = .02
piezospeed = 200.0
scan = 'Gold/scan170111_59_50.dat'

a, b, mu, sigma = noise.a, noise.b, noise.mu, noise.sigma
alpha = .001


# Fiteo del error

data = np.loadtxt(scan, comments='@', skiprows=10)
n = noise.indexAt(scan)
data = data[0:n, :]

cond = data[:, 1]
dist = data[:, 0]

# Se eliminan todos los datos en que la conductancia tiene valor negativo
# Porque no tiene sentido fisico
negative_index = np.where(cond <= 0)
cond = np.delete(cond, negative_index)
dist = np.delete(dist, negative_index)
# Se elimina el ruido usando la distribucion que se fitea el libreria noise.py,
# Se separan los datos cuya ocurrencia tiene probabilidad menor al 0.1 por ciento
# siguiendo la distribucion de Johnson SU
noise_index = np.where(scipy.stats.johnsonsu.cdf(
    np.log10(cond), a, b, mu, sigma) < 1 - alpha)

cond = np.delete(cond, noise_index)
dist = np.delete(dist, noise_index)

# Se eliminan todos los datos que representan cuando aun esta unida la juntura
bulk_index = np.where(cond > .5)
cond = np.delete(cond, bulk_index)
dist = np.delete(dist, bulk_index)

# Fit del tunneling


def tunneling(cond, alpha, phi):
    return np.exp(-alpha * cond + phi)

p0 = (1e-7, .6)  # Adivinanza

fit = scipy.optimize.curve_fit(tunneling, dist, cond, p0)
