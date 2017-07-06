# PySpark for "Big" Atmospheric & Oceanic Data Analysis 

## Background

> Climate and Weather directly impact all aspects of society. Understanding these processeses provide important information for policy - and decision - makers. To understand the average climate conditions and extreme weather events, Earth science and climate change researchers need data from climate models and observations. As such in the typical work flow of climate change and atmospheric research, much time is wasted waiting to reformat and regrid data to homogeneous formats. Additionally, because of the data volume, in order to compute metrics, perform analysis, and visualize data / generate plots, multi-stage processes with repeated I/O are used - the root cause of performance bottlenecks and the resulting user’s frustrations related to time inefficiencies.
**[NASA-SciSpark project](https://scispark.jpl.nasa.gov/about.html)**

<a name="footnote1">1</a>: Spark is a cluster computing paradigm based on the MapReduce paradigm that has garnered many scientific analysis workflows and are very well suited for Spark.  As a result of this lack of great deal of interest for its power and ease of use in analyzing “big data” in the commercial and computer science sectors.  In much of the scientific sector, however --- and specifically in the atmospheric and oceanic sciences --- Spark has not captured the interest of scientists for analyzing their data, even though their datasets may be larger than many commercial datasets interest, there are very few platforms on which scientists can experiment with and learn about using Hadoop and/or Spark for their scientific research.  Additionally, there are very few resources to teach and educate scientists on how or why to use Hadoop or Spark for their analysis.


## Goal

**PySpark for Big Atmospheric & Oceanic Data Analysis** is a [CISL/SIParCS research project](https://www2.cisl.ucar.edu/siparcs) that seeks to explore the realm of distributed parallel computing on NCAR's Yellowstone and Cheyenne supercomputers by taking advantage of: 

- Apache Spark's potential to offer speed-up and advancements of nearly 1000x in-memory

- The increasing growing community around Spark

- Spark's notion of Resilient Distributed Datasets(RDDs). RDDs represent immutable dataset that can be: 
  - reused across multi-stage operations.
  - partitioned across multiple machines.
  - automatically reconstructed if a partition is lost.

to address the pain points that scientists and researchers endure during model evaluation processes. 

Examples of these pain points include:

 - Temporal and Zonal averaging of data
 - Computation of climatologies
 - Pre-processing of CMIP data such as:
   - Regridding 
   - Variable clustering (min/max)
   - calendar harmonizing



## What's Apache Spark?

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


## Porting Apache Spark software stack on HPC

- Advantages of Porting Spark onto HPC
    - A more productive API for data-intensive computing
    - Relieve the users from:
        - concurrency control
        - communication
        - memory management with traditional MPI model
    - Embarrassingly parallel computing, ```data.map(func)```
    - Fault tolerance, ```recompute()```


- HPC applications often rely on hierarchical data formats to organize files and datasets. **However, accessing data stored in HDF/netCDF files is not natively supported in Spark.** 

- Reasons of lack of netCDF/HDF support in Spark include:
    - Lack of an API in Spark to directly load or sub-select HDF/netCDF datasets into its in-memory data structures.
    - HDF/netCDF have a deep hierarchy, which cannot simply be treated as a sequence of bytes nor be evenly divided.
    - GPFS file system is not well tuned for SPARK I/O and vice versa.



## Data in Spark

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

## Data in HDF/netCDF
- Hierarchical Data Format v5
![](https://i.imgur.com/gFC9CAp.jpg)




## Support HDF/netCDF in Spark 2.x Series
- What does Spark have in reading various data formats?
    - Textfile: ```sc.textFile()``` or ```spark.read.load("filename.txt", format="txt")```
    - Parquet: ```spark.read.load("filename.parquet", format="parquet")```
    - Json: ```spark.read.load("filename.json", format="json")```
    - csv: ```spark.read.load("filename.csv", format="csv)```
    - jdbc: ```spark.read.load("filename.jdbc", format="jdbc")```
    - orc, libsvm follow the same pattern.

- How about HDF5/netCDF4?:
    - There is no such thing as ```spark.read.load("filename.hdf5", format="hdf5")``` or ```spark.read.load("filename.nc", format="nc")```


- Challenges: Functionality and Performance
    - How to transform an netCDF dataset into an RDD?
    - How to utilize the netCDF I/O libraries in Spark?
    - How to enable parallel I/O on HPC?
    - What is the impact of a parallel filesytem striping like [GPFS](https://en.wikipedia.org/wiki/IBM_General_Parallel_File_System)?
    - What is the effect of Caching on I/O in Spark?

- Any Solution?
    - **[PySpark4Climate Package](https://github.com/NCAR/PySpark4Climate)** is a high level library for parsing netCDF data with Apache Spark, for Spark SQL and DataFrames.


