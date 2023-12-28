import os
import pandas as pd
from datetime import datetime

DIR = os.getcwd() + '/'
# DIR = "C:/Users/Ali/Documents/PhD/projects/openstack-evolution/"
# DIR = "/home/as98450/projects/openstack/"

TOKEN = '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'
GerritAccount = "aOQvaHsS1ar-vMzULlfZ5ExfJiWecMGx9G"
XSRF_TOKEN = "aOQvaHrC9OUN2lmxiDz8BgpSu.sehm5CSq"

def convert(seconds):
    # Calculate days, hours, minutes, and remaining seconds
    days = seconds // (24 * 3600)
    seconds %= (24 * 3600)
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return f'{days:.2f} days, {hours:.2f} hours, {minutes:.2f} minutes and {seconds:.2f} seconds'


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

def combine_openstack_data(filter_merged=True, filter_real_dev=True):
    '''Combine generated csv files into a single DataFrame object
    '''
    df = pd.DataFrame([])
    data_path = "%sChanges/" % DIR
    changes_file_names = list_file(data_path)
    for i in range(len(changes_file_names)):
        df_per_file = pd.read_csv("%schanges_data_%d.csv" % (data_path, i))
        df = pd.concat((df, df_per_file))

    if filter_merged:
        df = df[(df['status'] == 'MERGED')]

    if filter_real_dev:
        df = df[df['is_owner_bot'] == False]
    
    df = df.drop_duplicates(subset=["number"])

    df = df.sort_values(by="created", ascending=False).reset_index(drop=True)

    df['created'] = df['created'].map(lambda x: x[:-10])

    df.loc[df['project'].str.startswith('openstack/'), 'project'] = df['project'].map(lambda x: x[10:])

    return df