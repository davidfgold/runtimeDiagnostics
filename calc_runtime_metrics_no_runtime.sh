#/bin/bash

FORM=$1
NFE=$2

JAVA_ARGS="-cp MOEAFramework-2.13-Demo.jar"
java ${JAVA_ARGS} org.moeaframework.analysis.sensitivity.ResultFileEvaluator -d 6 -r runtimeDiagnostics/F${FORM}_N${NFE}_set.reference -o Triangle_F${FORM}_N${NFE}.metrics

