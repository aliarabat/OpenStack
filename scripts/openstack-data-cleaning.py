import pandas as pd
import re
import commons as cms
import helpers as hpr


def retrieve_depends_on(x):
    '''Extracts Depends-On values out of the commit message 
    '''
    result = re.split(r"\n|\r", x)

    final_result = []
    for l in result:
        if re.search(r"Depends-On:\s[a-zA-Z0-9]+", l):
            if l.startswith("Depends-On: http://review") | l.startswith(
                    "Depends-On: https://review"):
                final_result.append(str(re.search(r"\d+", l)[0]))
            elif re.search(r"^Depends-On:\s[^@:%._\\+~#?&//=\\s]", l):
                if l.find("http") != -1:
                    continue
                final_result.append(l[12:].split(" ")[0])
    return final_result if len(final_result) != 0 else None


def build_depends_chain(row):
    '''Flatten the depends-on columns for each change
    '''
    obj = {}
    depends_on = row["depends_on"]
    obj["Target"] = row["number"]
    obj["Target_repo"] = row["project"]
    row_src = None
    if depends_on.isnumeric():
        row_src = df[df["number"] == int(depends_on)]
    else:
        row_src = df[df["change_id"] == depends_on]

    if len(row_src) != 0:
        source_numbers = hpr.flatten_list(row_src[["number"]].to_numpy())

        source_numbers = list(dict.fromkeys(source_numbers))
        obj["Source"] = source_numbers
        obj["Source_repo"] = row_src["project"].head(1).tolist()[0]

    return obj


def generate_os_evolution_data(df):
    '''Generate Openstack evolution files containing following the 
    columns ["Source", "Target", "Source_repo", "Target_repo"]
    '''
    df_subset_columns = ["change_id", "project", "depends_on", "number"]
    evolution_columns = ["Source", "Target", "Source_repo", "Target_repo"]

    df["depends_on"] = df["commit_message"].map(retrieve_depends_on)

    df = df.explode(column="depends_on").reset_index(drop=True)

    df_depends_on = df.loc[df["depends_on"].isnull() == False,
                           df_subset_columns].copy()

    df_depends_on = df_depends_on.apply(build_depends_chain, axis=1)

    df_depends_on = pd.json_normalize(data=df_depends_on, errors="ignore")

    df_depends_on = df_depends_on.dropna()

    df_depends_on = df_depends_on.explode(column="Source").reset_index(
        drop=True)

    df_depends_on = df_depends_on.loc[:, evolution_columns]

    df_depends_on = df_depends_on[
        df_depends_on["Source_repo"] != df_depends_on["Target_repo"]]

    df_depends_on["Source"] = df_depends_on[["Source"]].astype(int)
    df_depends_on["Target"] = df_depends_on[["Target"]].astype(int)

    df_depends_on.to_csv("%sFiles/source_target_evolution.csv" % hpr.DIR, index=False)


if __name__ == "__main__":

    print("Script openstack-data-cleaning.py started...")

    start_date, start_header = hpr.generate_date("This script started at")

    df = cms.combine_openstack_data()

    generate_os_evolution_data(df)

    end_date, end_header = hpr.generate_date("This script ended at")

    print(start_header)

    print(end_header)

    hpr.diff_dates(start_date, end_date)

    print("Script openstack-data-cleaning.py ended\n")
