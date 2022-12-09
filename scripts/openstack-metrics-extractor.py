import pandas as pd  # for data manipulation
from efficient_apriori import apriori  # for association analysis
import ast
import helpers as hpr

def retrieve_metrics():
    '''Calculate metrics for the Openstack generated paths
    '''
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

    for i in range(len(items)):
        if i % 2 == 0:

            item = items[i]
            next_item = items[i + 1]
            if item.lhs[0] == next_item.rhs[0] and item.rhs[0] == next_item.lhs[0]:
                repo_a = item.lhs[0]
                support_a = df.count([repo_a]) / transactions_length

                repo_b = item.rhs[0]
                support_b = df.count([repo_b]) / transactions_length

                support_a_b = item.support

                confidence_a_b = item.confidence
                confidence_b_a = next_item.confidence

                lift_a_b = item.lift
                lift_b_a = next_item.lift

                metrics_list.update({
                    "Repo_A": metrics_list.get("Repo_A") + [repo_a],
                    "Repo_B": metrics_list.get("Repo_B") + [repo_b],
                    "Support_A": metrics_list.get("Support_A") + [support_a],
                    "Support_B": metrics_list.get("Support_B") + [support_b],
                    "Support_A_B": metrics_list.get("Support_A_B") + [support_a_b],
                    "Confidence_A_B": metrics_list.get("Confidence_A_B") + [confidence_a_b],
                    "Confidence_B_A": metrics_list.get("Confidence_B_A") + [confidence_b_a],
                    "Lift_A_B": metrics_list.get("Lift_A_B") + [lift_a_b],
                    "Lift_B_A": metrics_list.get("Lift_B_A") + [lift_b_a]
                })

    return metrics_list


if __name__ == "__main__":

    print("Script openstack-metrics-extractor.py started...")

    start_date, start_header = hpr.generate_date("This script started at")

    # Ingest the data
    df = pd.read_csv("%sFiles/Repo/extended_paths.csv" % hpr.DIR)

    df = df["Path"].apply(ast.literal_eval).values.tolist()

    # Runing the Apriori algorithm and save itemsets and association rules
    itemsets, rules = apriori(df, min_support=0.001, min_confidence=0.001)

    # sort results by lift then confidence descending
    items = sorted(rules, key=lambda item: (item.lift, item.confidence), reverse=True)

    # length of all transactions
    transactions_length = len(df)

    # retrieve metrics
    metrics_list = retrieve_metrics()

    # Save data in a csv file
    pd.DataFrame(metrics_list).to_csv("%sFiles/Repo/metrics.csv" % hpr.DIR, index=False)

    print("/Files/Repo/metrics.csv generated successfully")

    end_date, end_header = hpr.generate_date("This script ended at")

    print(start_header)

    print(end_header)

    hpr.diff_dates(start_date, end_date)

    print("Script openstack-metrics-extractor.py ended\n")
