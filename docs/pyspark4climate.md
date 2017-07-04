# [PySpark4Climate Package](https://github.com/valiantljk/h5spark)

## 1. Introduction

- Apache Spark is an open source cluster computing framework
    - It was developed at UCB AMPLab, 2014 v1.0, 2016 v.2
        - Actively developed, 1086 contributors, 19, 788 commits (As of June 5, 2017)

    - Productive programming interface
        - 6 vs 28 lines of code compare to hadoop mapreduce

    - Implicit data parallelism
    - Fault-tolerance

- Spark for Data-intensive Computing
    - Streaming processing
    - SQL
    - Machine Learning, MLlib
    - Graph Processing


## 2. Porting Apache Spark software stack on HPC

- Advantages of Porting Spark onto HPC
    - A more productive API for data-intensive computing
    - Relieve the users from:
        - concurrency control
        - communication
        - memory management with traditional MPI model
    - Embarrassingly parallel computing, ```data.map(func)```
    - Fault tolerance, ```recompute()```


- HPC applications often rely on hierarchical data formats to organize files and datasets. **However, accessing data stored in HDF5/netCDF4 files is not natively supported in Spark.** 

- Reasons of lack of netCDF/HDF5 support in Spark include:
    - Lack of an API in Spark to directly load or sub-select HDF5/netCDF datasets into its in-memory data structures.
    - HDF5/netCDF have a deep hierarchy, which cannot simply be treated as a sequence of bytes nor be evenly divided.
    - GPFS file system is not well tuned for SPARK I/O and vice versa.



## 3. Data in Spark

**Resilient Distributed Datasets(RDDs)** are:

- The primary abstraction in Spark
    - Immutable(Read-Only) once constructed
    - Spark tracks lineage information to efficiently recompute lost data
    - Enable operations on collection of elements in parallel
    
- You construct RDDs
    - by parallelizing existing Python collections (lists)
    - by transforming an existing RDDs
    - from files in HDFS or any other storage system (glade in case of Yellowstone and Cheyenne)
    
    
- The programmer needs to specify the number of partitions for an RDD or the default value is used if unspecified.

![Partitioning](https://i.imgur.com/zaOQIQY.jpg)

*Image Courtesy: BerkeleyX-CS100.1x-Big-Data-with-Apache-Spark*


There are two types of operations on RDDs: **Transformations** and **Actions**.



- **Transformations** are lazy in a sense that they are not computed immediately
- Transformed RDD is executed when action runs on it.
- RDDs can be persisted(cached) in memory or disk.

**Working with RDDs**:

- Create an RDD from a data source
- Apply transformations to an RDD: ```.map(...)```
- Apply actions to an RDD: ```.collect()```, ```.count()```

![](https://i.imgur.com/iqvUJV5.jpg)


![](https://i.imgur.com/EuyK62Q.jpg)

*Image Courtesy: BerkeleyX-CS100.1x-Big-Data-with-Apache-Spark*

## 4. Data in HDF5/netCDF4
- Hierarchical Data Format v5
![](https://i.imgur.com/gFC9CAp.jpg)




## 5. Support HDF5/netCDF4 in Spark 2.x Series
- What does Spark have in reading various data formats?
    - Textfile: ```sc.textFile()``` or ```spark.read.load("filename.txt", format="txt")```
    - Parquet: ```spark.read.load("filename.parquet", format="parquet")```
    - Json: ```spark.read.load("filename.json", format="json")```
    - csv: ```spark.read.load("filename.csv", format="csv)```
    - jdbc: ```spark.read.load("filename.jdbc", format="jdbc")```
    - orc, libsvm follow the same pattern.

- How about HDF5/netCDF4?:
    - There was no such thing as ```spark.read.load("filename.hdf5", format="hdf5")``` or ```spark.read.load("filename.nc", format="nc")``` until **H5Spark Package** came along!!


- Challenges: Functionality and Performance
    - How to transform an HDF5 dataset into an RDD?
    - How to utilize the HDF5 I/O libraries in Spark?
    - How to enable parallel I/O on HPC?
    - What is the impact of a parallel filesytem striping like [GPFS](https://en.wikipedia.org/wiki/IBM_General_Parallel_File_System)?
    - What is the effect of Caching on I/O in Spark?

[H5Spark](https://github.com/valiantljk/h5spark) is a Spark Package that:
- Supports Hierarchical Data Format, HDF5/netCDF4 and Rich Parallel I/O interface in Spark.

- Optimizes I/O performance on HPC with Lustre Filesytems Tuning.


# 6. H5Spark Design

H5Spark has 4 major components:

    1. Meta data analyzer 
    2. RDD seeder
    3. Hyperslab partitioner
    4. RDD constructor

- **For loading a single HDF5 file:**

    - H5Spark metadata analyzer takes the user's input filename and dataset name and triggers *first* I/O call to the file system to fetch the HDF5 file metadata info

    - I/O calls ```h5fopen``` and ```h5dopen``` are called to return size of each dimension of queried dataset.

    - Spark partition parameter is used to control the degree of parallelism.

        - E.g: If the user chooses 10 partitions, then there will be at most 10 parallel tasks to process the RDD.

- **Pros of H5Spark**

    - Parallel I/O is transparently handled without user's interaction
    - H5Spark's I/O is an **MPI-Like** independent I/O and this means that:
        - each executor will issue the I/O independently without communicating with other executors.

- **Scala/Python implementation**

    - Spark favors Scala and Python
    - H5Spark uses HDF5 Python library
    - Underneath is HDF5 C posix library
    - No MPIIO support 

![](https://i.imgur.com/gdQnBl3.jpg)

As it's shown in the figure below, **H5Spark** was designed for and tested on **Lustre parallel filesytem**. 

![](https://i.imgur.com/ILcF9uH.jpg)

**TODO:** Test H5Spark on NCAR's GPFS filesytem.


**References:**

- J.L. Liu, E. Racah, Q. Koziol, R. S. Canon, A. Gittens, L. Gerhardt, S. Byna, M. F. Ringenburg, Prabhat. "H5Spark: Bridging the I/O Gap between Spark and Scientific Data Formats on HPC Systems", Cray User Group, 2016, ([Paper](https://cug.org/proceedings/cug2016_proceedings/includes/files/pap137.pdf))

- [H5Spark GitHub Repo](https://github.com/valiantljk/h5spark)
