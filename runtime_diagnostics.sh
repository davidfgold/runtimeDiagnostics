# Aug 2020: D Gorelick adjustments to run different formulations 
# (one seed, one island each) of WJLWTP model tests
# because Borg output is stored in different WaterPaths sub-folder
# this shell script should be run from the parent folder of where
# it is stored (AGUmodel2019) 
 
FORMULATIONS=$(seq 0 2)
JAVA_ARGS="MOEAFramework-2.13-Demo.jar"
NFE=3000

# print current directory to see what's happening
echo $PWD

# .set files need to add three lines to the top of the file to describe the problem (for MOEAFramework to recognize)
for F in ${FORMULATIONS}
do
	sed -i '1i # Objectives = 6' WaterPaths/output/*S${F}_N${NFE}.set
	sed -i '1i # Variables = 70' WaterPaths/output/*S${F}_N${NFE}.set
	sed -i "1i # Problem = triangleSimulation_F${F}" WaterPaths/output/*S${F}_N${NFE}.set

	# set files also need a hash at the end for MOEA to recognize
	echo "#" >> WaterPaths/output/*S${F}_N${NFE}.set

	# create a reference set file without DVs (for runtime diagnostics)
	java -cp ${JAVA_ARGS} org.moeaframework.analysis.sensitivity.ResultFileSeedMerger WaterPaths/output/*S${F}_N${NFE}.set -o runtimeDiagnostics/F${F}_N${NFE}_set.reference -e 0.01,0.02,5,0.02,0.04,0.01 -d 6

	# calculate runtime metrics via submission of calc_runtime_metrics.sh
	SLURM="#!/bin/bash\n\
	#SBATCH --nodes=1\n\
	#SBATCH --ntasks-per-node=1\n\
	#SBATCH --export=ALL\n\
	#SBATCH -t 2:00:00\n\
	#SBATCH --job-name=calc_metrics_F${F}\n\
	#SBATCH --output=runtimeDiagnostics/metrics_info_F${F}.out\n\
	#SBATCH --error=runtimeDiagnostics/metrics_info_F${F}.error\n\

	bash runtimeDiagnostics/calc_runtime_metrics.sh ${F} ${NFE}"

	echo -e $SLURM | sbatch
	sleep 0.5

done

# create an overall reference set combining all formulations
java -cp ${JAVA_ARGS} org.moeaframework.analysis.sensitivity.ResultFileSeedMerger WaterPaths/output/*_N${NFE}.set -o runtimeDiagnostics/FAll_N${NFE}_set.reference -e 0.01,0.02,5,0.02,0.04,0.01 -d 6

# calculate overall reference set metrics
SLURM="#!/bin/bash\n\
#SBATCH --nodes=1\n\
#SBATCH --ntasks-per-node=1\n\
#SBATCH --export=ALL\n\
#SBATCH -t 2:00:00\n\
#SBATCH --job-name=calc_metrics_all\n\
#SBATCH --output=runtimeDiagnostics/metrics_info_all.out\n\
#SBATCH --error=runtimeDiagnostics/metrics_info_all.error\n\

bash runtimeDiagnostics/calc_runtime_metrics_no_runtime.sh ${F} ${NFE}"

echo -e $SLURM | sbatch

