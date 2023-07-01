import pandas as pd
import ast
import sys
sys.path.append('../utils')
import helpers as hpr
from commons import combine_openstack_data


def number_to_repo(data, df):
    '''Replace numbers of data with their corresponding repository names, then removing any duplicates.
    '''
    df_subset = df[["number", "project"]]
    result = []
    for i in range(len(data)):
        row = data[i]
        new_row = df_subset.loc[
            df_subset["number"].isin(row), "project"].values.tolist()
        result.append(new_row)
    return result


def merge_numbers(data):
    '''merge lines that mention at least one common number
    '''
    result = []
    data_copy = data.copy()
    for i in range(len(data)):
        new_item = {}
        not_to_add_indices = []

        if len(data[i]) == 0:
            continue

        for j in range(len(data_copy)):

            check_any = any(item in data[i] for item in data_copy[j])
            if check_any:
                new_item = {**new_item, **dict.fromkeys(data[i] + data_copy[j])}
                data_copy[j] = []
                not_to_add_indices.append(j)
        if len(new_item) == 0:
            print(new_item)
            result.append(data[i])
        else:
            result.append(list(new_item))

        for ntai in not_to_add_indices:
            data[ntai] = []

    return result


if __name__ == "__main__":

    print("Script openstack-paths-extending.py started...")

    start_date, start_header = hpr.generate_date("This script started at")

    DIR = hpr.DIR

    df = combine_openstack_data()

    result_number_co_changes = pd.read_csv("%sFiles/Number/all_paths.csv" % DIR)

    result_number_co_changes = result_number_co_changes["Path"].apply(ast.literal_eval).values.tolist()

    result_number_co_changes = [list(item) for item in result_number_co_changes]

    all_paths_flattend = list(dict.fromkeys(hpr.flatten_list(result_number_co_changes)))

    single_component_changes_number = df.loc[~df["number"].isin(all_paths_flattend), "number"].map(lambda x: [x]).tolist()

    extended_paths_number = result_number_co_changes

    merged_number_paths = merge_numbers(extended_paths_number) + single_component_changes_number

    pd.DataFrame({ "Path": merged_number_paths }).to_csv("%sFiles/Number/extended_paths.csv" % DIR, index=False)

    print("Number/extended_paths.csv generated successfully")

    possible_path_repo = number_to_repo(merged_number_paths, df)

    pd.DataFrame({ "Path": possible_path_repo }).to_csv("%sFiles/Repo/extended_paths.csv" % DIR, index=False)

    print("Repo/extended_paths.csv generated successfully")

    end_date, end_header = hpr.generate_date("This script ended at")

    print(start_header)

    print(end_header)

    hpr.diff_dates(start_date, end_date)

    print("Script openstack-paths-extending.py ended\n")
