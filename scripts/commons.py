import pandas as pd
import re
import helpers as hpr


def retrieve_related_bug(x):
    result = re.search(r"(Related-Bug:\s#\d+)", x)
    return result[0][14:] if result else None


def combine_openstack_data():
    '''Combine generated csv files into a single DataFrame object
    '''
    df = pd.DataFrame([])
    data_path = "../Changes/"
    changes_file_names = hpr.list_file(data_path)
    for i in range(len(changes_file_names)):
        df_per_file = pd.read_csv("%schanges_data_%d.csv" % (data_path, i))
        df = pd.concat((df, df_per_file))

    df = df.drop_duplicates(subset=["number"])

    df = df.sort_values(by="updated", ascending=False).reset_index(drop=True)

    df["related_bug"] = df["commit_message"].map(retrieve_related_bug)

    # df.to_csv("../Files/os_datasets.csv", index=False)

    return df