import pandas as pd

if __name__ == "__main__":
    df = pd.read_csv("../Files/openstack_evolution.csv")

    df = df.dropna()

    df = df.drop_duplicates().reset_index(drop=True)

    # df = df.drop_duplicates(subset=["Source_repo", "Target_repo"])

    df = df[df["Source_repo"] != df["Target_repo"]]

    df["Source"] = df[["Source"]].astype(int)
    df["Target"] = df[["Target"]].astype(int)

    df.to_csv("../Files/clean_openstack_evolution.csv", index=False)
