
# Quick Start: Cheyenne

**Prerequisites:** 

- If this is your first time running interactive jobs on multiple nodes, or if you've never installed SSH keys in your yellowstone/cheyenne user environment, installing SSH keys on Yellowstone/Cheyenne will simplify the process of running Spark jobs. For more details on how to install SSH keys go [here](https://www2.cisl.ucar.edu/resources/computational-systems/yellowstone/access-and-user-environment/install-ssh-keys).


## Logging in 
- Log in to the Cheyenne system from the terminal
    - ```ssh -X -l username cheyenne.ucar.edu```

- Copy ```cheyenne``` directory into your home directory by running 
    - ```cp -r /glade/p/work/abanihi/cheyenne/ .```


## Submitting jobs

Spark can be run interactively ( via ipython shell, jupyter notebook) or in batch mode. 

### 1. Interactive jobs

To start an interactive job, use the qsub command with the necessary options.

   - ```qsub -I -l select=1:ncpus=36:mpiprocs=36 -l walltime=01:00 -q small -A project_code```

### 1.1 Load IPython shell with PySpark

- To start IPython shell with PySpark, run the following:
     
     - ```~/cheyenne/spark/spark-cluster-scripts/start-pyspark.sh```

![](https://i.imgur.com/P2tb9vp.jpg)


### 1.2. Run PySpark in a Jupyter notebook  
       
 - To run PySpark in a Jupyter notebook, run the following:
    - ```~/cheyenne/spark/spark-cluster-scripts/start-sparknotebook``` and follow the instructions given.

![](https://i.imgur.com/l5nK3IA.jpg)


**Note:**

 When you run PySpark shell, SparkSession (single point of entry to interact with underlying Spark functionality) is created for you. This is not the case for the Jupyter notebook. Once the jupyter notebook is running, you will need to create and Initialize ```SparkSession``` and ```SparkContext``` before starting to use Spark.


```python
# Import SparkSession
from pyspark.sql import SparkSession

# Initialize SparkSession and attach a sparkContext to the created sparkSession
spark = SparkSession.builder.appName("pyspark").getOrCreate()
sc = spark.sparkContext

```


### 2. Batch jobs
To submit a Spark batch job, use the qsub command followed by the name of your PBS batch script file.
- ```qsub script_name```

### 2.1. Spark job script example

**Batch script to run a Spark job:**

- ```spark-test.sh```

```sh
#!/usr/bin/env bash
#PBS -A project_code
#PBS -j oe
#PBS -m abe
#PBS -M email_address
#PBS -q queue_name
#PBS -l walltime=01:00
#PBS -l select=1:ncpus=4:mpiprocs=4

source ~/cheyenne/spark/spark-cluster-scripts/spark-cluster.sh start
$SPARK_HOME/bin/spark-submit --master $MASTER ~/cheyenne-jobs/spark-test.py
```

- ```spark-test.py```

```python
from __future__ import print_function
from read import RDD, DataFrame
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName('spark-test').getOrCreate()
sc = spark.sparkContext
sc.addPyFile("/glade/p/work/abanihi/pyspark4climate/read.py")
filepath = '/glade/u/home/abanihi/data/pres_monthly_1948-2008.nc'
var = 'pres'
data_df = DataFrame(sc, (filepath, var), 'single')
df = data_df.df
print(df.show())
```

To run this spark job, run:

- ```qsub spark-test.sh```
