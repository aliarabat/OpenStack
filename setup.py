import os

if __name__ == "__main__":
    print("Setup...")
    script_names = [
        "openstack-data-collection.py", "openstack-data-transform.py",
        "openstack-data-cleaning.py", "openstack-paths-generation.py",
        "openstack-paths-extending.py", "openstack-metrics-extractor.py"
    ]

    for sn in script_names:
        os.system("python %s" % sn)
