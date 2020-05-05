# set number of seeds
SEEDS=$(seq 0 3)
JAVA_ARGS="-cp MOEAFramework-2.9-Demo.jar"

# .set files need to add three lines to the top of the file to describe the problem (for MOEAFramework to recognize)
sed -i '1i # Objectives = 3' blog_sets/*.set
sed -i '1i # Variables = 12' blog_sets/*.set
sed -i '1i # Problem = DTLZ2' blog_sets/*.set

# .set files also need a # at the end for MOEA framework to recognize
for SEED in ${SEEDS}
do
	echo "#" >> sets/DTLZ2_S${SEED}.set
done

# Find the reference set with DVs using the MOEAFramework
#java -cp MOEAFramework-2.9-Demo.jar org.moeaframework.analysis.sensitivity.ResultFileMerger -r blog_sets/* -o sets/ComoTestDVs.reference -e 0.01,0.01,0.01 -d 3 -v 12

# create a reference set file without DVs (for runtime diagnostics)
java -cp MOEAFramework-2.9-Demo.jar org.moeaframework.analysis.sensitivity.ResultFileSeedMerger sets/*.set -o sets/DTLZ2.reference -e 0.05,0.05,0.05 -d 3

# calc runtime metrics with the calc_runtime_metrics.sh script
# (THIS WILL SUBMIT 6 JOBS INTO THE QUEUE!)
for SEED in ${SEEDS}
do
SLURM="#!/bin/bash\n\
#SBATCH --nodes=1\n\
#SBATCH --ntasks-per-node=1\n\
#SBATCH --export=ALL\n\
#SBATCH -t 2:00:00\n\
#SBATCH --job-name=calc_metrics_DTLZ2_S${SEED}\n\
#SBATCH --output=metrics_info_DTLZ2_S${SEED}.out\n\
#SBATCH --error=metrics_info_DTLZ2_S${SEED}.error\n\

./calc_runtime_metrics.sh ${SEED}"

echo -e $SLURM | sbatch
sleep 0.5
done