from matplotlib import pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import numpy as np
from celluloid import Camera
from runtime_visualization_functions import *
import matplotlib.animation as animation
import seaborn as sns
sns.set(style='whitegrid')

"""

Plots a runtime diagnostic dashboard and dynamic runtime metrics
for the DTLZ2 test problem run with the Borg MOEA

By: D. Gold
Date: 5/20

"""

# load the runtime file
runtime_file = 'exampleDataDTLZ2_S0.runtime'
reference_set = np.loadtxt('exampleData/DTLZ2.reference', delimiter=' ', skiprows=3)
seed0 = read_runtime(runtime_file, 5000, 25, 3)
objs = seed0['Objectives']


# load runtime metrics
metrics_file = 'exampleData/DTLZ2_S0.metrics'
metrics = np.loadtxt(metrics_file, delimiter=' ', skiprows=1)
# load metrics (and normalize HV)
HV = metrics[:,0]/.48
gd = metrics[:,1]
epsI = metrics[:,4]

################### Diagnostic Dashboard ##############################


# create the figure object to store subplots
fig = plt.figure(figsize=(12,12))
gs = fig.add_gridspec(5,2)

# information axis
text_ax = fig.add_subplot(gs[0:2, 0])

# 3D scatter axis
scatter_ax = fig.add_subplot(gs[0:2,1],projection='3d')

# parallel axis plot axis
px_ax = fig.add_subplot(gs[2,:])

# HV axis
HV_ax = fig.add_subplot(gs[3,:])

# operator probabilities
op_ax = fig.add_subplot(gs[4,:])

# set up camera for animation
camera = Camera(fig)


# loop through runtime snapshots and plot data
# capture each with camera
for i in range(0, len(seed0['NFE'])):
	plot_text(text_ax, 'DTLZ2', 3, 25, i)
	plot_3Dscatter(scatter_ax, objs, i)
	plot_operators(op_ax, seed0, 5000, i)
	plot_metric(HV_ax, HV, "Hypervolume", seed0['NFE'], len(seed0['NFE'])*25, 1, i)
	plot_paxis(px_ax, objs, i)
	fig.tight_layout()
	camera.snap()

# use Celluloid to stitch animation
animation=camera.animate()

animation.save('DTLZ2_runtime.gif', writer='PillowWriter')

################### Metrics dashboard ##############################

# create the figure object to store subplots
fig2 = plt.figure(figsize=(10,8))
gs = fig2.add_gridspec(3,1)

HV_ax = fig2.add_subplot(gs[0,0])
gd_ax = fig2.add_subplot(gs[1,0])
eps_ax = fig2.add_subplot(gs[2,0])


# set up camera for animation
camera2 = Camera(fig2)

# loop through runtime snapshots and plot data
# capture each with camera
for i in range(0, len(seed0['NFE'])):
	plot_metric(HV_ax, HV, "Hypervolume", seed0['NFE'], len(seed0['NFE'])*25, 1, i)
	plot_metric(gd_ax, gd, "Generational Distance", seed0['NFE'], len(seed0['NFE'])*25, .2, i)
	plot_metric(eps_ax, epsI, "Addative Epsilon Indicator", seed0['NFE'], len(seed0['NFE'])*25, .75, i)
	fig2.tight_layout()
	camera2.snap()

# use Celluloid to stitch animation
animation2=camera2.animate()
animation2.save('DTLZ2_metrics.gif', writer='PillowWriter')


