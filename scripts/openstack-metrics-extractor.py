import pandas as pd  # for data manipulation
from efficient_apriori import apriori  # for association analysis
import ast
import helpers as hpr


def retrieve_metrics():
    '''Metrics retrieval from generated association rules
    '''
    metrics = []

    # Ingest the data
    df = pd.read_csv("%sFiles/Repo/extended_paths.csv" % hpr.DIR)

    df = df["Path"].apply(ast.literal_eval).values.tolist()

    # Runing the Apriori algorithm and save itemsets and association rules
    itemsets, rules = apriori(df, min_support=0.0018, min_confidence=0.02, verbosity=0)

    # sort results by lift then confidence descending
    items = sorted(rules,
                   key=lambda item: (item.lift, item.confidence),
                   reverse=True)

    for item in items:
        new_metric = {
            "antecedents": list(item.lhs),
            "consequents": list(item.rhs),
            "antecedent_support": count_support(df, list(item.lhs)),
            "consequent_support": count_support(df, list(item.rhs)),
            "support": item.support,
            "confidence": item.confidence,
            "lift": item.lift
        }

        metrics.append(new_metric)

    return metrics


def count_support(data, search_item):
    '''Count frequency distribution of search_item in data
    '''
    result = 0
    for data_item in data:
        if all(item in data_item for item in search_item):
            result += 1
    return result / len(data)


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
