#/bin/bash

FORM=$1
NFE=$2

JAVA_ARGS="-cp MOEAFramework-2.13-Demo.jar"
java ${JAVA_ARGS} org.moeaframework.analysis.sensitivity.ResultFileEvaluator -d 6 -i WaterPaths/output/*S${FORM}_N${NFE}*.runtime -r runtimeDiagnostics/F${FORM}_N${NFE}_set.reference -o Triangle_F${FORM}_N${NFE}.metrics

