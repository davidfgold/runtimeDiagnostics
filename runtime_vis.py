'''

To do:
    1. extract runtime files by NFE
    2. Create a function to make a 3D scatter plot for each snapshot
    3. animate the function (see other example)
    4. Add hypervolume as a second subplot
    5. Create a function to plot tradeoffs at each snapshot (p-axis)
    6. Add a Radvis (or other) As forth?
    7. Track operator probabilities?

'''

from matplotlib import pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
from runtime_visualization_functions import *
import matplotlib.animation as animation
import numpy as np
import seaborn as sns
sns.set(style='whitegrid')


# read runtime file        
file = 'DTLZ2_S0.runtime'
seed0 = read_runtime(file, 10000, 100, 3)


# create 3D scatter animation
fig = plt.figure()
ax1 = fig.add_subplot(3, 2, 1, projection='3d')
#ax= p3.Axes3D(fig)
ax1.view_init(25, 10)
ax1.set_xlabel('Obj 1 $\longrightarrow$')
ax1.set_ylabel('$\longleftarrow$ Obj 2')
ax1.set_zlabel('Obj 3 $\longrightarrow$')

generations = seed0['NFE']
objs = seed0['Objectives']
scatters = [ax1.scatter(objs[i][:,0], objs[i][:,1], objs[i][:,2], EdgeColor='b',
                       LineWidth=.5) for i in range(0, len(generations))]
iterations = len(objs)
scatter_ani = animation.FuncAnimation(fig, animate_scatters, 50, fargs=(objs, scatters),
                                   interval=600, blit=True, repeat=True)
#scatter_ani.save('test_subplots.gif', writer='PillowWriter')


# plot the operator dynamics

ax2 = fig.add_subplot(3, 2, 2)
SBX, = ax2.plot(seed0['NFE'], seed0['SBX'])
DE, = ax2.plot(seed0['NFE'], seed0['DE'])
PCX, = ax2.plot(seed0['NFE'], seed0['PCX'])
SPX, = ax2.plot(seed0['NFE'], seed0['SPX'])
UNDX, = ax2.plot(seed0['NFE'], seed0['UNDX'])
UM, = ax2.plot(seed0['NFE'], seed0['UM'])

operators_ani = animation.FuncAnimation(fig, animate_operators, len(seed0['NFE']), 
                                fargs=[seed0, SBX, DE, PCX, SPX, UNDX, UM],
                                interval=600, blit=True)

operators_ani.save('test_subplots.gif', writer='PillowWriter')




'''
# create 3D scatter animation
fig = plt.figure()
ax= p3.Axes3D(fig)
ax.view_init(25, 10)
ax.set_xlabel('Obj 1 $\longrightarrow$')
ax.set_ylabel('$\longleftarrow$ Obj 2')
ax.set_zlabel('Obj 3 $\longrightarrow$')

generations = seed0['NFE']
objs = seed0['Objectives']
scatters = [ax.scatter(objs[i][:,0], objs[i][:,1], objs[i][:,2], EdgeColor='b',
                       LineWidth=.5) for i in range(0, len(generations))]
iterations = len(objs)
scatter_ani = animation.FuncAnimation(fig, animate_scatters, 50, fargs=(objs, scatters),
                                   interval=600, blit=True, repeat=True)
scatter_ani.save('test_scatter.gif', writer='PillowWriter')


# plot the operator dynamics
fig, ax = plt.subplots()
SBX, = ax.plot(seed0['NFE'], seed0['SBX'])
DE, = ax.plot(seed0['NFE'], seed0['DE'])
PCX, = ax.plot(seed0['NFE'], seed0['PCX'])
SPX, = ax.plot(seed0['NFE'], seed0['SPX'])
UNDX, = ax.plot(seed0['NFE'], seed0['UNDX'])
UM, = ax.plot(seed0['NFE'], seed0['UM'])

operators_ani = animation.FuncAnimation(fig, animate_operators, len(seed0['NFE']), 
                                fargs=[seed0, SBX, DE, PCX, SPX, UNDX, UM],
                                interval=600, blit=True)

operators_ani.save('test_line.gif', writer='PillowWriter')



fig, ax = plt.subplots()
SBX, = ax.plot(seed0['NFE'], seed0['SBX'])
DE, = ax.plot(seed0['NFE'], seed0['DE'])


operators_test = animation.FuncAnimation(fig, animate_test, len(seed0['NFE']), 
                                fargs=[seed0, SBX, DE],
                                interval=600, blit=True)


# animate HV
metrics_file = 'DTLZ2_S0.metrics'
metrics = np.loadtxt(metrics_file, delimiter=' ', skiprows=1)

HV = metrics[:,0]/.48
NFE = seed0['NFE']

fig, ax = plt.subplots()
HV_plot, = ax.plot(NFE, HV)
dummy_plot, = ax.plot(NFE, HV)

HV_ani = animation.FuncAnimation(fig, animate_HV, len(seed0['NFE']), 
                                fargs=[HV, HV_plot, NFE, dummy_plot],
                                interval=600, blit=True)

HV_ani.save('test_HV.gif', writer='PillowWriter')


reference_set = np.loadtxt('DTLZ2.reference', delimiter=' ', skiprows=3)

plot_ref_set(reference_set)

'''

















