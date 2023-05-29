import json

import numpy as np
from matplotlib import pyplot as plt


def showCharts(results, if_cross, group_by,params):
    split_results = results[results['cross'] == if_cross]
    param_x = "models" if group_by == "model_name" else "processing"

    # Grupowanie wyników według nazwy modelu
    grouped_df = split_results.groupby(group_by).mean(float)
    metrics = ['mean_result_acc', 'mean_result_prec', 'mean_result_recall', 'mean_result_f1']
    labels = ['Accuracy', 'Precision', 'Recall', 'F1-score']

    # Wybierz kolory dla każdej miary
    colors = ['blue', 'green', 'red', 'orange']

    # Tworzenie wykresu
    plt.figure(figsize=(30, 20))

    # Iteruj po każdej miarze i rysuj słupki dla każdego modelu
    for i, metric in enumerate(metrics):
        plt.bar(np.arange(len(grouped_df)) + i * 0.15, grouped_df[metric], width=0.15, label=labels[i],
                color=colors[i])
        # Dodaj wartości wyników nad słupkami
        for j, value in enumerate(grouped_df[metric]):
            plt.text(j + i * 0.15, value + 0.01, round(value, 3), ha='center', fontsize=25)

    plt.xlabel(param_x, fontsize=30)
    plt.ylabel('Score', fontsize=30)
    plt.yticks(fontsize=30)
    plt.title(f'Mean Scores for Different types of {param_x} {"cross" if if_cross else "split"} validation',
              fontsize=35)
    plt.xticks(np.arange(len(grouped_df)), grouped_df.index, fontsize=30)
    plt.legend(loc='upper left', fontsize=25)
    plt.text((len(grouped_df))/2 -1 , -0.25, json.dumps(params, indent=4), fontsize=25, ha='left')

    plt.tight_layout()
    plt.show()
