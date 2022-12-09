from datetime import datetime
import os

DIR = "E:/PhD/Projects/Openstack/"
# DIR = "/home/as98450/OpenStack/"

def convert(seconds):
    """Convert seconds in the following format
    XX days, XX hours, XX minutes and XX seconds 
    """
    day = seconds // (24 * 3600)
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return "%d days, %d hours, %02d minutes and %02d seconds" % (
        day, hour, minutes, seconds)


def generate_date(header):
    """Generate a date with a passed-in title
    """
    date = datetime.now().strftime("%Y/%m/%d %H:%M:%S:%f")
    return date, "{} {}".format(header, date)


def diff_dates(start_date, end_date):
    """Calculate the difference between two dates
    """
    start_date = datetime.strptime(start_date, "%Y/%m/%d %H:%M:%S:%f")
    end_date = datetime.strptime(end_date, "%Y/%m/%d %H:%M:%S:%f")

    elapsed_seconds = convert((end_date - start_date).seconds)

    print("This script took {}".format(elapsed_seconds))

def list_file(directory):
    """List files of a directory
    """
    files = [f for f in os.listdir(directory)]
    return files

def flatten_list(array):
    '''Flattens array items
    Example: [[1], [2, 3], [4]] becomes [1, 2, 3, 4]
    '''
    result = [item for sublist in array for item in sublist]
    return result