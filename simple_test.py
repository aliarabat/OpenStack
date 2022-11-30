import pandas as pd
import numpy as np
import re
import helpers as hpr


def attach_co_changing_components(base_component):
    co_changes = df_depends_on.loc[df_depends_on["Source_repo"] ==
                                   base_component, "Target_repo"].values
    result = {base_component: list(co_changes)}
    return result

def dfs(data, path, paths):
    datum = path[-1]              
    if datum in data:
        for val in data[datum]:
            new_path = path + [val]
            paths = dfs(data, new_path, paths)
    else:
        paths += [path]
    return paths

def enumerate_paths(graph, nodes):
    nodes = list(nodes)
    all_paths = []
    for node in nodes:
        node_paths = dfs(graph, [node], [])
        # exist = False
        # for path in all_paths:
        #     if node in path:
        #         exist = True
        # if not exist:
        all_paths += node_paths
        # exist = False
    return all_paths

if __name__ == "__main__":

    graph = {
        "A": ["B", "C"],
        "C": ["D", "E"],
        "F": ["E"]
    }

    df_depends_on = pd.read_csv("clean_openstack_evolution.csv")

    co_changing_components = df_depends_on[["Source_repo"]].copy()

    co_changing_components = co_changing_components.drop_duplicates().reset_index(drop=True)

    co_changing_components = co_changing_components["Source_repo"].map(
    attach_co_changing_components)

    co_changing_components = co_changing_components.rename("Path")

    co_changing_components = co_changing_components.reset_index(drop=True)

    newdict = {}
    for k, v in [(key, d[key]) for d in co_changing_components for key in d]:
        if k not in newdict: newdict[k] = v
        else: newdict[k].append(v)

    graph_keys = df_depends_on["Source_repo"].drop_duplicates().to_dict().values()
    graph_keys = {*graph_keys}
    graph_keys = set([k for k in graph_keys if len(df_depends_on[df_depends_on["Target_repo"] == k]) > 0])

    result = enumerate_paths(newdict, graph_keys)

    print(result)