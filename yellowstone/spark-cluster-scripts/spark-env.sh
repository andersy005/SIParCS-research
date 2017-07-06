#!/usr/bin/env bash

source /etc/profile.d/modules.sh

module restore system
module swap intel gnu/5.3.0
module load java
module load python all-python-libs
module load h5py

export SPARK_WORKER_DIR=/glade/scratch/$USER/spark/work
export SPARK_LOG_DIR=/glade/scratch/$USER/spark/logs
export SPARK_LOCAL_DIRS=/glade/scratch/$USER/spark/temp
export SPARK_LOCAL_IP=$(sed -e 's/\([^.]*\).*$/\1-ib/' <<< $(hostname))


