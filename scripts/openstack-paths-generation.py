import pandas as pd
import networkx as nx
from itertools import chain, product,  starmap
from functools import partial
import os
import shutil
import re
import helpers as hpr
from commons import combine_openstack_data


def retrieve_project_numbers(x):
    '''Retrieve number associated with each project
    '''
    return x["number"].values


def remove_single_components(arr):
    '''Remove lines with only one number
    '''
    result = []
    for item in arr:
        if len(dict.fromkeys(item)) > 1:
            result.append(list(item))

    return result

def retrieve_related_bug(x):
    result = re.findall(r"(Related-Bug:\s#\d+)", x)
    return [item[14:] for item in result]


def get_paths(df):
    '''Get all possible paths regarding the Source and Target columns
    '''
    chaini = chain.from_iterable

    G = nx.DiGraph(df[["Source", "Target"]].values.tolist())

    roots = (v for v, d in G.in_degree() if d == 0)

    leaves = (v for v, d in G.out_degree() if d == 0)

    all_paths = partial(nx.all_simple_paths, G)

    paths = list(chaini(starmap(all_paths, product(roots, leaves))))

    return paths


def build_related_bug_paths(df):
    '''Extend initial path with related-bug numbers
    '''
    df["related_bug"] = df["commit_message"].map(retrieve_related_bug)

    df = df.explode(column="related_bug").reset_index(drop=True)

    df_main_related_bug = df[df["related_bug"].notnull()].copy()

    df_main_related_bug["related_bug"] = df_main_related_bug[[
        "related_bug"
    ]].astype(int)

    df_main_related_bug = df_main_related_bug[[
        "related_bug", "number"
    ]].groupby("related_bug").apply(retrieve_project_numbers).reset_index(
        drop=True)

    paths = remove_single_components(df_main_related_bug)

    return paths


def build_other_paths(df, property):
    '''Extend initial path with other paths, namely topic, subject and change-id
    '''
    df_main_topic = df[df[property].isnull() == False].copy()

    df_topic_subset = df_main_topic[[
        property, "number"
    ]].groupby(property).apply(retrieve_project_numbers).reset_index(drop=True)

    paths = remove_single_components(df_topic_subset)

    return paths


def combine_co_changes_number(main_array, second_array):
    '''Combine lines that mention at least 1 common number
    '''
    result = main_array.copy()
    
    for arr_item in second_array:

        added = False
        for j in range(len(main_array)):
            row_dep = main_array[j]
            check_any = any(item in row_dep for item in arr_item)

            if check_any:
                result[j] = list(dict.fromkeys(result[j] + arr_item))
                added = True

        if not added:
            result.append(arr_item)
    return result


if __name__ == "__main__":

    print("Script openstack-paths-generation.py started...")

    start_date, start_header = hpr.generate_date("This script started at")

    DIR = hpr.DIR
    files_path = "%sFiles/" % DIR
    for d in ["%sNumber" % (files_path), "%sRepo" % (files_path), "%sMetrics" % (files_path)]:
        if not os.path.exists(d):
            os.makedirs(d)
        # shutil.rmtree(path=DIR)

    df = combine_openstack_data()

    df_depends_needed = pd.read_csv("%sFiles/source_target_evolution.csv" % DIR)

    paths = get_paths(df_depends_needed)

    related_bug_number_changes = build_related_bug_paths(df)
    topic_number_changes = build_other_paths(df, "topic")
    change_id_number_changes = build_other_paths(df, "change_id")

    result_number_changes = combine_co_changes_number(paths, related_bug_number_changes)

    result_number_changes = combine_co_changes_number(result_number_changes, topic_number_changes)

    result_number_changes = combine_co_changes_number(result_number_changes, change_id_number_changes)

    pd.DataFrame({"Path": paths}).to_csv("%sFiles/Number/depends_needed.csv" % DIR, index=False)
    pd.DataFrame({"Path": related_bug_number_changes}).to_csv("%sFiles/Number/related_bug.csv" % DIR, index=False)
    pd.DataFrame({"Path": topic_number_changes}).to_csv("%sFiles/Number/topic.csv" % DIR, index=False)
    pd.DataFrame({"Path": change_id_number_changes}).to_csv("%sFiles/Number/change_id.csv" % DIR, index=False)
    pd.DataFrame({"Path": result_number_changes}).to_csv("%sExperiments/all_paths.csv" % DIR, index=False)

    end_date, end_header = hpr.generate_date("This script ended at")

    print(start_header)

    print(end_header)

    hpr.diff_dates(start_date, end_date)

    print("Script openstack-paths-generation.py ended\n")
