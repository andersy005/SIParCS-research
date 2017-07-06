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
