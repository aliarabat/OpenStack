# This is a quick description on how to use this project

This tool was primarily written in python programming language, since it is the most widely used in data science field, with the massive community surrounding it. This project was developed in the context of analyzing the co-evolution of software ecosystem, especially among Openstack components. Therefore, this tool is well-structured to ensure it's easy to use for newcomers.

## Set up your project environment

- Make sure all config values are changed with your own options in the files */utils/helpers.py*.
- This project requires python version 3 or later to be installed in you machine as well as the following packages :
    1. pandas
    2. numpy
    3. json
    4. requests
    5. shutil
    6. networkx
    7. bs4
- Execute the following command `export PYTHONPATH="${PYTHONPATH}:/Users/aliarabat/Documents/PhD/projects/openstack-evolution"`

The projects is organized as follows:

1. **Changes directory :** the main data source used in this project, it contains csv file.
2. **File directory :** generated csv files are generated here for further analysis.
3. **Scripts :** contains all scripts to run from data collection to data analysis

## How to use the project

The mian entry point to the project is the core file located at the root directory called *setup.py* which executes the certain scripts in the order as follows:

1. **openstack-data-collection.py**: collect the data from the OpenDev platform, thenn store the data in *Changes* directory.
2. **openstack-data-transform.py**: transforms the previously acquired data to a proper data format, which are then saved in csv-based files.
3. **openstack-members.py**: serves for get the list of OpenStack core team members. To do so, one must provide two important secret credentials **GerritAccount** and **XSRF_TOKEN** which can be accessed via browser coookie of the following website [link](https://review.opendev.org/admin/repos)". Plus, *casual contributors* are also obtained.
4. **openstack-project-selection.py**: this script retrieves the main OpenStack core services and map each project to their proper service.
5. **openstack-pq-metrics-extractor**: calculates the metrics for each pairs of projects/services such as developers'intersection.
6. **openstack-dependencies-generation.py**: generates the dependecies through *Depends-On* and *Needed-By* tags.
7. **openstack-paths-generation.py**: generates the chains of related changes according to the results of the previous script.
8. **openstack-paths-extending.py**: this extends the chains of depednent changes using *Related-Bug* and *Change-Id* infromations.

## Requirements for this projects



## How to run each script

There are two ways to run those scripts :

- Execute all scripts at once using the following command `python setup.py`
- Execute a particular script by using calling `python "SCRIPT_NAME".py`

## Important Notice

It is not suggested to run all the scripts at once, since it will take much time. Since the Data folder contains all files to play with you can go directly to the third step

## Links

1. The *Files* folder containes 2 sub-folders and 1 file:
    - **Number/ :** contains number-based co-changes
    - **Repo/ :** contains repo-based co-changes
    - File **source_target_evolution.csv :** contains source, target, source_repo, target_repo identified by depends-on attribute.

2. The folder *Files/Number/* contains the following files, along with their description:
    - **depends_on.csv :** related changes obtained using depends-on attribute.
    - **related_bug.csv :** related changes obtained using related-bug attribute:
    - **change_id.csv :** related changes obtained using change-id attribute.
    - **extended_paths.csv :** chains of related changes.

3. The folder *Files/Repo/* contains the following files, along with their descriptio
    - **extended_paths.csv :** repository-based co-changes, produced using the extended_paths.csv located at *Files/Number/*
    <!-- - **metrics.csv :** /Files/Repo/metrics.csv -->

4. External resources:
    - All external files can be found on onedrive through these links 
    [link](https://etsmtl365-my.sharepoint.com/:f:/r/personal/ali_arabat_1_ens_etsmtl_ca/Documents/Co-evolution%20of%20Multi-component%20systems?csf=1&web=1&e=0zgkJt). It contains file (i.e., pq_services_metrics.csv should be copied to */RQs/PQ/Files*) to conduct PQ, the results of our manually analyzed 100 cross-project changes (i.e., study_sample.csv), and dependencies file (i.e., all_dependencies.csv should be copied to */Files*) between OpenStack changes containing all metrics used to analyze all RQs.

## How each research question is addressed

It should be noted that along the aforementioned scripts, each research question has its own file analysis script which exists at the root of the projects. 