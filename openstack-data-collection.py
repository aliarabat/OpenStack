import json
import requests
from datetime import datetime
import os
import helpers

# exist_ok=True should be removed when running on the server
os.makedirs("./OpenStack/Data", exist_ok=True)

is_done = False
size = 500
page = 0

start_date = helpers.generate_date("This script started at")

while (not is_done):

    params = {'O': 97, 'n': size, 'S': page * size}
    # after should also be modified with your preferences
    change_response = requests.get(
        'https://review.opendev.org/changes/?q=status:merged repositories:openstack after:2020-01-01&o=CURRENT_FILES&o=MESSAGES&o=CURRENT_COMMIT&o=CURRENT_REVISION',
        params=params)

    data_per_request = change_response.text.split("\n")[1]

    data_per_request = list(json.loads(data_per_request))

    print("Length %d" % len(data_per_request))

    if len(data_per_request) != 0:

        print("page %s" % page)

        data_per_request = json.dumps(data_per_request)

        jsonFile = open("OpenStack/Data/openstack_data_{}.json".format(page),
                        "w")

        jsonFile.write(data_per_request)

        jsonFile.close()

        page += 1
    else:
        is_done = not is_done

end_date = helpers.generate_date("This script ended at")

helpers.diff_dates(start_date, end_date)