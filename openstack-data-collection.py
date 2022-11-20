import json
import requests
from datetime import datetime
import os
import helpers as hpr
import shutil


def get_openstack_data(dir):
    """Perform http requests to Opendev API,
    to get the list of changes related to the Openstack repository
    """
    is_done = False
    size = 500
    page = 0

    start_date = hpr.generate_date("This script started at")

    while (not is_done):

        params = {'O': 97, 'n': size, 'S': page * size}
        # after should also be modified with your preferences

        url = "https://review.opendev.org/changes/?q=repositories:{} after:{}&o={}&o={}&o={}&o={}".format(
            "openstack", "2020-10-21", "CURRENT_FILES", "MESSAGES",
            "CURRENT_COMMIT", "CURRENT_REVISION")

        change_response = requests.get(url, params=params)

        data_per_request = change_response.text.split("\n")[1]

        data_per_request = list(json.loads(data_per_request))

        print("Length %d" % len(data_per_request))

        if len(data_per_request) != 0:

            print("page %s" % page)

            data_per_request = json.dumps(data_per_request)

            jsonFile = open("{}openstack_data_{}.json".format(dir, page), "w")

            jsonFile.write(data_per_request)

            jsonFile.close()

            page += 1
        else:
            is_done = not is_done

    end_date = hpr.generate_date("This script ended at")

    hpr.diff_dates(start_date, end_date)


if __name__ == "__main__":

    DIR = hpr.DIR

    if os.path.exists(DIR):
        shutil.rmtree(path=DIR)
    os.makedirs(DIR, exist_ok=True)

    get_openstack_data(DIR)