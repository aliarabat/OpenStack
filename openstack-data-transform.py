import pandas as pd
import numpy as np
import json
from pathlib import Path
import os
import helpers as hpr
import shutil

directory_prefix = "/home/as98450/OpenStack/"


def process_json_file(file_name):
    with open('%sData/%s' % (directory_prefix, file_name), 'r') as string:
        dict_data = json.load(string)
    string.close()
    return dict_data


def retrieve_reviewers(df, index):
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

    filepath = '%sreviewers/reviewers_data_%d.csv' % (directory_prefix, index)
    reviewers_df.to_csv(filepath, index=False, encoding='utf-8')


def retrieve_messages(df, index):
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

    filepath = '%smessages/messages_data_%d.csv' % (directory_prefix, index)
    messages_df.to_csv(filepath, index=False, encoding='utf-8')


def retrieve_files(df, index):
    revisions_df = df[[
        "change_id", "current_revision", "project", "subject", "revisions"
    ]].copy()

    revisions_df["files"] = revisions_df.apply(
        lambda row: {
            "change_id": row["change_id"],
            "current_revision": row["current_revision"],
            "project": row["project"],
            "subject": row["subject"],
            "files": row["revisions"][row["current_revision"]]["files"],
        },
        axis=1)

    files_df = revisions_df["files"]

    files_data = []

    for row in np.array(files_df):
        file_keys = row["files"].keys()
        for fk in file_keys:
            new_row = {"name": fk, **row, **row["files"][fk]}
            files_data.append(new_row)

    files_df = pd.DataFrame(files_data)

    del files_df["files"]
    del files_df["status"]

    files_df = files_df.drop(columns=["files", "status", "old_path", "binary"],
                             errors="ignore")

    file_path = "%s/files/files_data_%d.csv" % (directory_prefix, index)
    files_df.to_csv(file_path, index=False, encoding='utf-8')


def calc_nbr_files(row):
    current_revision = row["revisions"][row["current_revision"]]
    if "files" not in current_revision.keys():
        return 0
    return len(current_revision["files"])


def retrieve_changes(data, index):
    changes_columns = [
        "id", "project", "branch", "topic", "change_id", "owner", "subject",
        "created", "updated", "submitted", "insertions", "deletions",
        "reviewers", "messages", "revisions", "total_comment_count", "_number",
        "current_revision", "messages_count", "reviewers_count",
        "revisions_count", "files_count"
    ]

    df = pd.DataFrame(data=data, columns=changes_columns)

    df["messages_count"] = df["messages"].map(lambda x: len(x))
    df["reviewers"] = df["reviewers"].map(lambda x: x["REVIEWER"])
    df["reviewers_count"] = df["reviewers"].map(lambda x: len(x))
    df["revisions_count"] = df["revisions"].map(lambda x: len(x))
    df["files_count"] = df.apply(calc_nbr_files, axis=1)

    df["owner_account_id"] = df["owner"].map(
        lambda x: x["_account_id"] if "_account_id" in x.keys() else None)
    df["owner_name"] = df["owner"].map(lambda x: x["name"]
                                       if "name" in x.keys() else None)
    df["owner_username"] = df["owner"].map(lambda x: x["username"]
                                           if "username" in x.keys() else None)

    del df["owner"]

    changes_df = df.copy()
    changes_df.columns = changes_df.columns.str.replace("_number", "number")

    del changes_df["reviewers"]
    del changes_df["messages"]
    del changes_df["revisions"]

    filepath = "%s/changes/changes_data_%d.csv" % (directory_prefix, index)
    changes_df.to_csv(filepath, index=False, encoding='utf-8')

    return df


if __name__ == "__main__":

    start_date = hpr.generate_date("This script started at")

    changes_dir = "%schanges" % directory_prefix
    reviewers_dir = "%sreviewers" % directory_prefix
    messages_dir = "%smessages" % directory_prefix
    files_dir = "%sfiles" % directory_prefix

    for dir in list([changes_dir, reviewers_dir, messages_dir, files_dir]):
        if os.path.exists(dir):
            shutil.rmtree(path=dir)
        os.makedirs(dir)

    index = 0
    # file_path = "openstack_data_train.json"
    for f in hpr.list_file("%sData" % directory_prefix):
        # for index in range(1):
        print("Index =====>  %d" % index)

        original_data = process_json_file(f)

        df = retrieve_changes(original_data, index)

        retrieve_reviewers(df, index)

        retrieve_messages(df, index)

        retrieve_files(df, index)

        index += 1

    end_date = hpr.generate_date("This script ended at")

    hpr.diff_dates(start_date, end_date)
