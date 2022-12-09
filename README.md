# This is a quick description on how to use this project

This tool was primarily written in python programming language, since it is the most widely used in data science field, with the massive community surrounding it. This project was developed in the context of analyzing the co-evolution of software ecosystem, especially among Openstack components. Therefore, this tool is well-structured to ensure it's easy to use for newcomers.

The projects is organized as follows:

1. **Changes directory :** the main data source used in this project, it contains csv file.
2. **File directory :** generated csv files are generated here for further analysis.
3. **Scripts :** contains all scripts to run from data collection to data analysis

## How to use the project

1. First, you need to run the script called *openstack-data-collection.py*, to get the required data in json format. Since *Changes* directory is already exist, you can skip both 1st and 2nd steps. There is **no input** for this script, but the **output** is a Changes folder containing the json files.
2. Second, you have to execute the *openstack-data-transform.py* in order to transform the json files obtained in the previous step into convenient csv files. The **input** would be the json files of the 1st step, and 4 sets of folders will be generated as **outputs** (Changes, Reviewers, Messages, Files), they are in a CSV format.
3. The third steps consists of running *openstack-data-cleaning.py*, this will parse commit messages to retrieve depends-on values that we are more interested in, to study such co-changes. Thus, the **input** is **Changes files** of the previous, and the **output** is a csv file named **Files/source_target_evolution.csv**, where the columns are *Source,Target,Source_repo,Target_repo*.
4. The fourth step, run the script *openstack-paths-generation.py*, the **input** is **Files/source_target_evolution.csv**, this will produce as **output**, a CSV file named all_paths.csv stored in *experiments/* where each line represents the co-changing Openstack components.
5. This step consist of calling *openstack-paths-extending.py*, which extends the *all_paths.csv* file as **input**, with single-component related changes, in other words, the changes that have no dependencies. This will result in as **output**, two files, 1st one stored in *Files/Number/extended_paths.csv* and second stored in *Files/Repo/extended_paths.csv*. The former contains number-based co-changes while the later contains repository-based co-changes.
6. Finally, one must execute the script *openstack-metrics-extractor.py*, it takes as **input**, *Files/Repo/all_paths.csv*, and produces *Files/Repo/metrics.csv*. The latter file contains metrics about each association rule in the following pattern *Repo_A*, *Repo_B*, *Support_A*, *Support_B*, *Support_A_B*, *Confidence_A_B*, *Confidence_B_A*, *Lift_A_B*, *Lift_B_A*,

## Requirements for this projects

This project requires python version 3 or later to be installed in you machine as well as the following packages :

- pandas
- numpy
- json
- requests
- shutil
- networkx

## How to run each script

There are two ways to run those scripts :

- Execute all scripts at once using the following command `python setup.py`
- Execute a particular script by using calling `python "SCRIPT_NAME".py`

## Important Notice

It is not suggested to run all the scripts at once, since it will too much time. Since the Data folder contains all files to play with you can go directly to the third step

## Links

1. The *Files* folder containes 2 sub-folders and 1 file:
    - **Number/ :** contains number-based co-changes
    - **Repo/ :** contains repo-based co-changes
    - File **source_target_evolution.csv :** contains source, target, source_repo, target_repo identified by depends-on attribute.

2. The folder *Files/Number/* contains the following files, along with their description:
    - **depends_on.csv :** co-changes obtained using depends-on attribute.
    - **related_bug.csv :** co-changes obtained using related-bug attribute:
    - **topic.csv :** co-changes obtained using topic attribute.
    - **subject.csv :** co-changes obtained using subject attribute.
    - **change_id.csv :** co-changes obtained using change-id attribute.
    - **extended_paths.csv :** co-changes obtained using based on all_paths.csv.

3. The folder *Files/Repo/* contains the following files, along with their descriptio
    - **extended_paths.csv :** repository-based co-changes, produced using the extended_paths.csv located at *Files/Number/*
    - **metrics.csv :** /Files/Repo/metrics.csv

4. External resources:
    - **all_paths.csv:** : the result of combination the *depends_on.csv*, *related_bug.csv*, *topic.csv*, *subject.csv* and *change_id.csv* based on common numbers. You can view it using this [link](https://drive.google.com/file/d/1vZWYjYs45E__iwoBg9cFTI4f-COv1ZcQ/view?usp=sharing)