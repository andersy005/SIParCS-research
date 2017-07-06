#!/usr/bin/env bash

source ~/yellowstone/spark/spark-cluster-scripts/spark-cluster.sh start

$SPARK_HOME/bin/pyspark --master $MASTER