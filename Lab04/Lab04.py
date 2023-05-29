from sklearn.naive_bayes import GaussianNB
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_validate
from sklearn.preprocessing import KBinsDiscretizer, MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.tree import DecisionTreeClassifier

type_of_glass = {
    1: 'building_windows_float_processed',
    2: 'building_windows_non_float_processed',
    3: 'vehicle_windows_float_processed',
    4: 'vehicle_windows_non_float_processed',
    5: 'containers',
    6: 'tableware',
    7: 'headlamps'
}

results= pd.DataFrame(columns=['mean_result_acc','mean_result_prec','mean_result_recall','mean_result_f1','processing_method','model_name','cross'])

PCA_N_COMPONENTS = 6
DISCRETIZATION_N_BINS = 5
NORMALIZATION_MAX_RANGE = 10

def read_data():
    df = pd.read_csv("glass.data",names=['ID','RI','Na','Mg','Al','Si','K','Ca','Ba','Fe','Type_int'],header=None)
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

def evaluate_model_cross(X, y, model,scaling_X):
    X_scaled = scaling_X(X)

    scores = cross_validate(model, X_scaled, y, cv=5,scoring = ['accuracy', 'precision_macro', 'recall_macro', 'f1_macro'])

    new_row = [ scores['test_accuracy'].mean(),
                scores['test_precision_macro'].mean(),
                scores['test_recall_macro'].mean(),
                scores['test_f1_macro'].mean(),
                scaling_X.__name__,
                model.__class__.__name__,
                True]

    results.loc[len(results)] = new_row

def evaluate_model_split(X, y, model, scaling_X):
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    X_train_scaled = scaling_X(X_train)
    X_val_scaled = scaling_X(X_val)

    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_val_scaled)

    accuracy = accuracy_score(y_val, y_pred)
    precision = precision_score(y_val, y_pred, average='macro')
    recall = recall_score(y_val, y_pred, average='macro')
    f1 = f1_score(y_val, y_pred, average='macro')

    new_row = [accuracy,
               precision,
               recall,
               f1,
               scaling_X.__name__,
               model.__class__.__name__,
               False]

    results.loc[len(results)] = new_row

df = read_data()




X = df.drop(['ID','Type_int'], axis=1)
y = df['Type_int']

logistic_reg = LogisticRegression(max_iter=100000)
random_forest = RandomForestClassifier()
decision_tree = DecisionTreeClassifier()
gauss = GaussianNB()

model_list = [logistic_reg,random_forest,decision_tree,gauss]
processing_methods_list = [normalization,discretization,pca,nothing]

for proc_method in processing_methods_list:
    for model in model_list:
        df = read_data()
        X = df.drop(['ID', 'Type_int'], axis=1)
        y = df['Type_int']
        evaluate_model_cross(X,y,model,proc_method)
        evaluate_model_split(X,y,model,proc_method)


print(results.to_string())
print('Cross')
print(results[results['cross'] == True].groupby('processing_method').mean().to_string())
print('Split')
print(results[results['cross'] == False].groupby('processing_method').mean().to_string())







