import pandas as pd

if __name__ == "__main__":

    print("Script openstack-data-manipulation.py started...")

    df = pd.read_csv("../Files/openstack_evolution.csv")

    df = df.dropna()

    df = df.drop_duplicates().reset_index(drop=True)

    df = df[df["Source_repo"] != df["Target_repo"]]

    df["Source"] = df[["Source"]].astype(int)
    df["Target"] = df[["Target"]].astype(int)

    df.to_csv("../Files/clean_openstack_evolution.csv", index=False)

    print("Script openstack-data-manipulation.py ended\n")
