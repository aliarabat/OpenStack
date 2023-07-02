import pandas as pd
import numpy as np
import re
import networkx as nx
import utils.helpers as hpr
import ast
import collections
import requests as rq
from bs4 import BeautifulSoup
import re


def get_teams_projects():
    """Services are then extended with teams
    """
    request = rq.get("https://releases.openstack.org/")
    soup = BeautifulSoup(request.text, 'html.parser')

    openstack_teams = {}

    team_section = soup.find(id= "teams")
    li_list = team_section.find_all("li")
    for i in range(len(li_list)):

        link = li_list[i].find("a")
        link_suffix = link["href"]

        request_projects = rq.get("https://releases.openstack.org/%s" % (link_suffix))
        soup_projects = BeautifulSoup(request_projects.text, 'html.parser')
        table_of_contents = soup_projects.find("div", attrs={"id": "table-of-contents"})
        ul_projects = table_of_contents.find("ul")
        ul_projects = ul_projects.find("ul")
        ul_projects = ul_projects.find_all("ul")
        projects = []
        for ul_item in ul_projects:

            href_projects = ul_item.find_all("a")

            for href_project in href_projects:
                project = href_project.text.replace(" (EOL)", "")
                if project in openstack_changes_projects:
                    projects.append(project)
                # href_links_projects = soup_projects.find_all("a", "reference internal")
        team = li_list[i].text
        team = re.compile('[^a-zA-Z]').sub('',  team.lower())
        openstack_teams[team] = list(dict.fromkeys(projects))
    return openstack_teams


def get_teams_deliverables():
    """Get project team deliverables
    """
    request_teams = rq.get("https://governance.openstack.org/tc/reference/projects/index.html")
    soup_teams = BeautifulSoup(request_teams.text, 'html.parser')

    teams_deliverables = {}
    href_links_teams = soup_teams.find_all("a", "reference internal")

    for i in range(1, len(href_links_teams)-2):
        link = href_links_teams[i]
        link_suffix = link["href"]

        request_projects = rq.get("https://governance.openstack.org/tc/reference/projects/%s" % (link_suffix))
        soup_projects = BeautifulSoup(request_projects.text, 'html.parser')
        href_links_projects = soup_projects.find_all("a", "reference internal")

        projects = [href_links_projects[j].text for j in range(3, len(href_links_projects))]
        projects = [p for p in projects if p in openstack_changes_projects]
        teams_deliverables[link_suffix[:-5].replace("-", "")] = projects
    return teams_deliverables


def merge(Map,Map2):
    """Merge two dictionaries
    """
    finalMap = Map
    for key in list(Map2.keys()):
        if key in list(finalMap.keys()):
            finalMap[key] += Map2[key]
            finalMap[key] = list(set(finalMap[key]))
        else:
            finalMap[key] = Map2[key]

    return finalMap


def switch_projects_are_services(all_services):
    """Switch projects between services
    """
    services = all_services.keys()
    projects_services = []
    result = all_services.keys()
    for k,v in all_services.items():
        projects_services.append(list(set(v).intersection(services)))
        new_projects = list(set(v).difference(services))
        result[k] = new_projects
    projects_services = hpr.flatten_list(projects_services)
    for k,v in all_services.items():
        if k in projects_services:
            new_list = list(dict.fromkeys(v + [k]))
            result[k] = new_list
    return result


def link_project_keyword(all_services, non_associated_projects):
    """Link projects using regular expressions
    """
    Map = dict()
    for k in all_services.keys():   
        re.compile('[^a-zA-Z]').sub('', k)
        repos = [repo for repo in non_associated_projects if k in re.compile('[^a-zA-Z]').sub('', repo)]
        if repos:
            repos = list(dict.fromkeys(repos))
            Map[k] = repos
        else:
            repos = list()
            for cmp in k.split('-'):
                repos += [repo for repo in non_associated_projects if (re.compile('[^a-zA-Z]').sub('', cmp) in re.compile('[^a-zA-Z]').sub('', repo) and cmp != 'openstack')]
            repos = list(dict.fromkeys(repos))
            Map[k] = repos
    return Map


if __name__ == '__main__':
    df = hpr.combine_openstack_data()

    openstack_changes_projects = df["project"].unique()
    openstack_changes_projects = [p.replace("openstack/", "") for p in openstack_changes_projects if p.startswith("openstack")]

    # Get services from the OpenStack core services big picture
    core_services = pd.read_csv("./OpenStackComponents.csv")
    core_services = core_services["OpenStack Components"].map(lambda item: re.compile('[^a-zA-Z]').sub('',  item.lower())).values
    core_services = {s: [] for s in core_services}

    # Combine services
    openstack_teams = get_teams_projects()
    all_services = merge(core_services, openstack_teams)

    # Map teams deliverables to services
    teams_deliverables = get_teams_deliverables()
    teams_deliverables_keys = teams_deliverables.keys()
    all_services = {k: list(set((teams_deliverables[k] if k in teams_deliverables_keys else []) + v)) for k,v in all_services.items()}

    # Remove redundant projects
    redundant_projects = collections.Counter(hpr.flatten_list(all_services.values()))
    redundant_projects = pd.DataFrame({"k": redundant_projects.keys(), "v": redundant_projects.values()})
    redundant_projects = redundant_projects.loc[redundant_projects["v"]>1, "k"].values
    for service, projects in all_services.items():
        all_services[service] = [p for p in projects if p not in redundant_projects]

    #### Remaining non associated projects
    associated_projects = hpr.flatten_list(all_services.values())
    non_associated_projects = set(list(redundant_projects) + [p for p in openstack_changes_projects if p not in associated_projects])

    # switch projects that are services
    all_services = switch_projects_are_services(all_services)

    # Link remaining projects
    linked_projects = link_project_keyword()
    
    # Merge two lists of services
    merged_repos = merge(all_services, linked_projects)

    for k, v in merged_repos.items():
        current_keys = [item for item in list(merged_repos.keys()) if item != k]
        old_list = merged_repos.get(k)
        merged_repos[k] = [item for item in old_list if item not in current_keys]

    # Remove redundant projects
    redundant_projects2 = collections.Counter(hpr.flatten_list(merged_repos.values()))
    redundant_projects2 = pd.DataFrame({"k": redundant_projects2.keys(), "v": redundant_projects2.values()})
    redundant_projects2 = redundant_projects2.loc[redundant_projects2["v"]>1, "k"].values
    for service, projects in merged_repos.items():
        merged_repos[service] = [p for p in projects if p not in redundant_projects2]

    # Ceate dataframe for the final list of services with their corresponding projects
    df_all_services = pd.DataFrame({"main_project": merged_repos.keys(), "related_projects":merged_repos.values()})
    df_all_services["count"] = df_all_services["related_projects"].map(len)

    # Save the data
    df_all_services.loc[df_all_services["count"]!=0, ["main_project", "related_projects"]].to_csv("%sall_os_components.csv" % hpr.DIR, index=False)