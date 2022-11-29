import pandas as pd
import re
import helpers as hpr


def retrieve_depends_on(x):
    result = re.split(r"\n|\r", x)

    final_result = []
    for l in result:
        if re.search(r"Depends-On:\s[a-zA-Z0-9]+", l):
            if l.startswith("Depends-On: https://review"):
                final_result.append(str(re.search(r"\d+", l)[0]))
            elif re.search(r"^Depends-On:\s[^@:%._\\+~#?&//=]", l):
                if l.find("https") != -1:
                    continue

                final_result.append(l[12:])
    return final_result if len(final_result) != 0 else None


def build_depends_chain(row):
    obj = {}
    depends_on = row["depends_on"]
    obj["Target"] = row["change_id"]
    obj["Target_repo"] = row["project"]
    row_src = None
    if depends_on.isnumeric():
        row_src = df[df["number"] == int(depends_on)].head(1)
    else:
        row_src = df[df["change_id"] == depends_on].head(1)

    if len(row_src) != 0:
        obj["Source"] = row_src["change_id"].tolist()[0]
        obj["Source_repo"] = row_src["project"].tolist()[0]

    return obj


def generate_os_evolution_data(df):
    df_subset_columns = ["change_id", "project", "depends_on", "number"]
    evolution_columns = ["Source", "Target", "Source_repo", "Target_repo"]

    df = df.explode(column="depends_on").reset_index(drop=True)

    df_subset_dep = df.loc[df["depends_on"].isnull() == False,
                           df_subset_columns].copy().reset_index(drop=True)

    df_depends_on = df_subset_dep.apply(build_depends_chain, axis=1)

    df_depends_on = pd.json_normalize(data=df_depends_on, errors="ignore")

    df_depends_on = df_depends_on.loc[:, evolution_columns]

    df_depends_on.to_csv("openstack_evolution.csv", index=False)


def combine_openstack_data():
    df = pd.DataFrame([])
    data_path = "Data/"
    changes_file_names = hpr.list_file(data_path)
    for i in range(len(changes_file_names)):
        df_per_file = pd.read_csv("%schanges_data_%d.csv" % (data_path, i))
        df = pd.concat((df, df_per_file))

    df = df.sort_values(by="updated", ascending=False).reset_index(drop=True)

    df["depends_on"] = df["commit_message"].map(retrieve_depends_on)

    return df


if __name__ == "__main__":

    start_date, start_header = hpr.generate_date("This script started at")
    
    df = combine_openstack_data()

    generate_os_evolution_data(df)

    end_date, end_header = hpr.generate_date("This script ended at")

    print(start_header)

    print(end_header)

    hpr.diff_dates(start_date, end_date)
