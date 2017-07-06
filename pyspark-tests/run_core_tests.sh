#!/usr/bin/env bash

#PBS -A PROJECT_CODE
#PBS -N spark-core-test
#PBS -j oe
#PBS -m abe
#PBS -M email_address
#PBS -q economy
#PBS -l walltime=20:00
#PBS -l select=1:ncpus=4:mpiprocs=4

source ~/cheyenne/spark/spark-cluster-scripts/spark-cluster.sh start
$SPARK_HOME/bin/spark-submit --master $MASTER /glade/u/home/abanihi/PySpark4Climate/pyspark-tests/core_tests.py --all -a --num-records 1000000000 --num-partitions 20000

