import os
import helpers as hpr


if __name__ == "__main__":
    print("Setup...")
    
    start_date, start_header = hpr.generate_date("The setup script started at")
    
    script_names = [
        "openstack-data-collection.py", "openstack-data-transform.py",
        "openstack-data-cleaning.py", "openstack-paths-generation.py",
        "openstack-paths-extending.py", "openstack-metrics-extractor.py"
    ]

    for sn in script_names:
        os.system("python ./Scripts/%s" % sn)
    
    end_date, end_header = hpr.generate_date("The setup script ended at")

    print(start_header)

    print(end_header)

    hpr.diff_dates(start_date, end_date)

    print("Setup ended")