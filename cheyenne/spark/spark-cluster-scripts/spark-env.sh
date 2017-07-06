#!/usr/bin/env bash

source /etc/profile.d/modules.sh

module restore system
module swap intel gnu
export MODULEPATH=/glade/p/work/bdobbins/Modules:${MODULEPATH}
module load java
ml python
ml numpy
ml jupyter
ml scipy
ml h5py
ml bottleneck
ml numexpr
ml pandas
ml pyside
ml matplotlib
ml pyngl
ml scikit-learn
ml netcdf4-python
ml cf_units
ml xarray

export SPARK_WORKER_DIR=/glade/scratch/$USER/spark/work
export SPARK_LOG_DIR=/glade/scratch/$USER/spark/logs
export SPARK_LOCAL_DIRS=/glade/scratch/$USER/spark/temp
export SPARK_LOCAL_IP=$(sed -e 's/\([^.]*\).*$/\1/' <<< $(hostname))

