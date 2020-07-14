from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from visualization_functions import *
import seaborn as sns
from sammon import sammon
from minisom import MiniSom
from matplotlib.patches import RegularPolygon, Ellipse
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib import cm, colorbar
from sklearn.decomposition import PCA
sns.set(style='whitegrid')
setFolder = ''

#################################################################################
# load and scale the data to 0-1

DTLZ2_4D_PSet = np.loadtxt('pFronts\DTLZ2_4D.pf', delimiter=' ')
DTLZ7_4D_PSet = np.loadtxt('pFronts\DTLZ7_4D.pf', delimiter=' ')

pSets =[DTLZ2_4D_PSet, DTLZ7_4D_PSet]

# normalize the pSet
for pSet in pSets:
    for i in range(0,4):
        pSet[:,i] = (pSet[:,i]-min(pSet[:,i]))/(max(pSet[:,i])-min(pSet[:,i]))

#################################################################################
# plot p-coords

fig = plt.figure(figsize= (16,10))

# DTLZ 2
ax = fig.add_subplot(2,1,1)
plot_paxis(ax, DTLZ2_4D_PSet, ['Obj 1', 'Obj 2', 'Obj 3', 'Obj 4'])
ax.set_title('Four objective DTLZ 2')

# DTLZ 7
ax0= fig.add_subplot(2,1,2)
plot_paxis(ax0, DTLZ7_4D_PSet, ['Obj 1', 'Obj 2', 'Obj 3', 'Obj 4'])
ax0.set_title('Four objective DTLZ 7')

plt.savefig('Paxes.png', bbox_inches='tight')


#################################################################################
# MDS

# set up the figure
fig1 = plt.figure(figsize=(12,5))

# DTLZ 2
ax1 = fig1.add_subplot(1,2,1)
plot_MDS(DTLZ2_4D_PSet, ax1, '')
ax1.set_title('MDS: 4 Obj DTLZ 2')
ax1.set_xlabel('')

ax2 = fig1.add_subplot(1,2,2)
plot_MDS(DTLZ7_4D_PSet, ax2, '')
ax2.set_title('MDS: 4 Obj DTLZ 7')
ax2.set_xlabel('')

plt.savefig('4ObjMDS.png', bbox_inches='tight')

# Isomapping

# set up the figure
fig2 = plt.figure(figsize=(12,5))

ax3 = fig2.add_subplot(1,2,1)
plot_IsoMap(DTLZ2_4D_PSet, 12, ax3, '')
ax3.set_title('IsoMap: 4 Obj DTLZ 2')
ax3.set_xlabel('')

ax4 = fig2.add_subplot(1,2,2)
plot_IsoMap(DTLZ7_4D_PSet, 30, ax4, '')
ax4.set_title('IsoMap: 4 Obj DTLZ 7')
ax4.set_xlabel('')

plt.savefig('4ObjIsoMap.png', bbox_inches='tight')


#################################################################################
# Sammon Mapping

fig3 = plt.figure(figsize=(12,5))

ax5 = fig3.add_subplot(1,2,1)
sammon_DTLZ2 = sammon(DTLZ2_4D_PSet, 3)
ax5.scatter(sammon_DTLZ2[0][:,0], sammon_DTLZ2[0][:,1], 
                alpha = .7,)
ax5.set_title('Sammon: 4 Obj DTLZ 2')
ax5.set_xlabel('')

ax6 = fig3.add_subplot(1,2,2)
sammon_DTLZ7 = sammon(DTLZ7_4D_PSet, 2)
ax6.scatter(sammon_DTLZ7[0][:,0], sammon_DTLZ7[0][:,1], 
                alpha = .7,)
ax6.set_title('Sammon: 4 Obj DTLZ 7')
ax6.set_xlabel('')

plt.savefig('4ObjSammon.png', bbox_inches='tight')






# Self Organizing Maps

#################################################################################
# SOM

# Initialization and training
SOM_DTLZ2 = MiniSom(15, 15, 4, sigma=1.5, learning_rate=.7, 
                activation_distance='euclidean',
                topology='hexagonal', neighborhood_function='gaussian', 
                random_seed=10)

SOM_DTLZ2.train_batch(DTLZ2_4D_PSet, 1000, verbose=True)

SOM_DTLZ7 = MiniSom(15, 15, 4, sigma=1.5, learning_rate=.7, 
                  activation_distance='euclidean',
                  topology='hexagonal', neighborhood_function='gaussian', 
                  random_seed=10)

SOM_DTLZ7.train_batch(DTLZ7_4D_PSet, 1000, verbose=True)



# plotting
fig = plt.figure(figsize=(14,6))
gspec = fig.add_gridspec(ncols=4, nrows=1, height_ratios = [1], 
                            width_ratios=[1, 0.075, 1, 0.075])


ax7 = fig.add_subplot(gspec[0,0])
xx, yy = SOM_DTLZ2.get_euclidean_coordinates()
umatrix = SOM_DTLZ2.distance_map()
weights = SOM_DTLZ2.get_weights()

for i in range(weights.shape[0]):
    for j in range(weights.shape[1]):
        
        wy = yy[(i, j)]*2/np.sqrt(3)*3/4
        
        hex = RegularPolygon((xx[(i, j)], wy), numVertices=6, 
                                radius=.95/np.sqrt(3), 
                                facecolor=cm.Greens(umatrix[i, j]), 
                                alpha=.8, edgecolor='gray')
        ax7.add_patch(hex)
ax7.set_xlim([-1,14])
ax7.set_ylim([-1,13])
ax7.set_title('SOM: 4 Obj DTLZ 2')

ax_cb = fig.add_subplot(gspec[0,1])   
cb1 = colorbar.ColorbarBase(ax_cb, cmap=cm.Greens, 
                            orientation='vertical', alpha=.4)
cb1.ax.get_yaxis().set_ticks_position('left')
cb1.ax.get_yaxis().set_label_position('left')
cb1.ax.get_yaxis().labelpad = 12
cb1.ax.set_ylabel('Distance from neurons in the neighbourhood',
                    rotation=90, fontsize=12)




ax8 = fig.add_subplot(gspec[0,2])
xx, yy = SOM_DTLZ7.get_euclidean_coordinates()
umatrix = SOM_DTLZ7.distance_map()
weights = SOM_DTLZ7.get_weights()

for i in range(weights.shape[0]):
    for j in range(weights.shape[1]):
        
        wy = yy[(i, j)]*2/np.sqrt(3)*3/4
        
        hex = RegularPolygon((xx[(i, j)], wy), numVertices=6, 
                                radius=.95/np.sqrt(3), 
                                facecolor=cm.Blues(umatrix[i, j]), 
                                alpha=.8, edgecolor='gray')
        ax8.add_patch(hex)
ax8.set_xlim([-1,14])
ax8.set_ylim([-1,13])
ax8.set_title('SOM: 4 Obj DTLZ 7')

ax_cb2 = fig.add_subplot(gspec[0,3])   
cb2 = colorbar.ColorbarBase(ax_cb2, cmap=cm.Blues, 
                            orientation='vertical', alpha=.4)
cb2.ax.get_yaxis().set_ticks_position('left')
cb2.ax.get_yaxis().set_label_position('left')                             
cb2.ax.get_yaxis().labelpad = 12
cb2.ax.set_ylabel('Distance from neurons in the neighbourhood',
                    rotation=90, fontsize=12)

plt.tight_layout()

# save the figure
plt.savefig('4DSOMs.png', bbox_inches='tight')





#########################################################################


# set up the figure
pSet = np.loadtxt('pFronts\DTLZ7_6D.pf', delimiter=' ')
fig = plt.figure(figsize=(12,10))
gspec = fig.add_gridspec(ncols=3, nrows=2, height_ratios = [1,1], 
                            width_ratios=[1, 1, 0.05])
    
# create MDS
ax1 = fig.add_subplot(gspec[0,0])
plot_MDS(pSet, ax1, '')
ax1.set_title('MDS')
ax1.set_xlabel('')

# create Isomap
ax2 = fig.add_subplot(gspec[0,1])
plot_IsoMap(pSet, 80, ax2, '')
ax2.set_title('IsoMap')
ax2.set_xlabel('')

# Sammon mapping
ax3 = fig.add_subplot(gspec[1,0])
sammon_proj = sammon(pSet, 2)
ax3.scatter(sammon_proj[0][:,0], sammon_proj[0][:,1], 
            alpha = .7,)
ax3.set_title('Sammon Map')
    


# SOM
# Initialization and training
som = MiniSom(25, 25, 6, sigma=3, learning_rate=.7, 
                activation_distance='euclidean',
                topology='hexagonal', neighborhood_function='gaussian', 
                random_seed=10)

som.train_batch(pSet, 1000, verbose=True)

# plotting
ax4 = fig.add_subplot(gspec[1,1])
xx, yy = som.get_euclidean_coordinates()
umatrix = som.distance_map()
weights = som.get_weights()

for i in range(weights.shape[0]):
    for j in range(weights.shape[1]):
        
        wy = yy[(i, j)]*2/np.sqrt(3)*3/4
        
        hex = RegularPolygon((xx[(i, j)], wy), numVertices=6, 
                                radius=.95/np.sqrt(3), 
                                facecolor=cm.Blues(umatrix[i, j]), 
                                alpha=.8, edgecolor='gray')
        ax4.add_patch(hex)
ax4.set_xlim([-1,22])
ax4.set_ylim([-1,20])
ax4.set_title('SOM')

ax_cb = fig.add_subplot(gspec[1,2])   
cb1 = colorbar.ColorbarBase(ax_cb, cmap=cm.Blues, 
                            orientation='vertical', alpha=.4)
cb1.ax.get_yaxis().labelpad = 16
cb1.ax.set_ylabel('Distance from neurons in the neighbourhood',
                    rotation=270, fontsize=12)


plt.tight_layout()

# save the figure
plt.savefig('6_dimensional_transformations.png', bbox_inches='tight')


def hide_current_axis(*args, **kwds):
    plt.gca().set_visible(False)    

g = sns.pairplot(pd.DataFrame(Viennet3, columns = ['Obj1', 'Obj 2', 'Obj 3', 'Obj 4']))
g.map_upper(hide_current_axis)
plt.savefig('DTLZ2_4D_pairwise.png', bbox_inches = 'tight')


