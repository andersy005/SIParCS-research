# PySpark4Climate
This is a repository for the "PySpark for Big Atmospheric &amp;  Oceanic Data Analysis" 2017 SIParCS Project


# Installation and Use

Spark 2.1.1+Hadoop2.7 is already installed and ready to use on both Cheyenne and Yellowstone.

**Note:** 

- If this is your first time running interactive jobs on multiple nodes, or if you've never installed SSH keys in your yellowstone/cheyenne user environment, installing SSH keys on Yellowstone/Cheyenne will simplify the process of running Spark jobs. For more details on how to install SSH keys go [here](https://www2.cisl.ucar.edu/resources/computational-systems/yellowstone/access-and-user-environment/install-ssh-keys).

- When you run PySpark shell, SparkSession (single point of entry to interact with underlying Spark functionality) is created for you. This is not the case for the Jupyter notebook. Once the jupyter notebook is running, you will need to create and Initialize ```SparkSession``` and ```SparkContext``` before starting to use Spark.

```python
# Import SparkSession
from pyspark.sql import SparkSession

# Initialize SparkSession and attach a sparkContext to the created sparkSession
spark = SparkSession.builder.appName("pyspark").getOrCreate()
sc = spark.sparkContext

```

- If you need to use **Spark Master WebUI**, consider running spark on Cheyenne. As of now, Spark Master WebUI is not available on Yellowstone.


## 1. Yellowstone

- Log into Yellowstone

- Copy ```yellowstone``` directory into your home directory by running 
  - ```cp -r /glade/p/work/abanihi/yellowstone/ .```

- Schedule your job to run on the Yellowstone, by submitting your job through **lsf scheduler**
    - Example: ```bsub -Is -W 01:00 -q small -P ProjectID -R "span[ptile=1]" -n 4 bash```
    

### 1.1. Run PySpark Shell

- To run PySpark shell, run ```~/yellowstone/spark/spark-cluster-scripts/start-pyspark.sh```

 If everything is well setup, you should get something similar to this:![](https://i.imgur.com/cdns3KT.jpg)

### 1.2. Run PySpark in a Jupyter notebook  
       
 - To run PySpark in a Jupyter notebook:
    - run ```~/yellowstone/spark/spark-cluster-scripts/start-sparknotebook``` and follow the instructions given.

- There are two notebooks in the ```spark-cluster-scripts/``` directory. Run the **Spark-Essentials** notebook to test that Spark is running and that you have access to a cluster of nodes.

**NOTE:** We've not been able to get SparkUI feature working on Yellowstone yet!

------------------

## 2. Cheyenne

- Log into Cheyenne

- Copy ```cheyenne``` directory into your home directory by running 
  - ```cp -r /glade/p/work/abanihi/cheyenne/ .```

- Submit your job with **pbs scheduler**
    - Example: ```qsub -I -l select=4:ncpus=1:mpiprocs=1 -l walltime=03:00:00 -q regular -A PROJECTID ```
    

### 2.1. Run PySpark Shell

- To run PySpark shell, run ```~/cheyenne/spark/spark-cluster-scripts/start-pyspark.sh```

### 2.2. Run PySpark in a Jupyter notebook  
       
 - To run PySpark in a Jupyter notebook:
    - run ```~/cheyenne/spark/spark-cluster-scripts/start-sparknotebook``` and follow the instructions given.

### 2.3 Spark webUI on Cheyenne
If you are using Spark in a jupyter notebook, to access the Spark Master webUI, you will need to run the last 2 commands that will appear when you run the ```start-sparknotebook``` script.


## References:
<sup>[1](#footnote1)</sup><a href="https://www2.cisl.ucar.edu/siparcs-2017-projects#big-data">PySpark for "Big" Atmospheric &amp; Oceanic Data Analysis</a>

