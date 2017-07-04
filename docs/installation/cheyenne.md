# Apache Spark 2.1.1 on Cheyenne
The Second task of our research project was to install the newest version of Apache Spark on Cheyenne. 

As of today (June/2017), we've been able to install the newest version of Apache Spark - [Spark 2.1.1+Hadoop2.7](https://spark.apache.org/downloads.html).

Below are the steps that we took to get Spark Up and Running on Cheyenne.

If all you need is to run the existing Apache Spark on Cheyenne, just skip to **Section 2** of this page.


## 1. Installation

### 1.1 Downloading Spark and Setting up Spark's directory and necessary files

The steps described in this section are similar to those for Yellowstone. Since both Yellowstone and Cheyenne have access to the same parallel filesytem, we decide to use the same downloaded Spark binaries.

The following section gives details on how Apache Spark would be installed on Cheyenne.

1. Log into Cheyenne
2. Change working directory to ```/glade/p/work/abanihi```
    - ```cd /glade/p/work/abanihi/```
3. Go to [Apache Spark's official website](https://spark.apache.org/downloads.html) and follow steps 1-4 to get a download link for Spark. Copy the download link and 

4. Go to ```/glade/p/work/abanihi/``` and download Spark
    - ```wget https://d3kbcqa49mib13.cloudfront.net/spark-2.1.1-bin-hadoop2.7.tgz```
    - Untar ```spark-2.1.1-bin-hadoop2.7.tgz``` with 
        - ```tar -xzf spark-2.1.1-bin-hadoop2.7.tgz```

5. Change directory to ```spark-2.1.1-bin-hadoop2.7/conf``` and open ```log4j.properties.template```
    - ```cd spark-2.1.1-bin-hadoop2.7/conf```
    - ``` nano log4j.properties.template```
    - Go to the following line: ```log4j.rootCategory=INFO, console``` and change ```INFO``` to ```ERROR```
    - Exit out of the editor

6. Rename ```log4j.properties.template``` to ```log4j.properties```
    - ```mv log4j.properties.template log4.properties```

7. Change working directory to ```/glade/p/work/abanihi```
    - ```cd /glade/p/work/abanihi/```

8. Download H5Spark Package: This package supports Hierarchical Data Format, HDF5/netCDF4 and Rich Parallel I/O interface in Spark. For more details, please see this [page](https://github.com/NCAR/PySpark4Climate/blob/devel/docs/templates/h5spark.md).
    - ```git clone https://github.com/valiantljk/h5spark.git```
    - This package will be added to ```Python Path``` in ```spark-cluster.sh``` script.


### 1.2 Scripts

Even though the scripts for Yellowstone and Cheyenne have so much in common, there are some differences.


- Change working directory to ```/glade/p/work/abanihi```
    - ```cd /glade/p/work/abanihi```

- Create a new directory called ```cheyenne``` and move into it 
    - ```mkdir cheyenne```
    - ```cd cheyenne``
    - Create ```spark-cluster-scripts```directory and move into it
    - ```mkdir spark-cluster-scripts```
    - ```cd spark-cluster-scripts/```

- Create a new script and name it ```spark-env.sh```
    - ```nano spark-env.sh```
    - ```spark-env.sh``` should have the following content 

```bash
##!/usr/bin/env bash

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

```

- Create a new script file and name it ```spark-cluster.sh```
    - ```nano spark-cluster.sh```

```bash
#!/usr/bin/env bash
export SPARK_HOME=/glade/p/work/abanihi/spark-2.1.1-bin-hadoop2.7/
export PYTHONPATH=$SPARK_HOME/python/:$PYTHONPATH
export PYTHONPATH=$PYTHONPATH:/glade/p/work/abanihi/h5spark/src/main/python/h5spark/:$PYTHONPATH
export SPARK_CONF_DIR=~/cheyenne/spark/conf
export SPARK_HOSTFILE=$SPARK_CONF_DIR/spark_hostfile

# create temp hostfile
export SPARK_TEMP_HOSTFILE=$SPARK_CONF_DIR/spark_temp_hostfile

rm $SPARK_HOSTFILE $SPARK_CONF_DIR/slaves

export MPI_SHEPHERD=true
mpiexec_mpt hostname | grep -v Execute | sort >> $SPARK_TEMP_HOSTFILE

#sed -i 's/$/-ib/' $SPARK_TEMP_HOSTFILE
cat $SPARK_TEMP_HOSTFILE | sort -u >> $SPARK_HOSTFILE
tail -n +2 $SPARK_TEMP_HOSTFILE | sort -u >> $SPARK_CONF_DIR/slaves
tail -n +2 $SPARK_TEMP_HOSTFILE | uniq -c > temp_ncores_slaves

rm $SPARK_TEMP_HOSTFILE


export SPARK_MASTER_HOST=$(head -n 1 $SPARK_HOSTFILE)
export MASTER=spark://$SPARK_MASTER_HOST:7077

cp spark-env.sh $SPARK_CONF_DIR/spark-env.sh
source $SPARK_CONF_DIR/spark-env.sh

if [ "$1" == "start" ]; then
    cmd_master="$SPARK_HOME/sbin/start-master.sh"
    cmd_slave="$SPARK_HOME/sbin/spark-daemon.sh --config $SPARK_CONF_DIR start org.apache.spark.deploy.worker.Worker 1 $MASTER"
elif [ "$1" == "stop" ]; then
    cmd_master="$SPARK_HOME/sbin/stop-master.sh"
    cmd_slave="$SPARK_HOME/sbin/spark-daemon.sh --config $SPARK_CONF_DIR stop org.apache.spark.deploy.worker.Worker 1"
else
    exit 1
fi

$cmd_master

while read ncore_slave
do
    ncore=$(echo $ncore_slave | cut -d' ' -f1)
    slave=$(echo $ncore_slave | cut -d' ' -f2)

    if [ "$slave" == "$SPARK_MASTER_HOST" ]; then
          echo "On Master node.  Running: cmd_slave --cores $ncore"
          $cmd_slave --cores $ncore
     else
          echo "On Worker node.  Running: cmd_slave --cores $ncore"
          ssh $slave "$cmd_slave" --cores $ncore < /dev/null

    fi
done <temp_ncores_slaves
```

- Create a new script file and name it ```start-pyspark.sh```

```bash
#!/usr/bin/env bash

source spark-cluster.sh start
$SPARK_HOME/bin/pyspark --master $MASTER

```


- Create a new script file and name it ```start-sparknotebook```. This script file is an extension of ```/glade/apps/opt/jupyter/5.0.0/gnu/4.8.2/bin/start-notebook``` script file.

```bash
#!/usr/bin/env bash

source spark-cluster.sh start

# Add the PySpark classes to the Python path:
export PATH="$SPARK_HOME:$PATH"
export PATH=$PATH:$SPARK_HOME/bin
export PYTHONPATH=$SPARK_HOME/python/:$PYTHONPATH
export PYTHONPATH=$SPARK_HOME/python/lib/py4j-0.10.4-src.zip:$PYTHONPATH

# Create trap to kill notebook when user is done
kill_server() {
    if [[ "$JNPID" != -1 ]]; then
        echo -en "\nKilling Jupyter Notebook Server with PID=$JNPID ... "
        kill "$JNPID"
        echo "done"
        exit 0
    else
        exit 1
    fi
}

JNPID=-1
trap kill_server SIGHUP SIGINT SIGTERM

# Begin server creation
JNHOST=$(hostname)
LOGDIR=/glade/scratch/${USER}/.jupyter-notebook
LOGFILE=${LOGDIR}/log.$(date +%Y%m%dT%H%M%S)
mkdir -p "$LOGDIR"

if [[ $JNHOST == ch* || $JNHOST == r* ]]; then
    STHOST=cheyenne
else
    STHOST=yellowstone
fi

echo "Logging this session in $LOGFILE"

# Check if running on login nodes
if [[ $JNHOST == yslogin* ]]; then
cat << EOF

See "Use of login nodes" here before running Jupyter Notebook on this
node: https://www2.cisl.ucar.edu/resources/yellowstone/using_resources.

Consider running on Geyser instead by using execgy to start a session. (Run execgy -help.)
EOF
elif [[ $JNHOST == cheyenne* ]]; then
cat << EOF

See "Use of login nodes" here before running Jupyter Notebook on this
node: https://www2.cisl.ucar.edu/resources/computational-systems/cheyenne/running-jobs.

Consider running in an interactive job instead by using qinteractive. (Run qinterative -help.)
EOF
fi


jupyter notebook "$@" --no-browser --ip="$JNHOST"> "$LOGFILE" 2>&1 &
JNPID=$!


echo -en  "\nStarting jupyter notebook server, please wait ... "

ELAPSED=0
ADDRESS=

while [[ $ADDRESS != *"${JNHOST}"* ]]; do
    sleep 1
    ELAPSED=$((ELAPSED+1))
    ADDRESS=$(tail -n 1 "$LOGFILE")

    if [[ $ELAPSED -gt 30 ]]; then
        echo -e "something went wrong\n---"
        cat "$LOGFILE"
        echo "---"

        kill_server
    fi
done

echo -e "done\n---\n"

ADDRESS=${ADDRESS##*:}
PORT=${ADDRESS%/*}
TOKEN=${ADDRESS#*=}

cat << EOF
Run the following command on your desktop or laptop:

   ssh -N -l $USER -L 8888:${JNHOST}:$PORT ${STHOST}.ucar.edu

Log in with your YubiKey/Cryptocard (there will be no prompt).
Then open a browser and go to http://localhost:8888. The Jupyter web
interface will ask you for a token. Use the following:

    $TOKEN

Note that anyone to whom you give the token can access (and modify/delete)
files in your GLADE spaces, regardless of the file permissions you
have set. SHARE TOKENS RARELY AND WISELY!

Run the following commands on your destop or latptop:

   ssh -N -l $USER -L 8080:${JNHOST}:8080 ${STHOST}.ucar.edu
   ssh -N -l $USER -L 4040:${JNHOST}:4040 ${STHOST}.ucar.edu

Log in with your YubiKey/Cryptocard(there will be no prompt).
Then open a browser and go to http://localhost:8080 to access the Spark Master UI.

Finally open a browser and go to http://localhost:4040 to access the Spark Master UI jobs
history.

To stop the server, press Ctrl-C.
EOF

# Wait for user kill command
sleep inf
```

**Note:** Make the above scripts executable by running (```chmod +x script_name.sh```)

## 2. Running Existing Cheyenne Spark Installation


- Log into Cheyenne
- Create a working directory in your home and move into it:
    - ```mkdir cheyenne```
    - ```cd cheyenne``
    - ```mkdir spark```
    - ```cd spark```

- Copy ```spark-cluster-scripts``` directory to ```spark``` directory
    - ```cp -r /glade/p/work/abanihi/cheyenne/spark-cluster-scripts .```

- In the created ```spark``` directory, create ```conf``` directory:
    - ```mkdir conf```

- Schedule your job to run on the Cheyenne, by submitting your job through **pbs scheduler**
    - Example: ```qsub -I -l select=4:ncpus=1:mpiprocs=1 -l walltime=00:30:00 -q regular -A ProjectID```

- Change current directory to ```spark-cluster-scripts```
    - ```cd spark-cluster-scripts```

### 2.1. Run PySpark Shell

- To run PySpark shell, run ```start-pyspark.sh``` by running ```./start-pyspark.sh```. You should get something similar to this:![](https://i.imgur.com/cdns3KT.jpg)

### 2.2. Run PySpark in a Jupyter notebook  
       
 - To run PySpark in a Jupyter notebook, make sure you that your current directory is ```spark-cluster-scripts``` and 
    - run ```start-sparknotebook``` by typing ```./start-sparknotebook``` and follow the instructions given.

- There are two notebooks in the ```spark-cluster-scripts/``` directory. Run the **Spark-Essentials** notebook to test that Spark is running and that you have access to a cluster of nodes.

