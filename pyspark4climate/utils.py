from netCDF4 import num2date
from netCDF4 import Dataset
import datetime as dt


def decode_time(filename):
    """Decode NetCDF time values into Python datetime objects.
    Args:
        - filename     (str): name of netCDF file from which time values should be extracted.

    Returns:
        - The list of converted datetime values
    """

    f = Dataset(filename, 'r')
    time_data = f.variables['time']
    time_units = time_data.units

    if 'calendar' in time_data.ncattrs():
        time_calendar = time_data.calendar
    else:
        time_calendar = 'standard'

    dates = num2date(time_data[:], time_units, time_calendar)
    f.close()
    return dates


if __name__ == '__main__':
    pass
