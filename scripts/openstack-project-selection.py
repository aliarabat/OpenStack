import requests
import re
import csv
from github import Github
from itertools import chain
import pandas as pd
import sys
sys.path.append('../utils')
import helpers as hpr

owner = 'openstack'
token = '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'

def getGitRepos(owner):
    g = Github(token)
    org = g.get_organization(owner)
    repos = org.get_repos()
    return [repo.ssh_url.split('/')[-1].replace('.git','') for repo in repos]


def getProjectsFromReleaseNotes(repoList):
    release_url = 'https://releases.openstack.org/index.html'
    release_page = requests.get(release_url)
    components = [word.split('/')[1].split('.')[0] for word in release_page.text.split() if 'teams/' in word]
    repos = list()
    Map = dict()
    for component in components:
        url = 'https://releases.openstack.org/teams/' + component + '.html'
        page = requests.get(url)
        tmp = [word.replace('<td><p>', '').replace('</p></td>', '').replace('openstack/','')
               for word in page.text.split() if (word.startswith('<td><p>openstack/')
                 and word.replace('<td><p>', '').replace('</p></td>', '').replace('openstack/','') in repoList)]
        repos += tmp
        Map[re.compile('[^a-zA-Z]').sub('', component)] = list(set(tmp))

    return Map


def getProjectsUsingKeywords(repoList, input_path):
    input = open(input_path, 'r', encoding='utf-8', newline='')
    CSVreader = csv.reader(input, delimiter=',')
    next(CSVreader)

    Map = dict()

    for line in CSVreader:
        component = line[0].lower()
        repos = [repo for repo in repoList if re.compile('[^a-zA-Z]').sub('', component) in re.compile('[^a-zA-Z]').sub('', repo)]
        if repos:
            repos = list(dict.fromkeys(repos))
            Map[re.compile('[^a-zA-Z]').sub('', component)] = repos
        else:
            repos = list()
            for cmp in component.split('-'):
                repos += [repo for repo in repoList if (re.compile('[^a-zA-Z]').sub('', cmp) in re.compile('[^a-zA-Z]').sub('', repo) and cmp != 'openstack')]
            repos = list(dict.fromkeys(repos))
            Map[re.compile('[^a-zA-Z]').sub('', component)] = repos

    return Map


def merge(Map,Map2):
    finalMap = Map
    for key in list(Map2.keys()):
        if key in list(finalMap.keys()):
            finalMap[key] += Map2[key]
            finalMap[key] = list(set(finalMap[key]))
        else:
            finalMap[key] = Map2[key]

    return finalMap


if __name__ == '__main__':
    input_path = 'OpenStackComponents.csv'
    output_path = 'OpenStackRepos.csv'

    repoList = getGitRepos(owner, token)
    print(len(repoList))
    repoList += getGitRepos("openstack-archive", token)
    print(len(repoList))
    repos_RN = getProjectsFromReleaseNotes(repoList)
    reamining_projects = [item for item in repoList if item not in hpr.flatten_list(list(repos_RN.values()))]
    repos_KEY = getProjectsUsingKeywords(reamining_projects, input_path)
    merged_repos = merge(repos_KEY, repos_RN)

    for k, v in merged_repos.items():
        current_keys = [item for item in list(merged_repos.keys()) if item != k]
        old_list = merged_repos.get(k)
        merged_repos[k] = [item for item in old_list if item not in current_keys]

    df_projects_mapping = pd.DataFrame({"main_project": merged_repos.keys(), "related_projects": merged_repos.values()})
    # df_projects_mapping = pd.DataFrame({"main_project": repos_RN.keys(), "related_projects": repos_RN.values()})
    df_projects_mapping["count"] = df_projects_mapping["related_projects"].map(lambda x: len(x))
    df_projects_mapping.loc[df_projects_mapping["count"] > 0, ["main_project", "related_projects"]].to_csv("./all_os_components.csv", index=False)

    values = list(merged_repos.values())
    # values = list(repos_RN.values())
    final_repo_list = list(set(chain.from_iterable(values))) #flatten the 2D array and remove duplicates
    outputCSV = open(output_path, 'w', encoding='utf-8', newline='')
    CSVwriter = csv.writer(outputCSV, delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
    header = ['repo']
    CSVwriter.writerow(header)
    for repo in final_repo_list:
        CSVwriter.writerow([repo])

    # non_associated_projects = [item for item in repoList if item not in hpr.flatten_list(list(merged_repos.values()))]

    # pd.DataFrame({"project": non_associated_projects}).to_csv("./non_associated_projects.csv", index=False)