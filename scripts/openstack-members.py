import json
import pandas as pd
import requests
import os
from commons import combine_openstack_data
import sys
sys.path.append('../utils')
import helpers as hpr
import collections

DIR = hpr.DIR

def get_openstack_core_members():
    """Perform http requests to Opendev API,
    to get the list of core members related to the Openstack repository
    """
    result = {}
    cookies = {
        "GerritAccount": "aOQvaHsS1ar-vMzULlfZ5ExfJiWecMGx9G",
        "XSRF_TOKEN": "aOQvaHrC9OUN2lmxiDz8BgpSu.sehm5CSq"
    }
    for repo in os_repositories:
        url = "https://review.opendev.org/groups/%s/members/" % repo

        change_response = requests.get(url, cookies=cookies)

        data_per_request = change_response.text.split("\n")[1]
        if data_per_request != "":
            data_per_request = list(json.loads(data_per_request))
        else:
            data_per_request = []

        result[repo] = data_per_request
    return result

def retrieve_account_ids(devs):
    return [dev["_account_id"] for dev in devs]



if __name__ == "__main__":

    print("Script openstack-members.py started...")

    start_date, start_header = hpr.generate_date("This script started at")

    df = combine_openstack_data()
    # Retrieve OpenStack core team member 
    os_repositories = list(dict.fromkeys(df["project"].values))

    os_repositories = ["%s-core" % p[10:] for p in os_repositories]

    os_core_members = get_openstack_core_members()

    df_os_core_members = pd.DataFrame({"repo": os_core_members.keys(), "developers": os_core_members.values()})

    df_os_core_members["developers"] = df_os_core_members["developers"].map(retrieve_account_ids)

    df_os_core_members["devs_count"] = df_os_core_members["developers"].map(lambda x: len(x))

    df_os_core_members = df_os_core_members.loc[df_os_core_members["devs_count"] != 0]

    df_os_core_members.to_csv("%sRQs/PQ/Files/os_core_team.csv" % DIR, index=False)

    # Retrieve OpenStack core team member
    developers = df.loc[(df["is_owner_bot"] == 0)&(df["status"] != "ABANDONED"), "owner_account_id"]

    developers = collections.Counter(developers.values)
    
    developers = pd.DataFrame({"dev": developers.keys(), "nbr_changes": developers.values()})
    
    developers.loc[developers["nbr_changes"] == 1, "dev"].to_csv("%sRQs/Files/casual_constributors.csv" % DIR, index=False)

    end_date, end_header = hpr.generate_date("This script ended at")

    print(start_header)

    print(end_header)

    hpr.diff_dates(start_date, end_date)

    print("Script openstack-members.py ended\n")
