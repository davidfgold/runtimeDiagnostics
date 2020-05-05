#/bin/bash

SEED=$1

JAVA_ARGS="-cp MOEAFramework-2.9-Demo.jar"
java ${JAVA_ARGS} org.moeaframework.analysis.sensitivity.ResultFileEvaluator -d 3 -i runtime/DTLZ2_S${SEED}.runtime -r sets/DTLZ2.reference -o DTLZ2_S${SEED}.metrics

