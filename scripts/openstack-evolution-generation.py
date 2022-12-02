import pandas as pd
import numpy as np
import networkx as nx
from itertools import chain, product, starmap
from functools import partial


def number_to_repo(data):
    result = []
    for i in range(len(data)):
        new_row = ""
        row = data[i]
        for j in range(len(row)):
            new_row += os_nodes.loc[os_nodes["id"] == row[j],
                                    "label"].tolist()[0]
            if j + 1 < len(row):
                new_row += " "
        result.append(new_row)
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


if __name__ == "__main__":

    print("Script openstack-evolution-generation.py started...")

    df_depends_on = pd.read_csv("../clean_openstack_evolution.csv")

    paths = get_paths(df_depends_on, "Source", "Target")

    os_edges = df_depends_on[["Source", "Target"]].copy()

    os_nodes_1 = df_depends_on[["Source", "Source_repo"]].copy()
    os_nodes_1 = os_nodes_1.rename(columns={
        "Source": "id",
        "Source_repo": "label"
    })

    os_nodes_2 = df_depends_on[["Target", "Target_repo"]].copy()
    os_nodes_2 = os_nodes_2.rename(columns={
        "Target": "id",
        "Target_repo": "label"
    })

    os_edges = os_edges.reset_index(drop=True)

    os_nodes = pd.concat((os_nodes_1, os_nodes_2))
    os_nodes = os_nodes.drop_duplicates()
    os_nodes = os_nodes.reset_index(drop=True)

    np_paths = np.array(paths)

    co_evolution_number_df = pd.DataFrame(np_paths)

    data_repo_changes = number_to_repo(np_paths)

    co_evolution_repo_df = pd.DataFrame(data_repo_changes)

    co_evolution_number_df.to_csv("../Files/co_evolution_number.csv",
                                  index=False)
    co_evolution_repo_df.to_csv("../Files/co_evolution_repo.csv", index=False)

    os_nodes.to_csv("../Files/os_nodes.csv", index=False)
    os_edges.to_csv("../Files/os_edges.csv", index=False)

    print("Script openstack-evolution-generation.py ended\n")
