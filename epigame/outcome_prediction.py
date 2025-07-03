import os
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score
from pickle import load
from itertools import combinations
from collections import defaultdict

def load_all_subjects_scores(score_dir, subject_ids):
    data = defaultdict(dict)
    for sub in subject_ids:
        file_path = os.path.join(score_dir, f"scores_sub{sub}.p")
        if os.path.exists(file_path):
            sub_result = load(open(file_path, "rb"))
            for (cm, sigma), result in sub_result.items():
                data[(cm, sigma)][sub] = result
        else:
            print(f"Missing file: {file_path}")
    return data

def compute_mean_scores_per_subject(data, selected_cms, target_sigma, outcome_df):
    subjects = sorted({sub for (cm, s), result in data.items() if s == target_sigma for sub in result})
    X, y = [], []

    for sub in subjects:
        cm_scores = []
        for cm in selected_cms:
            sigma = target_sigma
            score = 0
            # recursively check lower sigma values if overlap_ratio is 0
            while sigma >= 1:
                entry = data.get((cm, sigma), {}).get(sub)
                if entry:
                    score = entry['overlap_ratio']
                    if score != 0:
                        break
                sigma -= 1
            if score:
                cm_scores.append(score)
        if cm_scores:
            X.append(np.mean(cm_scores))
            sub_outcome = outcome_df.loc[outcome_df['subject_id'] == sub, 'outcome']
            if not sub_outcome.empty:
                y.append(int(sub_outcome.values[0]))

    return np.array(X), np.array(y), subjects

def compute_roc_auc(X, y):
    return roc_auc_score(y, X) if len(set(y)) > 1 else np.nan

def run_outcome_prediction(score_dir, subject_ids, sigma=4, max_n_cms=5, outcome_path="data/input/outcomes.xlsx"):
    data = load_all_subjects_scores(score_dir, subject_ids)
    outcome_df = pd.read_excel(outcome_path)
    all_cms = sorted(set(cm for (cm, s) in data if s == sigma))

    results = []
    for k in range(1, max_n_cms+1):
        for subset in combinations(all_cms, k):
            X, y, subjects = compute_mean_scores_per_subject(data, subset, sigma, outcome_df)
            if len(X) > 0:
                auc = compute_roc_auc(X, y)
                results.append({
                    'CM_combination': subset,
                    'n_CMs': k,
                    'ROC_AUC': auc,
                    'N_subjects': len(subjects)
                })
    df_results = pd.DataFrame(results).sort_values(by='ROC_AUC', ascending=False)
    df_results.to_excel("data/output/outcome_prediction_results.xlsx", index=False)

    return df_results

