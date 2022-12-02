# This is a quick description on how to use this project

This tool was primarily written in python programming language, since it is the most widely used
in data science field, with the massive community surrounding it. This project was developed in
the context of analyzing the co-evolution of software ecosystem, especially among Openstack components.
Therefore, this tool is well-structured to ensure it's easy to use for newcomers.

The projects is organized as follows:

1. **Data directory :** the main data source used in this project, it contains csv file.
2. **File directory :** generated csv files are generated here for further analysis.
3. **Scripts :** contains all scripts to run from data collection to data analysis

## How to use the project

1. First, you need to run the script called *openstack-data-collection.py*, to get the required data in json format.
Since *Data* directory is already exist, you can skip both 1st and 2nd steps.
2. Second, you have to execute the *openstack-data-transform.py* in order to transform the json files obtained
in the previous step into convenient csv files.
3. The third steps consists of running *openstack-data-cleaning.py*, this will parse commit messages to retrieve
depends-on values that we are more interested in, to study such co-changes.
4. Next, execute the script named *openstack-data-manipulation.py* to get a four-column csv file that will be used for
further steps
5. Finally, run the 5th script *openstack-evolution-generation.py*, this will produce csv file where each line represents
the co-changing Openstack components.

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

It is not suggested to run all the scripts at once, since it will too much time. Since the Data folder contains all files to
play with you can go directly to the third step
