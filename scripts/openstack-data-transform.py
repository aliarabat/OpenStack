import pandas as pd
import numpy as np
import json
import os
import shutil
import helpers as hpr

DIR = hpr.DIR


def process_json_file(file_name):
    """Transform a json file into a readable python dict format
    """
    with open('%sData/%s' % (DIR, file_name), 'r') as string:
        dict_data = json.load(string)
    string.close()
    return dict_data


def retrieve_reviewers(df, index):
    """Filter the reviewers of each change
    """
    old_columns = ["change_id", "reviewers"]
    main_columns = ["change_id", "account_id", "name", "email", "username"]

    reviewers_df = df[old_columns].copy()

    reviewers_df["flatenned_object"] = reviewers_df.apply(
        lambda row: {
            "change_id": row["change_id"],
            "reviewers": row["reviewers"]
        },
        axis=1)

    reviewers_df = reviewers_df.drop(columns=old_columns)

    reviewers_df = pd.json_normalize(data=reviewers_df["flatenned_object"],
                                     record_path="reviewers",
                                     meta=["change_id"],
                                     sep="_",
                                     errors='ignore')

    reviewers_df.columns = reviewers_df.columns.str.replace(
        "_account_id", "account_id")

    reviewers_df = reviewers_df[main_columns]

    filepath = '%sReviewers/reviewers_data_%d.csv' % (DIR, index)
    reviewers_df.to_csv(filepath, index=False, encoding='utf-8')


def retrieve_messages(df, index):
    """Filter the discussion messages of each change
    """
    old_columns = ["change_id", "current_revision", "messages"]

    new_columns = [
        "change_id", "id", "date", "message", "author_account_id",
        "author_name", "author_username", "real_author_account_id",
        "real_author_name", "real_author_username", "author_email",
        "real_author_email"
    ]

    messages_df = df[old_columns].copy()

    messages_df["flatenned_object"] = messages_df.apply(
        lambda row: {
            "change_id": row["change_id"],
            "messages": row["messages"]
        },
        axis=1)

    for c in old_columns:
        del messages_df[c]

    messages_df = pd.json_normalize(data=messages_df["flatenned_object"],
                                    record_path="messages",
                                    meta=["change_id"],
                                    sep="_",
                                    errors="ignore")

    messages_df = messages_df.rename(
        columns={
            "author__account_id": "author_account_id",
            "real_author__account_id": "real_author_account_id"
        })

    messages_df = messages_df[new_columns]

    filepath = '%sMessages/messages_data_%d.csv' % (DIR, index)
    messages_df.to_csv(filepath, index=False, encoding='utf-8')


def filter_files_attr(row):
    """Filter files of the current change
    """
    if row["current_revision"] not in row["revisions"].keys():
        return {}

    return row["revisions"][row["current_revision"]]["files"]


def retrieve_files(df, index):
    """Filter the files of each change
    """
    revisions_df = df[[
        "change_id", "current_revision", "project", "subject", "revisions"
    ]].copy()

    revisions_df["files"] = revisions_df.apply(
        lambda row: {
            "change_id": row["change_id"],
            "current_revision": row["current_revision"],
            "project": row["project"],
            "subject": row["subject"],
            "files": filter_files_attr(row),
        },
        axis=1)

    files_df = revisions_df[["files"]]

    files_data = []

    for row in np.array(files_df):
        row = row[0]
        file_keys = row["files"].keys()

        if len(file_keys) == 0:
            continue

        for fk in file_keys:
            new_row = {"name": fk, **row, **row["files"][fk]}
            files_data.append(new_row)

    files_df = pd.DataFrame(files_data)

    del files_df["files"]
    del files_df["status"]

    files_df = files_df.drop(columns=["files", "status", "old_path", "binary"],
                             errors="ignore")

    file_path = "%sFilesOS/files_data_%d.csv" % (DIR, index)
    files_df.to_csv(file_path, index=False, encoding='utf-8')


def calc_nbr_files(row):
    """Count number of files for each change
    """
    return len(filter_files_attr(row))


def retrieve_commit_message(row):
    """Retrieve commit message of each review
    """
    if row["current_revision"] not in row["revisions"].keys():
        keys = list(row["revisions"].keys())
        return row["revisions"][keys[0]]["commit"]["message"]

    return row["revisions"][row["current_revision"]]["commit"]["message"]


def retrieve_changes(origin_df, index):
    """Filter the changes
    """
    changes_columns = [
        "id", "project", "branch", "change_id", "owner", "subject",
        "status", "created", "updated", "submitted", "insertions", "deletions",
        "reviewers", "messages", "revisions", "total_comment_count", "_number",
        "current_revision"
    ]

    df = origin_df[changes_columns]

    df["discussion_messages_count"] = df["messages"].copy().map(lambda x: len(x))
    df["reviewers"] = df["reviewers"].map(lambda x: x["REVIEWER"]
                                          if "REVIEWER" in x.keys() else [])
    df["reviewers_count"] = df["reviewers"].map(lambda x: len(x))
    df["revisions_count"] = df["revisions"].map(lambda x: len(x))
    df["files_count"] = df.apply(calc_nbr_files, axis=1)

    df["owner_account_id"] = df["owner"].map(
        lambda x: x["_account_id"] if "_account_id" in x.keys() else None)
    df["owner_name"] = df["owner"].map(lambda x: x["name"]
                                       if "name" in x.keys() else None)
    df["owner_username"] = df["owner"].map(lambda x: x["username"]
                                           if "username" in x.keys() else None)

    df["commit_message"] = df.apply(retrieve_commit_message, axis=1)

    if "topic" in origin_df.columns:
        df = pd.concat((df, origin_df[["topic"]]), axis=1)

    del df["owner"]

    changes_df = df.copy()
    changes_df.columns = changes_df.columns.str.replace("_number", "number")

    del changes_df["reviewers"]
    del changes_df["messages"]
    del changes_df["revisions"]

    file_path = "%sChanges2/changes_data_%d.csv" % (DIR, index)
    changes_df.to_csv(file_path, index=False, encoding='utf-8')

    return df


if __name__ == "__main__":

    print("Script openstack-data-transform.py started...")

    start_date, start_header = hpr.generate_date("This script started at")

    changes_dir = "%sChanges2" % DIR
    reviewers_dir = "%sReviewers" % DIR
    messages_dir = "%sMessages" % DIR
    files_dir = "%sFilesOS" % DIR

    for dir in list([changes_dir, reviewers_dir, messages_dir, files_dir]):
        if os.path.exists(dir):
           shutil.rmtree(path=dir)
        os.makedirs(dir)

    # index = 0
    # file_path = "openstack_data_722.json"
    for f in hpr.list_file("%sData" % DIR):
        # for index in range(1406, 1407):
        # f = "openstack_data_%d.json" % index

        index = int(f[15:-5])

        print("Filename =====>  %s" % f)

        print("Index =====>  %d" % index)

        # print("Index =====>  %d" % index)
        origin_df = pd.read_json('%sData/%s' % (DIR, f))
        # original_data = process_json_file(f)

        df = retrieve_changes(origin_df, index)

        retrieve_reviewers(df, index)

        retrieve_messages(df, index)

        retrieve_files(df, index)

        index += 1

    end_date, end_header = hpr.generate_date("This script ended at")

    print(start_header)

    print(end_header)

    hpr.diff_dates(start_date, end_date)

    print("Script openstack-data-transform.py ended\n")
