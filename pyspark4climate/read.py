#!/usr/bin/env python
###############################################################################
#           This module ingests netCDF data formats into Spark as:            #
#                   - a resilient distributed dataset(RDD)                    #
#                   - a distributed dataframe                                 #
#                                                                             #
#          Missing Features:                                                  #
#                *Support multiple files reading                              #
#                * Convert time_indices from numbers to dates                 #
#                                                                             #
#               __author__  = "Anderson Banihirwe, Kevin Paul"                #
#               __credits__ = "Liping Yang"                                   #
#               __status__  = "Prototype"                                     #
#               __version__ = "0.0.1"                                         #
###############################################################################

from __future__ import print_function
from netCDF4 import Dataset
from netCDF4 import MFDataset
import numpy as np
from pyspark.sql import SparkSession
from pyspark.sql import Row
import itertools
import os
from functools import partial
from pyspark4climate.utils import decode_time


class RDD(object):
    """Defines and initializes rdd with data from netCDF file.
    Attributes:
        filepath                 (str)   :  path for the file to be read
        variable_name            (str)   :  variable name
        dims                     (tuple) :  dimensions (excluding time dimension) of the variable of interest
        ndims                    (int)   :  size of dims tuple
        times                    (list)  :  list of converted datetime values
        partitions               (int)   :  number of partitions to be used by spark
        other_dims_values_tuples (list)  :  list of tuples containing cartesian product of all dims values
    """

    def __init__(self, sc=None, file_list=None, mode='multi', partitions=None):
        if isinstance(file_list, tuple):
            filepath_variable_tuple = file_list
            self.filepath = filepath_variable_tuple[0]
            self.variable_name = filepath_variable_tuple[1]

        elif isinstance(file_list, list):
            filepath_variable_tuple = file_list[0]
            self.filepath = filepath_variable_tuple[0]
            self.variable_name = filepath_variable_tuple[1]

        self.mode = mode
        self.partitions = partitions
        self.dims = None
        self.ndims = None
        self.rows = None
        self.times = decode_time(self.filepath)
        self.other_dims_values_tuples = self.generate_cartesian_product()
        self.rdd = self.create_rdd(sc)

    def generate_cartesian_product(self):
        f = Dataset(self.filepath, 'r')
        dset = f.variables[self.variable_name]
        self.rows = dset.shape[0]
        self.partitions = self.rows / 6
        self.dims = dset.dimensions[1:]
        self.ndims = len(self.dims)
        values = [f.variables[dim][:].tolist() for dim in self.dims]
        f.close()
        return [element for element in itertools.product(*values)]

    def create_rdd(self, sc):
        """Create an RDD from a file_list or tuple of (filepath, variable) and Returns the RDD.
        """

        if self.mode == 'multi':
            return self.read_nc_multi(sc)

        elif self.mode == 'single':
            return self.read_nc_single_chunked(sc)

        else:
            raise NotImplementedError("You specified a mode that is not implemented.")

    def read_nc_single_chunked(self, sc):
        """Generates an RDD and returns it.
        """
        step = self.rows / self.partitions
        variable_name = self.variable_name
        filepath = self.filepath

        rdd = sc.range(0, self.rows, step)\
                .sortBy(lambda x: x, numPartitions=self.partitions)\
                .flatMap(partial(RDD.readonep, self.filepath,
                                 self.variable_name, step)).zipWithIndex()\
                .map(partial(RDD.decode_time_indices, self.times))
        return rdd

    def read_nc_multi(self):
        pass

    @staticmethod
    def readonep(filepath, variable_name, chunk_size, start_idx):
        """Read a slice from one file.

        Args:
            filepath     (str): string containing the file path
            variable_name(str): variable name
            start_idx    (int): starting index
            chunk_size   (int): the chunk size to be read at a time.

        Returns:
            list:   list of the chunk read
        """
        try:
            f = Dataset(filepath, 'r')
            dset = f.variables[variable_name]
            dims = dset.dimensions
            ndims = len(dims)

            end_idx = start_idx + chunk_size
            if end_idx < dset.shape[0]:
                chunk = dset[tuple([slice(start_idx, end_idx)] + [slice(None)] * (ndims - 1))]

            else:
                chunk = dset[tuple([slice(start_idx, dset.shape[0])] + [slice(None)] * (ndims - 1))]

            return list(chunk[:])

        except Exception as e:
            print("IOError: {} {}".format(e, filepath))

        finally:
            pass
            f.close()

    @staticmethod
    def decode_time_indices(times, element):
        time_idx = element[1]
        decoded_time_idx = times[time_idx]
        data = element[0]
        return data, decoded_time_idx
            

class DataFrame(RDD):
    
    def __init__(self, sc=None, file_list=None, mode='multi', partitions=None):
        if isinstance(file_list, tuple):
            filepath_variable_tuple = file_list
            self.filepath = filepath_variable_tuple[0]
            self.variable_name = filepath_variable_tuple[1]

        elif isinstance(file_list, list):
            filepath_variable_tuple = file_list[0]
            self.filepath = filepath_variable_tuple[0]
            self.variable_name = filepath_variable_tuple[1]
        RDD.__init__(self, sc, file_list, mode, partitions)

        # use spark to broadcast some of the variables that are needed by flatten_data and row_transform methods
        self.other_dims_values_tuples = sc.broadcast(super(RDD, self).__getattribute__('other_dims_values_tuples'))
        self.dims_ = sc.broadcast(super(RDD, self).__getattribute__('dims'))
        self.variable_name_ = sc.broadcast(super(RDD, self).__getattribute__('variable_name'))

        self.df = self.create_dataframe()

    def create_dataframe(self):
        """Creates a distributed dataframe from an RDD."""
        return self.rdd.map(partial(DataFrame.flatten_data, self.other_dims_values_tuples)) \
                       .flatMap(lambda x: x).repartition(self.partitions * 10) \
                       .map(partial(DataFrame.row_transform, self.dims_, self.variable_name_))\
                       .toDF()

    @staticmethod
    def flatten_data(other_dims_values_tuples, element):
        """Flattens numpy array and return a tuple of each value
            and its corresponding lat_lon coordinates together with other dimensions.

            Args:
                other_dims_values_tuples   (list)  : contains a tuples generated by generate_cartesian_product() method
                element                    (tuple) :  an rdd element in the form of a tuple (data, idx) where data is
                                            a numpy array and idx correspond to time index.

            Returns:
                 results (tuple): a transformed rdd element in the form
                                   of a tuple (idx, dim1_value, dim_value2, ..., data_value)


            Examples:
                >>> a = rdd.first()
                >>> print(a)
                >>> (array([[ 0.,  1.],
                            [ 2.,  3.]], dtype=float32), 0)

                >>> print(other_dims_values_tuples.value)
                >>> [(-90, 0), (-90, 1), (-90, 2), (-90, 3)]

                flatten_data() would transform this rdd element as follows
                >>> b = rdd.map(Partial(flatten_data, other_dims_values_tuples))
                >>> print(b.first())
                >>> [(0, -90, 0, 0.0), (0, -90, 1, 1.0), (0, -90, 2, 2.0), (0, -90, 3, 3.0)]

        """
        time = element[1]
        data = element[0].ravel().tolist()
        results = map(lambda x: (time,) + (x[0]) + (x[1],), zip(other_dims_values_tuples.value, data))
        return results

    @staticmethod
    def row_transform(dims_, variable_name, element):
        """Transforms a a tuple (idx, dim1_value, dim_value2, ..., data_value) into a Spark sql
               Row object.

            Args:
                dims_           (tuple): broadcasted tuple containing the dimensions
                variable_name   (str)  : variable name
                element         (tuple): a tuple of the form (idx, dim1_value, dim_value2, ..., data_value)

            Returns:
                row(*line) : Spark Row object with arbitray number of items depending on the size of
                             the tuple in line.

            Examples:
                >>> print(element)
                (0, 100000.0, -90.0, 0.0, 257.8)
                >>> print(dims_)
                3
                >>> print(variable_)
                ta
                >>> print(columns)
                ("time", "plev", "lat", "lon", "ta")
                >>> Row(*columns)
                <Row(time, plev, lat, lon, ta)>
                >>> row(*element)
                Row(time=0, plev=100000.0, lat=-90.0, lon=0.0, ta=257.8)
        """
        dims_ = dims_.value
        variable_ = variable_name.value
        columns = ("time",) + tuple(dims_[:]) + (variable_,)
        row = Row(*columns)
        return row(*element)


if __name__ == '__main__':
    spark = SparkSession.builder.appName('testing').getOrCreate()
    sc = spark.sparkContext
    filepath = '/glade/u/home/abanihi/data/pres_monthly_1948-2008.nc'
    var = 'pres'

    data_df = DataFrame(sc, (filepath, var), mode='single')
    df = data_df.df
    print(df.show())
