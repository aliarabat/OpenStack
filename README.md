# This is a quick description on how to use this project

This tool was primarily written in python programming language, since it is the most widely used in data science field, with the massive community surrounding it. This project was developed in the context of analyzing the co-evolution of software ecosystem, especially among Openstack components. Therefore, this tool is well-structured to ensure it's easy to use for newcomers.

The projects is organized as follows:

1. **Changes directory :** the main data source used in this project, it contains csv file.
2. **File directory :** generated csv files are generated here for further analysis.
3. **Scripts :** contains all scripts to run from data collection to data analysis

## How to use the project

1. First, you need to run the script called *openstack-data-collection.py*, to get the required data in json format. Since *Changes* directory is already exist, you can skip both 1st and 2nd steps. There is **no input** for this script, but the **output** is a Changes folder containing the json files.
2. Second, you have to execute the *openstack-data-transform.py* in order to transform the json files obtained in the previous step into convenient csv files. The **input** would be the json files of the 1st step, and 4 sets of folders will be generated as **outputs** (Changes, Reviewers, Messages, Files), they are in a CSV format.
3. The third steps consists of running *openstack-data-cleaning.py*, this will parse commit messages to retrieve depends-on values that we are more interested in, to study such co-changes. Thus, the **input** is **Changes files** of the previous, and the **output** is a csv file named **clean_openstack_evolution.csv**, where the columns are *Source,Target,Source_repo,Target_repo*.
4. Finally, run the 5th script *openstack-evolution-generation.py*, the **input** is **clean_openstack_evolution.csv**, this will produce CSV files where each line represents the co-changing Openstack components, *co_evolution_number.csv* containing the co-changing components in number(id(s)) and *co_evolution_repo.csv* consists of reposotories' names isntead of numbers. *os_nodes.csv* contains all the nodes(mapping of number and their corresponding repository names) of openstack, *os_edges.csv* contains all the edges(*Source and Target*).

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

- all_paths.csv : https://drive.google.com/file/d/1vZWYjYs45E__iwoBg9cFTI4f-COv1ZcQ/view?usp=sharing
- extended_paths.csv : /Co-changes/Repo/extended_paths.csv
- metrics.csv : /Co-changes/Repo/metrics.csv