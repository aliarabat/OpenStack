import pandas as pd

import helpers as hpr


def combine_openstack_data():
    '''Combine generated csv files into a single DataFrame object
    '''
    df = pd.DataFrame([])
    data_path = "%sChanges2/" % hpr.DIR
    changes_file_names = hpr.list_file(data_path)
    for i in range(len(changes_file_names)):
        df_per_file = pd.read_csv("%schanges_data_%d.csv" % (data_path, i))
        df = pd.concat((df, df_per_file))

    df = df.drop_duplicates(subset=["number"])

    df = df.sort_values(by="updated", ascending=False).reset_index(drop=True)

    return df