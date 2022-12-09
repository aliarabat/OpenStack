import pandas as pd
import helpers as hpr
from commons import combine_openstack_data


def number_to_repo(data, df):
    df_subset = df[["number", "project"]]
    result = []
    for i in range(len(data)):
        row = data[i]
        new_row = df_subset.loc[
            df_subset["number"].isin(row), ["project"]].drop_duplicates(
                subset="project").values.reshape(-1).tolist()
        result.append(new_row)
    return result


def combine_path_numbers(data):
    result = []
    data = data.copy()
    for i in range(len(data)):
        new_item = {}

        if len(data[i]) == 0:
            continue

        for j in range(1, len(data)):
            if len(data[j]) == 0 or (data[i] == data[j]):
                continue

            check_any = any(item in data[i] for item in data[j])
            if check_any == True:
                new_item = {**new_item, **dict.fromkeys(data[i] + data[j])}
                data[j] = []

        if len(new_item) == 0:
            result.append(data[i])
        else:
            result.append(list(new_item))
        data[i] = []

    return result


if __name__ == "__main__":

    print("Script openstack-paths-extending.py started...")

    start_date, start_header = hpr.generate_date("This script started at")

    # df = combine_openstack_data()

    df = pd.read_csv("%sexperiments/all_paths.csv" % hpr.DIR)

    result_number_co_changes = pd.read_csv(
        "%sCo-changes/Number/all_paths.csv" % hpr.DIR,
        converters={'Path': pd.eval})

    result_number_co_changes = result_number_co_changes["Path"].to_list()

    result_number_co_changes = [
        list(item) for item in result_number_co_changes
    ]

    all_paths_flattend = list(
        dict.fromkeys(hpr.flatten_list(result_number_co_changes)))

    single_component_changes = df.loc[~df["number"].isin(all_paths_flattend),
                                      ["number", "project"]].reset_index(
                                          drop=True)

    single_component_changes_number = single_component_changes["number"].map(
        lambda x: [x]).tolist()

    extended_paths_number = result_number_co_changes + single_component_changes_number

    test = extended_paths_number[:5000]

    combined_number_paths = combine_path_numbers(test)

    pd.DataFrame({
        "Path": combined_number_paths
    }).to_csv("%sCo-changes/Number/extended_paths.csv" % hpr.DIR, index=False)

    print("Number/extended_paths.csv generated successfully")

    possible_path_repo = number_to_repo(combined_number_paths, df)

    pd.DataFrame({
        "Path": possible_path_repo
    }).to_csv("%sCo-changes/Repo/extended_paths.csv" % hpr.DIR, index=False)

    print("Repo/extended_paths.csv generated successfully")

    end_date, end_header = hpr.generate_date("This script ended at")

    print(start_header)

    print(end_header)

    hpr.diff_dates(start_date, end_date)

    print("Script openstack-paths-extending.py ended\n")
