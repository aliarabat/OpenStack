import os
import utils.helpers as hpr


if __name__ == "__main__":
    print("Setup...")
    
    start_date, start_header = hpr.generate_date("The setup script started at")
    
    script_names = [
        "openstack-data-collection", 
        "openstack-data-transform",
        "openstack-core-members",
        "openstack-project-selection",
        "openstack-pq-metrics-extractor",
        "openstack-dependencies-generation", 
        "openstack-paths-generation",
        "openstack-paths-extending"
    ]

    for sn in script_names:
        os.system("python ./Scripts/%s.py" % sn)
    
    end_date, end_header = hpr.generate_date("The setup script ended at")

    print(start_header)

    print(end_header)

    hpr.diff_dates(start_date, end_date)

    print("Setup ended")