import pandas as pd

if __name__ == "__main__":
    df = pd.read_csv("./openstack_evolution.csv")

    df = df.dropna()

    df = df.drop_duplicates()

    df = df.drop_duplicates(subset=["Source_repo", "Target_repo"])

    df = df.reset_index(drop=True)

    df = df[df["Source_repo"] != df["Target_repo"]]

    df.to_csv("clean_openstack_evolution.csv", index=False)
