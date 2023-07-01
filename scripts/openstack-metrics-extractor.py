import pandas as pd  # for data manipulation
from efficient_apriori import apriori  # for association analysis
import ast
import sys
sys.path.append('../utils')
import helpers as hpr


def retrieve_metrics():
    '''Metrics retrieval from generated association rules
    '''

    # Ingest the data
    df = pd.read_csv("%sFiles/Repo/extended_paths.csv" % hpr.DIR)

    df = df["Path"].apply(ast.literal_eval).values.tolist()

    # Runing the Apriori algorithm and save itemsets and association rules
    itemsets, rules = apriori(df, min_support=0.0018, min_confidence=0.02, verbosity=0)

    # sort results by lift then confidence descending
    items = sorted(rules,
                   key=lambda item: (item.lift, item.confidence),
                   reverse=True)

    metrics_list = {
        "Repo_A": [],
        "Repo_B": [],
        "Support_A": [],
        "Support_B": [],
        "Support_A_B": [],
        "Confidence_A_B": [],
        "Confidence_B_A": [],
        "Lift_A_B": [],
        "Lift_B_A": []
    }

    for i in range(len(items[:30])):

        item = items[i]

        repo_a = list(item.lhs)

        support_a = compute_support(df, repo_a)

        repo_b = list(item.rhs)
        support_b = compute_support(df, repo_b)

        support = item.support

        confidence_a_b = item.confidence
        confidence_b_a = compute_confidence(df, repo_b, repo_a)

        lift_a_b = item.lift
        lift_b_a = compute_lift(df, repo_b, repo_a)

        new_list_repo_a = metrics_list.get("Repo_A") + [" ".join(sorted(repo_a))]
        new_list_repo_b = metrics_list.get("Repo_B") + [" ".join(sorted(repo_b))]
        metrics_list.update({"Repo_A": new_list_repo_a})
        metrics_list.update({"Repo_B": new_list_repo_b})

        new_list_support_a = metrics_list.get("Support_A") + [support_a]
        new_list_support_b = metrics_list.get("Support_B") + [support_b]
        metrics_list.update({"Support_A": new_list_support_a})
        metrics_list.update({"Support_B": new_list_support_b})

        new_list_support = metrics_list.get("Support_A_B") + [support]
        metrics_list.update({"Support_A_B": new_list_support})

        new_list_confidence_a_b = metrics_list.get("Confidence_A_B") + [confidence_a_b]
        new_list_confidence_b_a = metrics_list.get("Confidence_B_A") + [confidence_b_a]
        metrics_list.update({"Confidence_A_B": new_list_confidence_a_b})
        metrics_list.update({"Confidence_B_A": new_list_confidence_b_a})

        new_list_lift_a_b = metrics_list.get("Lift_A_B") + [lift_a_b]
        new_list_lift_b_a = metrics_list.get("Lift_B_A") + [lift_b_a]
        metrics_list.update({"Lift_A_B": new_list_lift_a_b})
        metrics_list.update({"Lift_B_A": new_list_lift_b_a})

    return metrics_list


def compute_support(data, search_item):
    '''Count frequency distribution of search_item in data
    '''
    result = 0
    for data_item in data:
        if all(item in data_item for item in search_item):
            result += 1
    return result / len(data)

def compute_confidence(data, item1, item2):
    '''Compute confidence between item1 and item2
    '''
    support1 = compute_support(data, item1 + item2)
    support2 = compute_support(data, item1)
    return support1/support2

def compute_lift(data, item1, item2):
    '''Compute lift between item1 and item2
    '''
    confidence = compute_confidence(data, item1, item2)
    support = compute_support(data, item2)
    return confidence/support


if __name__ == "__main__":

    print("Script openstack-metrics-extractor.py started...")

    start_date, start_header = hpr.generate_date("This script started at")

    metrics = retrieve_metrics()

    # Save data in a csv file
    pd.DataFrame(metrics).to_csv("%sFiles/Metrics/association_rules.csv" % hpr.DIR, index=False)

    print("/Files/Repo/metrics.csv generated successfully")

    end_date, end_header = hpr.generate_date("This script ended at")

    print(start_header)

    print(end_header)

    hpr.diff_dates(start_date, end_date)

    print("Script openstack-metrics-extractor.py ended\n")
