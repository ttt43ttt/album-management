"""
Evaluation for the clustering algorithms.
"""
from collections import defaultdict
from itertools import combinations

def f1_score(labels_true, labels_pred):
    # {id1: label1, id2: label2}
    label_lookup = {}
    for (i, label) in enumerate(labels_true):
        label_lookup[i] = label

    # {label1: [id1,id2], label2: [id3,id4]}
    cluster_lookup = {}
    for (i, label) in enumerate(labels_pred):
        if label in cluster_lookup:
            ids = cluster_lookup[label]
        else:
            ids = []
            cluster_lookup[label] = ids
        ids.append(i)

    # [[id1,id2], [id3,id4,id5]]
    clusters = []
    for ids in cluster_lookup.values():
        clusters.append(ids)

    correct_pairs, total_pairs, true_pairs, precision, recall, f_score = f1_score_metrics(clusters, label_lookup)
    # print(f"correct_pairs:{correct_pairs}, total_pairs:{total_pairs}, true_pairs:{true_pairs}, precision:{precision}, recall:{recall}, f_score:{f_score}")
    return f_score

def f1_score_metrics(clusters, label_lookup):
    """
    Given a cluster, return pairwise precision and recall.

    Approximate Rank-Order Clustering (AROC) algorithm.
    https://arxiv.org/abs/1604.00989
    """
    def _count_correct_pairs(cluster, label_lookup):
        """
        Given a cluster, count the number of pairs belong to the same label and
        the total number of pairs.
        """
        total_pairs = 0
        correct_pairs = 0
        pairs = combinations(cluster, 2)
        for idx1, idx2 in pairs:
            if label_lookup[idx1] == label_lookup[idx2]:
                correct_pairs += 1
            total_pairs += 1

        return correct_pairs, total_pairs

    correct_pairs = 0
    total_pairs = 0
    for cluster in clusters:
        correct_pair, total_pair = _count_correct_pairs(
            cluster, label_lookup)
        correct_pairs += correct_pair
        total_pairs += total_pair

    gt_clusters = defaultdict(list)
    for row_no, label in label_lookup.items():
        gt_clusters[label].append(row_no)

    true_pairs = 0
    for _, cluster_items in gt_clusters.items():
        cluster_len = len(cluster_items)
        true_pairs += cluster_len * (cluster_len - 1) / 2.0

    precision = float(correct_pairs) / total_pairs
    recall = float(correct_pairs) / true_pairs
    f_score = 2.0 * (precision * recall) / (precision + recall) \
        if precision + recall > 0 else 0

    return correct_pairs, total_pairs, true_pairs, precision, recall, f_score
