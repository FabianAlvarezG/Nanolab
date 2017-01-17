import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize
from scipy.signal import argrelextrema
import heapq

cali = .02
piezospeed = 200.0


scan= 'C60 COOH/Gold/Gold/16-20/scan170111_59_111.dat'

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

# intento de encontrar el intervalo ideal
#para cada Fiteo
def find_delta(dist,cond):
    '''encuentra bla bla bla'''
    epsilon = 20
    mean_max_loc = []
    std_max_loc = []
    maximos = []
    n = len(cond) / epsilon
    m = len(cond)
    for i in range(n):
        cond_r = cond[m - (i + 1) * epsilon: m - i * epsilon ]
        max_loc = cond_r[argrelextrema(cond_r, np.greater)[0]]
        #prom = np.mean(max_loc)
        #std = np.std(max_loc)
        #mean_max_loc = np.append(mean_max_loc,prom)
        #std_max_loc = np.append(std_max_loc,std)
        maximos = np.append(maximos,max_loc)
    return maximos

maximos = find_delta(dist,cond)
log_maximos = np.log10(maximos)
#print log_maximos
# se procede a eliminar los NaN de la lista porque no son representativos

cleanedList = log_maximos[~np.isnan(log_maximos)] # en escala log
plt.hist(cleanedList)
plt.title("Histograma delos maximos locales")
plt.xlabel("Valor")
plt.ylabel("Frecuencia")
plt.show()


print cleanedList

hist , bins = np.histogram(cleanedList,10)


print '* * * * * * * * * * *'
print hist
print '- - - - - - - - - - - - - -'
print 'limites de los intervalos:'
print bins
print '* * * * * * * * * * *'
#el valor con mayor frecuencia "representaria" un BG,
#lurgo se quiere encontrar el segundo valor mas alto
#para atribuirselo al ruido
index_sort = heapq.nlargest(10, xrange(len(hist)), key=hist.__getitem__)
sort_hist = heapq.nlargest(10, hist)
print '* * * * * * * * * * *'
print sort_hist # entrega las frecuencias de mayor a menor
print '- - - - - - - - - - - - - -'
print'indices del intervalo en que se encuentran las frecuencias ordenadas de mayor a menor'
print index_sort # entrega el indice de las barras ordenadas de mayor a menor
print '* * * * * * * * * * *'

noise_freq = sort_hist[1] #obtener segunda mejor frecuencia
noise_index = index_sort[1] #y su indice
print '* * * * * * * * * * *'
print 'segunda mejor frecuencia, que corresponde al ruido'
print noise_freq
print '- - - - - - - - - - - - - -'
print 'indice de la barra en el que se encuetra el ruido en el histograma'
print noise_index
print '* * * * * * * * * * *'


#con esto se obtiene la cota inferior del intervalo del ruido (en bins[noise_index])
# y la cota superior esta dada por el bins[(noise_index + 1)]

lim_sup = bins[noise_index + 1]
lim_inf = bins[noise_index ]
print '* * * * * * * * * * *'
print 'limite inferior del ruido (conductancia) :' + str(lim_inf)
print 'limite inferior del ruido (conductancia) :' + str(lim_sup)
print '* * * * * * * * * * *'
                                                                                                                            #ahora se sabe donde buscar en las maximas conductancias y se puede hacer un
# histograma que sea mas representativo
noise_log_maximos = []
for i in log_maximos:
    if(i <= lim_sup and i >= lim_inf):
        noise_log_maximos = np.append(noise_log_maximos, i )

noise_hist , noise_bins = np.histogram(noise_log_maximos,50)
plt.hist(noise_log_maximos,bins = 50)
plt.title("histograma del ruido")
plt.xlabel("conductancia")
plt.ylabel("frecuencia")
plt.show()

index_sort_noise = heapq.nlargest(10, xrange(len(noise_hist)), key=noise_hist.__getitem__)
sort_hist_noise = heapq.nlargest(10, noise_hist)
print '* * * * * * * * * * *'
print sort_hist_noise # entrega las frecuencias de mayor a menor
print '- - - - - - - - - - - - - -'
print'indices del intervalo en que se encuentran las frecuencias ordenadas de mayor a menor'
print index_sort_noise# entrega el indice de las barras ordenadas de mayor a menor
print '* * * * * * * * * * *'

"""= []
for i in range(len(sort_hist_noise)):
    if i == 0:
        pass
    else:
        if sort_hist_noise[i] == sort_hist_noise[0]:

cota = np.mean(frequently)
print cota

"""
               
