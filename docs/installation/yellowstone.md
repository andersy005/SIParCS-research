# Apache Spark 2.1.1 on Yellowstone

The first task of our research project was to install the newest version of Apache Spark on Yellowstone. 

At the time (May/2017), there was an old installation of Apache Spark (Spark 1.6) on Yellowstone. This installation was done by Davide Del Vento.

As of today (June/2017), we've been able to install the newest version of Apache Spark - [Spark 2.1.1+Hadoop2.7](https://spark.apache.org/downloads.html).

Below are the steps that we took to get Spark Up and Running on Yellowstone.

If all you need is to run the existing Apache Spark on Yellowstone, just skip to **Section 2** of this page.


## 1. Installation

### 1.1 Downloading Spark and Setting up Spark's directory and necessary files

1. Log into Yellowstone
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

**Note:** The scripts in this directory are based on Davide's previous scripts for Spark 1.6.

- Change working directory to ```/glade/p/work/abanihi```
    - ```cd /glade/p/work/abanihi```

- Create a new directory called ```yellowstone``` and move into it 
    - ```mkdir yellowstone```
    - ```cd yellowstone``
    - Create ```spark-cluster-scripts```directory and move into it
    - ```mkdir spark-cluster-scripts```
    - ```cd spark-cluster-scripts/```

- Create a new script and name it ```spark-env.sh```
    - ```nano spark-env.sh```
    - ```spark-env.sh``` should have the following content 

```bash
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

```

- Create a new script file and name it ```spark-cluster.sh```
    - ```nano spark-cluster.sh```

```bash
#!/usr/bin/env bash
export SPARK_HOME=/glade/p/work/abanihi/spark-2.1.1-bin-hadoop2.7/
export PYTHONPATH=$SPARK_HOME/python/:$PYTHONPATH
export PYTHONPATH=$PYTHONPATH:/glade/p/work/abanihi/pyspark4climate/
export SPARK_CONF_DIR=~/yellowstone/spark/conf
export SPARK_HOSTFILE=$SPARK_CONF_DIR/spark_hostfile

# create temp hostfile
export SPARK_TEMP_HOSTFILE=$SPARK_CONF_DIR/spark_temp_hostfile

rm $SPARK_HOSTFILE $SPARK_CONF_DIR/slaves


mpirun.lsf hostname | grep -v Execute | sort >> $SPARK_TEMP_HOSTFILE

sed -i 's/$/-ib/' $SPARK_TEMP_HOSTFILE
cat $SPARK_TEMP_HOSTFILE | sort -u >> $SPARK_HOSTFILE
tail -n +2 $SPARK_TEMP_HOSTFILE | sort -u >> $SPARK_CONF_DIR/slaves
tail -n +2 $SPARK_TEMP_HOSTFILE | uniq -c > $SPARK_CONF_DIR/temp_ncores_slaves

rm $SPARK_TEMP_HOSTFILE


export SPARK_MASTER_HOST=$(head -n 1 $SPARK_HOSTFILE)
export MASTER=spark://$SPARK_MASTER_HOST:7077

cp ~/yellowstone/spark/spark-cluster-scripts/spark-env.sh $SPARK_CONF_DIR/spark-env.sh
source $SPARK_CONF_DIR/spark-env.sh

if [ "$1" == "start" ]; then
    cmd_master="$SPARK_HOME/sbin/start-master.sh"
    cmd_slave="$SPARK_HOME/sbin/spark-daemon.sh --config $SPARK_CONF_DIR start org.apac
he.spark.deploy.worker.Worker 1 $MASTER"
elif [ "$1" == "stop" ]; then
    cmd_master="$SPARK_HOME/sbin/stop-master.sh"
    cmd_slave="$SPARK_HOME/sbin/spark-daemon.sh --config $SPARK_CONF_DIR stop org.apach
e.spark.deploy.worker.Worker 1"
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
          ssh $slave "$cmd_slave" --cores $ncore </dev/null &
    fi
done <$SPARK_CONF_DIR/temp_ncores_slaves

```

- Create a new script file and name it ```start-pyspark.sh```

```bash
#!/usr/bin/env bash

source ~/yellowstone/spark/spark-cluster-scripts/spark-cluster.sh start

$SPARK_HOME/bin/pyspark --master $MASTER

```


- Create a new script file and name it ```start-sparknotebook```. This script file is an extension of ```/glade/apps/opt/jupyter/5.0.0/gnu/4.8.2/bin/start-notebook``` script file.

```bash
#!/usr/bin/env bash

#source spark-cluster.sh start
source ~/yellowstone/spark/spark-cluster-scripts/spark-cluster.sh start

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

Consider running on Geyser instead by using execgy to start a session. (Run execgy -hel
p.)
EOF
elif [[ $JNHOST == cheyenne* ]]; then
cat << EOF

See "Use of login nodes" here before running Jupyter Notebook on this
node: https://www2.cisl.ucar.edu/resources/computational-systems/cheyenne/running-jobs.

Consider running in an interactive job instead by using qinteractive. (Run qinterative
-help.)
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

To stop the server, press Ctrl-C.
EOF

# Wait for user kill command
sleep inf

```

**Note:** Make the above scripts executable (```chmod +x script_name.sh```)


