import warnings

import pandas as pd
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.exceptions import UndefinedMetricWarning
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split, cross_validate
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import KBinsDiscretizer, MinMaxScaler
from sklearn.tree import DecisionTreeClassifier

from Analyse import *

type_of_glass = {
    1: 'building_windows_float_processed',
    2: 'building_windows_non_float_processed',
    3: 'vehicle_windows_float_processed',
    4: 'vehicle_windows_non_float_processed',
    5: 'containers',
    6: 'tableware',
    7: 'headlamps'
}

results = pd.DataFrame(
    columns=['mean_result_acc', 'mean_result_prec', 'mean_result_recall', 'mean_result_f1', 'processing_method',
             'model_name', 'cross'])

# Przetwarzanie parametry
PCA_N_COMPONENTS = 6
DISCRETIZATION_N_BINS = 5
NORMALIZATION_MAX_RANGE = 100

# Modele hiperparametry
hyper_params = {
    'LOGISTIC_REGRESSION_C': [0.1, 1.0, 10.0],
    'DECISION_TREE_MAX_DEPTH': [3, 5, 7],
    'DECISION_TREE_MIN_SAMPLES_SPLIT': [2, 5, 10],
    'DECISION_TREE_CRITERION': ['gini', 'entropy','log_loss'],
    'RANDOM_FOREST_N_ESTIMATORS': [50, 100, 200],
    'RANDOM_FOREST_MAX_DEPTH': [5, 10, 15],
    'RANDOM_FOREST_MIN_SAMPLES_SPLIT': [2, 4, 6]
}


def read_data():
    df = pd.read_csv("glass.data", names=['ID', 'RI', 'Na', 'Mg', 'Al', 'Si', 'K', 'Ca', 'Ba', 'Fe', 'Type_int'],
                     header=None)
    return df


def nothing(X):
    return X


def normalization(X):
    scaler = MinMaxScaler(feature_range=(0, NORMALIZATION_MAX_RANGE))
    X = scaler.fit_transform(X)
    return X


def discretization(X):
    discretizer = KBinsDiscretizer(n_bins=DISCRETIZATION_N_BINS, encode='ordinal', strategy='uniform')
    X_discretized = discretizer.fit_transform(X)
    return X_discretized


def pca(X):
    pca = PCA(n_components=PCA_N_COMPONENTS)
    X_pca = pca.fit_transform(X)
    return X_pca


def evaluate_model_cross(X, y, model, scaling_X):
    X_scaled = scaling_X(X)

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UndefinedMetricWarning)
        scores = cross_validate(model, X_scaled, y, cv=5,
                                scoring=['accuracy', 'precision_macro', 'recall_macro', 'f1_macro'])

    new_row = [scores['test_accuracy'].mean(),
               scores['test_precision_macro'].mean(),
               scores['test_recall_macro'].mean(),
               scores['test_f1_macro'].mean(),
               scaling_X.__name__,
               model.__class__.__name__,
               True]

    results.loc[len(results)] = new_row


def evaluate_model_split(X, y, model, scaling_X):
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.3, random_state=0)

    X_train_scaled = scaling_X(X_train)
    X_val_scaled = scaling_X(X_val)

    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_val_scaled)

    accuracy = accuracy_score(y_val, y_pred)
    precision = precision_score(y_val, y_pred, average='macro', zero_division=1)
    recall = recall_score(y_val, y_pred, average='macro', zero_division=1)
    f1 = f1_score(y_val, y_pred, average='macro', zero_division=1)

    new_row = [accuracy,
               precision,
               recall,
               f1,
               scaling_X.__name__,
               model.__class__.__name__,
               False]

    results.loc[len(results)] = new_row

for i in range(3):
    for j in range(3):
        for k in range(3):
            df = read_data()

            X = df.drop(['ID', 'Type_int'], axis=1)
            y = df['Type_int']

            params = {
                'LOGISTIC_REGRESSION_C': hyper_params['LOGISTIC_REGRESSION_C'][i],

                'RANDOM_FOREST_N_ESTIMATORS': hyper_params['RANDOM_FOREST_N_ESTIMATORS'][i],
                'RANDOM_FOREST_MAX_DEPTH': hyper_params['RANDOM_FOREST_MAX_DEPTH'][j],
                'RANDOM_FOREST_MIN_SAMPLES_SPLIT':hyper_params['RANDOM_FOREST_MIN_SAMPLES_SPLIT'][k],

                'DECISION_TREE_MAX_DEPTH': hyper_params['DECISION_TREE_MAX_DEPTH'][i],
                'DECISION_TREE_MIN_SAMPLES_SPLIT': hyper_params['DECISION_TREE_MIN_SAMPLES_SPLIT'][j],
                'DECISION_TREE_CRITERION': hyper_params['DECISION_TREE_CRITERION'][k]
            }

            logistic_reg = LogisticRegression(
                max_iter=100000,
                C= params['LOGISTIC_REGRESSION_C']
            )

            random_forest = RandomForestClassifier(
                n_estimators=params['RANDOM_FOREST_N_ESTIMATORS'],
                max_depth=params['RANDOM_FOREST_MAX_DEPTH'],
                min_samples_split=params['RANDOM_FOREST_MIN_SAMPLES_SPLIT']
            )

            decision_tree = DecisionTreeClassifier(
                max_depth=params['DECISION_TREE_MAX_DEPTH'],
                min_samples_split=params['DECISION_TREE_MIN_SAMPLES_SPLIT'],
                criterion=params['DECISION_TREE_CRITERION']
            )

            gauss = GaussianNB()

            model_list = [logistic_reg, random_forest, decision_tree, gauss]
            processing_methods_list = [normalization, discretization, pca, nothing]

            for proc_method in processing_methods_list:
                for model in model_list:
                    df = read_data()
                    X = df.drop(['ID', 'Type_int'], axis=1)
                    y = df['Type_int']
                    evaluate_model_cross(X, y, model, proc_method)
                    evaluate_model_split(X, y, model, proc_method)

            showCharts(results, True, 'model_name',params)
            # showCharts(results, True, 'processing_method')
            # showCharts(results, True, ['processing_method', 'model_name'])

#
# print(f"{50 * '#'} Processing {50 * '#'}")
# print(f"{50 * '-'} Cross {50 * '-'}")
# print(results[results['cross'] == True].groupby('processing_method').mean(float).to_string())
# print(f"{50 * '-'} Split {50 * '-'}")
# print(results[results['cross'] == False].groupby('processing_method').mean(float).to_string())
#
# print(f"{50 * '#'} Modeling {50 * '#'}")
# print(f"{50 * '-'} Cross {50 * '-'}")
# print(results[results['cross'] == True].groupby('model_name').mean(float).to_string())
# print(f"{50 * '-'} Split {50 * '-'}")
# print(results[results['cross'] == False].groupby('model_name').mean(float).to_string())
#
# print(f"{50 * '#'} ALL {50 * '#'}")
# print(f"{50 * '-'} Cross {50 * '-'}")
# print(results[results['cross'] == True].groupby(['model_name', 'processing_method']).mean(float).to_string())
# print(f"{50 * '-'} Split {50 * '-'}")
# print(results[results['cross'] == False].groupby(['model_name', 'processing_method']).mean(float).to_string())

# ----------------------------------------- WYKRESY





