import pandas as pd
import numpy as np

df_depends_on = pd.read_csv("clean_openstack_evolution.csv")


def attach_co_changing_components(base_component):
    co_changes = df_depends_on.loc[df_depends_on["Source_repo"] ==
                                   base_component, "Target_repo"].values
    result = np.concatenate(([base_component], co_changes))
    return result


if __name__ == "__main__":

    co_changing_components = df_depends_on[["Source_repo"]].copy()

    co_changing_components = co_changing_components.drop_duplicates(
    ).reset_index(drop=True)

    co_changing_components = co_changing_components["Source_repo"].map(
        attach_co_changing_components)

    co_changing_components = co_changing_components.reset_index(drop=True)

    co_changing_components = co_changing_components.rename("Path")

    co_changing_components.to_csv("openstack_evolution_paths.csv", index=False)
