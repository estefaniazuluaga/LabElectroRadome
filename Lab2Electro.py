import numpy as np
import scipy.constants as sc
from matplotlib import pyplot as plt

# Definición de variables
Npts = 300    # Número de puntos
pc = 3        # Punto en el que se aplicará la onda electromagnética 
Ez = np.zeros((1,Npts),dtype=float) # Creación de vector de ceros para el campo eléctrico
Hy = np.zeros((1,Npts),dtype=float) # Creación de vector de ceros para el campo magnético

ei = np.zeros((1,Npts),dtype=float) # Creación de vector de ceros para el epsilon inicial (sería el relativo)
# Con ayuda de la librería obtenemos las constantes y se multiplican por cada epsilon (cambia según medio)
ei[0, 0: 50]=sc.epsilon_0  # medio: vacío
ei[0, 50: 87]=sc.epsilon_0 * 2 # medio: película
ei[0, 87: 215]=sc.epsilon_0 * 12 # medio: radome
ei[0, 215: 242]=sc.epsilon_0 * 2 # medio: película
ei[0, 242: 300]=sc.epsilon_0  # medio: vacío

ui = np.zeros((1,Npts),dtype=float) # Creación de vector de ceros mara mu
ui[0, 0: 300]=sc.mu_0

dx = 0.1e-3  # Distancia de paso 
dt = dx / 3e8  # Paso de tiempo

E0 = 1.0 # Magnitud de camapo

a=0
b=0
f = 10.5e9 # Frecuencia: 10.5GHz

x = np.linspace(0, Npts, num=Npts) * dx
Ez = np.zeros((1,Npts),dtype=float)
Hy = np.zeros((1,Npts),dtype=float)

Ez[0,pc] = E0 * np.sin(0) 
y = Ez[0,:]

plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
line1, = ax.plot(x, y, 'r-')
ax.axvline(x=51*dx, color='b')
ax.axvline(x=88*dx,color='c')
ax.axvline(x=216*dx,color='c')
ax.axvline(x=252*dx, color='b')
ax.set_xlim(0,300 * dx)
ax.set_ylim(-1.5,1.5)
ax.set_ylabel('Electric Field(V/m)')
ax.set_xlabel('Posición x(m)')
# Aplicación del FDTD
for i in range(0, 750):
    # Cálculo de campo magnético
    for j in range(0,(Npts-1)):
        Hy[0,j]=Hy[0,j]+(dt/(ui[0,j]*dx))*(Ez[0,j+1]-Ez[0,j])
    # Cálculo de campo eléctrico
    for k in range(1,Npts):
        Ez[0,k]=Ez[0,k]+(dt/(ei[0,k]*dx))*(Hy[0,k]-Hy[0,k-1])
    # Onda que se va a propagar
    Ez[0,pc] = E0 * np.sin(2*np.pi*10*f*dt*i)

    line1.set_ydata(Ez[0,:])
    fig.canvas.draw()
    fig.canvas.flush_events()

