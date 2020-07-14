import numpy as np
from matplotlib import pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
from yellowbrick.features import RadViz
from yellowbrick.features import Manifold


def plot_paxis(ax, objs, obj_names):
    """
    Plots a parallel axis plot of objectives
    Parameter ax: a Matplotlib subplot
    Parameter objs: a numpy array of objectives
    Parameter i: snapshot number
    """

    for j in range(len(objs[:,0])):
        ys = objs[j,:]
        xs = range(len(ys))
        ax.plot(xs, ys, c='b', alpha=.8, linewidth=.5)

    ax.set_ylabel('Objective Value  \n Preference $\longleftarrow$', size=12)
    ax.set_ylim([0,1])
    ax.set_xticks(np.arange(len(obj_names)))
    ax.set_xticklabels(obj_names, fontsize=12)
    ax.set_xlim([0, len(objs[0,:])-1])


def animate_scatters(iteration, objectives, scatters):
    for i in range(0, len(objectives)):
        scatters[i]._offsets3d = (objectives[iteration][:,0], 
                objectives[iteration][:,1], objectives[iteration][:,2])
    
    return scatters


def animate_operators(i, runtime, SBX, DE, PCX, SPX, UNDX, UM):
    SBX.set_data(runtime['NFE'][:i], runtime['SBX'][:i])  # update the data.
    SBX.axes.axis([0, 10000, 0, 1])
    DE.set_data(runtime['NFE'][:i], runtime['DE'][:i])  # update the data.
    DE.axes.axis([0, 10000, 0, 1])
    PCX.set_data(runtime['NFE'][:i], runtime['PCX'][:i])  # update the data.
    PCX.axes.axis([0, 10000, 0, 1])
    SPX.set_data(runtime['NFE'][:i], runtime['SPX'][:i])  # update the data.
    SPX.axes.axis([0, 10000, 0, 1])
    UNDX.set_data(runtime['NFE'][:i], runtime['UNDX'][:i])  # update the data.
    UNDX.axes.axis([0, 10000, 0, 1])
    UM.set_data(runtime['NFE'][:i], runtime['UM'][:i])  # update the data.
    UM.axes.axis([0, 10000, 0, 1])
    
    return SBX, DE, PCX, SPX, UNDX, UM


def animate_test(i, runtime, SBX, DE):
    SBX.set_data(runtime['NFE'][:i], runtime['SBX'][:i])  # update the data.
    SBX.axes.axis([0, 10000, 0, 1])
    DE.set_data(runtime['NFE'][:i], runtime['DE'][:i])  # update the data.
    DE.axes.axis([0, 10000, 0, 1])
    
    return SBX, DE


def animate_HV(i, HV, HV_plot, NFE, dummy_plot):
    HV_plot.set_data(NFE[:i], HV[:i])
    HV_plot.axes.axis([0, 10000, 0, 1])
    dummy_plot.set_data([],[])
    
    return HV_plot, dummy_plot


def plot_ref_set(ref_set):
    fig = plt.figure()
    ax= p3.Axes3D(fig)
    ax.view_init(25, 10)
    ax.set_xlabel('Obj 1 $\longrightarrow$')
    ax.set_ylabel('$\longleftarrow$ Obj 2')
    ax.set_zlabel('Obj 3 $\longrightarrow$')
    ax.view_init(25, 10)
    ax.set_xlim([0,2])
    ax.set_ylim([0,2])
    ax.set_zlim([0,2])
    ax.scatter(ref_set[:,0],ref_set[:,1], ref_set[:,2], EdgeColor='b',
                       LineWidth=.5)
    plt.savefig('reference_set.png')
    
    
def plot_Radvis(objectives, ax, name):
    class_dummy = np.zeros(len(objectives))
    visualizer = RadViz(classes=[name], ax=ax, alpha=.75)
    visualizer.fit(objectives, class_dummy)
    visualizer.show()

def plot_MDS(objectives, ax, name):
    class_dummy = np.zeros(len(objectives))
    visualizer = Manifold(manifold='mds', classes=[name], ax=ax)
    visualizer.fit_transform(objectives, class_dummy)
    visualizer.show()

def plot_IsoMap(objectives, n_neighbors, ax, name):
    class_dummy = np.zeros(len(objectives))
    visualizer = Manifold(manifold='isomap', n_neighbors=n_neighbors,
    classes=[name], ax=ax)
    visualizer.fit_transform(objectives, class_dummy)
    visualizer.show()