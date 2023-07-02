import os
import pandas as pd
from datetime import datetime

DIR = "/Users/aliarabat/Documents/PhD/projects/openstack-evolution/"
# DIR = "C:/Users/Ali/Documents/PhD/projects/openstack-evolution/"
# DIR = "/home/as98450/projects/openstack/"

TOKEN = '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'
GerritAccount = "aOQvaHsS1ar-vMzULlfZ5ExfJiWecMGx9G"
XSRF_TOKEN = "aOQvaHrC9OUN2lmxiDz8BgpSu.sehm5CSq"

def convert(seconds):
    """Convert seconds in the following format
    XX days, XX hours, XX minutes and XX seconds 
    """
    day = seconds // (24 * 60 * 60)
    seconds = seconds % (24 * 60 * 60)
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

def combine_openstack_data():
    '''Combine generated csv files into a single DataFrame object
    '''
    df = pd.DataFrame([])
    data_path = "%sChanges/" % DIR
    changes_file_names = list_file(data_path)
    for i in range(len(changes_file_names)):
        df_per_file = pd.read_csv("%schanges_data_%d.csv" % (data_path, i))
        df = pd.concat((df, df_per_file))

    df = df.drop_duplicates(subset=["number"])

    df = df.sort_values(by="updated", ascending=False).reset_index(drop=True)

    return df