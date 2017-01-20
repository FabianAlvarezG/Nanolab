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
    '''encuentra los maximos locales
       de la conductancia (lista) por
       medio de un mapeo a pequenos intervalos
       de menor a mayor conductancia
       suponiendo el comportamiento del histograma
       2D de la medicion'''
    epsilon = 100
    #mean_max_loc = []
    #std_max_loc = []
    maximos = []
    n = len(cond) / epsilon
    m = len(cond)
    for i in range(n):
        cond_r = cond[m - (i + 1) * epsilon: m - i * epsilon ] #se obtienen los mini intervalos desde atras para adelante
        #max_loc = cond_r[argrelextrema(cond_r, np.greater)[0]]
        max_loc = max(cond_r)
        # se encuentran los maximos locales de cada mini intervalo
        #prom = np.mean(max_loc)
        #std = np.std(max_loc)
        #mean_max_loc = np.append(mean_max_loc,prom)
        #std_max_loc = np.append(std_max_loc,std)
        maximos = np.append(maximos,max_loc) # se crea lista con los maximos locales de toda la conductancia
    return maximos

maximos = find_delta(dist,cond) #obtiene los maximos con raw data
log_maximos = np.log10(maximos) #se pasa a escala logaritmica
#print log_maximos
# se procede a eliminar los NaN de la lista porque no son representativos

cleanedList = log_maximos[~np.isnan(log_maximos)] # en escala log, elimina los NaN
""" HISTOGRAMA de LOS MAXIMOS LOCALES """
plt.hist(cleanedList)
plt.title("Histograma delos maximos locales")
plt.xlabel("Valor")
plt.ylabel("Frecuencia")
plt.show()
print '* * * CONDUCTANCIAS MAXIMAS (Log) * * *'
print '  '
print 'Conductancias Maximas (escala log)'
print log_maximos
print '  '
print ' =================================================='
print '  '
print 'Eliminando las conductancias maximas que son NaN'
print cleanedList
# HISTOGRAMA de los MAXIMOS LOCALES
hist , bins = np.histogram(cleanedList,10)

#bins = valores de los limites de los intervalos del HISTOGRAMA
# se quieren 10 bins por la escala logaritmica de las conductancias
# se puede apreciar esta eleccion en los exponentes de cleanedList!!! :D
#hist = frecuencias de los bins (frecuencias de ciertas conductancias )

print '* * * * * * * * * * *'
print '* * * HISTOGRAMA DE LOS MAXIMOS LOCALES * * *'
print 'frecuencias de las conductancias'
print hist
print '- - - - - - - - - - - - - -'
print 'limites de los intervalos de las conductancias:'
print bins
print '* * * * * * * * * * *'
#el valor con mayor frecuencia "representaria" un BG,
#lurgo se quiere encontrar el segundo valor mas alto
#para atribuirselo al ruido
index_sort = heapq.nlargest(10, xrange(len(hist)), key=hist.__getitem__)
sort_hist = heapq.nlargest(10, hist)
print '* * * * * * * * * * *'
print ' * * * HISTOGRAMA ORDENADO (encontrar intervalo de ruido) * * * '
print '*** frecuencias ordenadas de menor a mayor ***'
print sort_hist # entrega las frecuencias de conductancia ordenadas de mayor a menor
print '        '
print '- - - - - - - - - - - - - -'
print '        '
print'indices del intervalo en que se encuentran las frecuencias ordenadas de mayor a menor'
print index_sort # entrega el indice de las barras de conductancia ordenadas de mayor a menor
print '* * * * * * * * * * *'
print '        '
'''OBTRNER INTERVALO de MAXIMOS de RUIDO '''
noise_freq = sort_hist[1] #obtener segunda mejor frecuencia
noise_index = index_sort[1] #y su indice

print '* * * * * * * * * * *'
print 'segunda mejor frecuencia, que corresponde al ruido'
print 'noise_freq: '+ str(noise_freq)
print '        '
print '- - - - - - - - - - - - - -'
print '        '
print 'indice de la barra en el que se encuetra el ruido en el histograma'
print 'este valor debe ser el mismo que el segundo valor del indice de las conductancias  ordenadas de mayor a menor frecuencia'
print 'noise_index: ' + str(noise_index)
print '* * * * * * * * * * *'
print '        '


#con esto se obtiene la cota inferior del intervalo del ruido (en bins[noise_index])
# y la cota superior esta dada por el bins[(noise_index + 1)]

lim_sup = bins[noise_index + 1]
lim_inf = bins[noise_index ]
print '* * * * * * * * * * *'
print 'limite inferior del ruido (conductancia) :' + str(lim_inf)
print 'limite inferior del ruido (conductancia) :' + str(lim_sup)
print '* * * * * * * * * * *'
                                                                                                                            #ahora se sabe donde buscar en las maximas conductancias y se puede hacer un
# histograma que sea mas representativo del ruido, habiendo acotado los valores
# donde se encuentrauna vez encontrados lim_sup y lim_inf
noise_log_maximos = [] #aquise guardaran las maximas conductancias que podrian pertenercer al ruido

for i in log_maximos:
    if(i <= lim_sup and i >= lim_inf): #condicion de pertenencia al ruido
        noise_log_maximos = np.append(noise_log_maximos, i ) # se crea la lista
# una vez que se tiene noise_log_max, se puede hacer un histograma del ruido (maximos valores)

noise_hist , noise_bins = np.histogram(noise_log_maximos,50) # histograma max ruido

n_bins = 50 #esta variable puede ser cambiada a gusto del consumidor
plt.hist(noise_log_maximos,bins = n_bins)
plt.title("histograma del ruido")
plt.xlabel("conductancia")
plt.ylabel("frecuencia")
plt.show()

index_sort_noise = heapq.nlargest(n_bins, xrange(len(noise_hist)), key=noise_hist.__getitem__) # entrega los indices de las n mayores frecuencias( n = n_bins)
sort_hist_noise = heapq.nlargest(n_bins, noise_hist) # entrga el valor
print '* * * * * * * * * * *'
print sort_hist_noise # entrega las frecuencias de mayor a menor
print '- - - - - - - - - - - - - -'
print'indices del intervalo en que se encuentran las frecuencias ordenadas de mayor a menor'
print index_sort_noise# entrega el indice de las barras ordenadas de mayor a menor
print '* * * * * * * * * * *'

""" OBTENER LA COTA... yay! :D """
# notando que sort_hist_noise e index_sort_noise tienen la misma cantidad de elementos
# nos interesan aquellas conductancias que tienen la mayor frecuencia mientras estas sean iguales
# se quiere crear una lista que las contenga a todas y promediarlas para hacer la cota
most_frequent_noise_cond= []  # aqui guardare el valor medio de todos los intervalos mas repetidos

for i in range(len(sort_hist_noise)):
    if i == sort_hist_noise[0]: #si el primer elemento es efectivamente el primero...
        pass # no hacemos nada hehehe queteparese
    else:
        if sort_hist_noise[i] == sort_hist_noise[0]: # si la siguiente frecuencia es igual a la mayor, guardamos su indice.
        # al igual que en la parte anterior, encontraremos el lim_inf y sup de cada una para sacar su valor medio
        # recordar que con el indice podemos hacer una especie de biyeccion con los bins de esta distribucion (asi se sacan los lims )
            sup_inoise = noise_bins[i+1]
            inf_inoise = noise_bins[i]
            representative_value = -1 * np.abs(sup_inoise + inf_inoise)/ 2. #valor representativo, me aseguro que siempre sea negativo heheh
            most_frequent_noise_cond = np.append(most_frequent_noise_cond, representative_value)
"""finalmente, la cota (segun yo xD puede que este mal)"""
cota = max(most_frequent_noise_cond)
print ' '
print '* * * THE COTITAX * * *'
print cota
print '* * * * * * * * * * * *'
print '  '

cota_raw = (10 ** cota)
'GRAFICAMOS LA INFORMACION'
jeje = np.where(cond < 0)
cond = np.delete(cond, jeje)
dist = np.delete(dist, jeje)
logcond = np.log10(cond)
logdist = np.log10(dist)
plt.plot(dist, logcond, '.')
plt.ylabel("conductancia")
plt.xlabel("distancia (nm)")
plt.axhline(y = cota, xmin = dist[0], xmax= dist[len(dist)-1], linewidth=2, color = 'k')
plt.show()

""" O J O : falta graficar la recta aun hehehe me da pajita pero subo por mientras esta cosita...  los tkm """

""" IMPORTANTE: la cotitax se obtiene como un promedio de lo mas repetido pero no es rigurosamente correcto si tiene mucha dispersion
    podemos atacar el problema reduciendo la dispersion en la seleccion previa de los datos o hacer un fit con el ultimo histograma
    de todas formas es necesario que corrijan eso... esto es solo una idea """

# P A R T E   2
'''eliminamos lo que NO es RUIDO '''
cleanConductance = []
cleanDisplacement =[]
j = 1
n = len(logcond) - 1
switch = 0
delete_idx = []
for i  in range(1, n-2):
    if (logcond[i-1] > cota and logcond[i] <= cota):
        j = -1 * j
        switch = switch + 1
    elif (logcond[i-1] <= cota and logcond[i] > cota):
        j = -1 * j
        witch = switch + 1
    elif j == -1:
        delete_idx.append(i)
    if switch > 4 :
        break
logcond= np.delete(logcond,delete_idx)
dist = np.delete(dist,delete_idx )

print 'conductancias que no son RUIDO: '
print cleanConductance

""" FILTRADO graph """
plt.plot(dist,logcond, '.')
plt.xlabel(" distancia (nm) ")
plt.ylabel(" conductancias ")
plt.show ()



#se plantea ver la variacion del area bajo los puntos
