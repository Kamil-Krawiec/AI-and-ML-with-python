import json
import time

import numpy as np
from matplotlib import pyplot as plt


def showCharts(results, if_cross, group_by_model, hyper_params, mean):

    split_results = results[results['cross'] == if_cross]

    param_x = ['model_name','processing_method'] if group_by_model else 'processing_method'

    grouped_df = split_results.groupby(param_x).mean(float) if mean else split_results.groupby(param_x).max(float)

    grouped_df['labels'] = grouped_df.index.map(lambda x: x[0][:3]+'-'+x[1][:3])

    metrics = ['mean_result_acc', 'mean_result_prec', 'mean_result_recall', 'mean_result_f1']
    labels = ['Accuracy', 'Precision', 'Recall', 'F1-score']

    colors = ['blue', 'green', 'red', 'orange']

    plt.figure(figsize=(45, 25))

    # Iteruj po każdej mierze i rysuj słupki dla każdego modelu
    for i, metric in enumerate(metrics):
        plt.bar(np.arange(len(grouped_df)) + i * 0.15, grouped_df[metric], width=0.15, label=labels[i],
                color=colors[i])
        # Dodaj wartości wyników nad słupkami
        for j, value in enumerate(grouped_df[metric]):
            plt.text(j + i * 0.15, value + 0.01, round(value, 3), ha='center', fontsize=30,rotation=90)

    plt.xlabel(param_x, fontsize=30)
    plt.ylabel('Score', fontsize=30)
    plt.yticks(fontsize=30)
    plt.title(f'{"Mean" if mean else "Max" } Scores for Different types of {str(param_x)} {"cross" if if_cross else "split"} validation',
              fontsize=35)

    plt.xticks(np.arange(len(grouped_df)), grouped_df['labels'], fontsize=40,rotation=0)
    plt.legend(loc='upper center', fontsize=25)
    plt.text((len(grouped_df)) / 2 -0.89, -0.3,
             json.dumps(hyper_params, indent=4),
             bbox=dict(boxstyle='round',facecolor='white', edgecolor='gray', alpha=0.7),
             fontsize=25, ha='left', wrap=True)
    plt.tight_layout()
    plt.savefig(f'./Charts/{"Models" if group_by_model else "Processing"}/{time.time()}_plot.png')
    plt.close()
