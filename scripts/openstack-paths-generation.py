import pandas as pd
import networkx as nx
import os
from itertools import chain, product, starmap
from functools import partial
from commons import combine_openstack_data


def retrieve_project_numbers(x):
    return x["number"].values


def remove_single_components(arr):
    result = []
    for item in arr:
        if len(dict.fromkeys(item)) > 1:
            result.append(list(item))

    return result


def get_paths(df):
    graph = nx.from_pandas_edgelist(df=df,
                                    source="Source",
                                    target="Target",
                                    create_using=nx.DiGraph)

    roots = (node for node, d in graph.in_degree if d == 0)

    leaves = (node for node, d in graph.out_degree if d == 0)

    all_paths = partial(nx.all_simple_paths, graph)

    paths = list(
        chain.from_iterable(starmap(all_paths, product(roots, leaves))))

    return paths


def build_related_bug_paths(df):
    df_main_related_bug = df[df["related_bug"].isnull() == False].copy()

    df_main_related_bug["related_bug"] = df_main_related_bug[[
        "related_bug"
    ]].astype(int).reset_index(drop=True)

    df_related_bug_subset = df_main_related_bug[[
        "related_bug", "number"
    ]].groupby("related_bug").apply(retrieve_project_numbers).reset_index(
        drop=True)

    paths = remove_single_components(df_related_bug_subset)

    return paths


def build_other_paths(df, property):

    df_main_topic = df[df[property].isnull() == False].copy()

    df_topic_subset = df_main_topic[[
        property, "number"
    ]].groupby(property).apply(retrieve_project_numbers).reset_index(drop=True)

    paths = remove_single_components(df_topic_subset)

    return paths


def combine_co_changes_number(main_path, other_paths):
    result = main_path.copy()

    for other_arr in other_paths:
        for arr_item in other_arr:
            arrays_to_add = []

            for j in range(len(main_path)):
                row_dep = main_path[j]
                check_any = any(item in row_dep for item in arr_item)

                if check_any == True:
                    result[j] = list(dict.fromkeys(result[j] + arr_item))
                elif arr_item not in arrays_to_add:
                    arrays_to_add.append(arr_item)

            arrays_to_add = [item for item in arr_item]
            result.append(arrays_to_add)
            arrays_to_add = []
    return result


if __name__ == "__main__":

    print("Script openstack-paths-generation.py started...")

    df = combine_openstack_data()

    df_depends_on = pd.read_csv("../Files/clean_openstack_evolution.csv")

    paths = get_paths(df_depends_on)

    related_bug_number_changes = build_related_bug_paths(df)
    topic_number_changes = build_other_paths(df, "topic")
    subject_number_changes = build_other_paths(df, "subject")
    change_id_number_changes = build_other_paths(df, "change_id")

    result_number_changes = combine_co_changes_number(
        paths, [related_bug_number_changes])

    result_number_changes = combine_co_changes_number(result_number_changes,
                                                      [topic_number_changes])

    result_number_changes = combine_co_changes_number(result_number_changes,
                                                      [subject_number_changes])
    result_number_changes = combine_co_changes_number(
        result_number_changes, [change_id_number_changes])

    pd.DataFrame({
        "Path": paths
    }).to_csv("../Co-changes/Number/depends_on.csv", index=False)
    pd.DataFrame({
        "Path": related_bug_number_changes
    }).to_csv("../Co-changes/Number/related_bug.csv", index=False)
    pd.DataFrame({
        "Path": topic_number_changes
    }).to_csv("../Co-changes/Number/topic.csv", index=False)
    pd.DataFrame({
        "Path": subject_number_changes
    }).to_csv("../Co-changes/Number/subject.csv", index=False)
    pd.DataFrame({
        "Path": change_id_number_changes
    }).to_csv("../Co-changes/Number/change_id.csv", index=False)
    pd.DataFrame({
        "Path": result_number_changes
    }).to_csv("../Co-changes/Number/all_paths.csv", index=False)

    print("Script openstack-paths-generation.py ended\n")
