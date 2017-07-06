# [PySpark4Climate Package](https://github.com/NCAR/PySpark4Climate)

PySpark4Climate is a high level library for parsing netCDF data with Apache Spark, for Spark SQL and DataFrames.


## Requirements
This library requires:

- [Spark 2.0+](https://spark.apache.org/)
- [netcdf4-python 1.2.8+](https://unidata.github.io/netcdf4-python/)


## Features

This package allows reading netCDF files in local or distributed filesystem a:

- [Spark DataFrames](https://spark.apache.org/docs/latest/sql-programming-guide.html#datasets-and-dataframes)

- [Spark RDD](https://spark.apache.org/docs/latest/quick-start.html)

When reading files the API accepts several options:

- ```sc```          : by default ```sc``` is ```None```, but sc should be set to SparkContext
- ```file_list```   : list of tuples. Each tuple is of the form (filepath, variable_name). By default ```file_list``` is None. 
- ```mode```        : string. By default ```mode``` is ```multi``` for multiple files. To read a single a file, ```mode``` is set to ```single```.
- ```partitions```  : number of partitions to be used by Spark. By default ```partitions``` is None. When ```partitions``` is ```None```, Spark uses the number of partitions computed using information from the dataset metadata.



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

**Currently Supported Fe
* [x] Introduction
* [x] Usage
* [x] Curabitur elit nibh, euismod et ullamcorper at, iaculis feugiat est
* [ ] Vestibulum convallis sit amet nisi a tincidunt
    * [x] In hac habitasse platea dictumst
    * [x] In scelerisque nibh non dolor mollis congue sed et metus
    * [x] Sed egestas felis quis elit dapibus, ac aliquet turpis mattis
    * [ ] Praesent sed risus massa
* [ ] Aenean pretium efficitur erat, donec pharetra, ligula non scelerisque
* [ ] Nulla vel eros venenatis, imperdiet enim id, faucibus nisi