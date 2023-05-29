from sklearn.naive_bayes import GaussianNB
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold, cross_val_score
from sklearn.preprocessing import Normalizer, StandardScaler, MinMaxScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier

type_of_glass = {
    1: 'building_windows_float_processed',
    2: 'building_windows_non_float_processed',
    3: 'vehicle_windows_float_processed',
    4: 'vehicle_windows_non_float_processed',
    5: 'containers',
    6: 'tableware',
    7: 'headlamps'
}

def read_data():
    df = pd.read_csv("glass.data",names=['ID','RI','Na','Mg','Al','Si','K','Ca','Ba','Fe','Type_int'],header=None)
    return df

def normalization(X):
    scaler = MinMaxScaler(feature_range=(0, 10))
    X = scaler.fit_transform(X=X)
    return X

def normalization_v2(X):
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    return X_scaled


def evaluate_model(X, y, model,scaling_X):
    X_scaled = scaling_X(X)

    scores = cross_val_score(model, X_scaled, y, cv=5)  # Walidacja krzyżowa z 5 podziałami
    print("{:^} {:^} {:^} {:^}".format(scores,scores.mean(),scaling_X.__name__,model.__class__.__name__))


df = read_data()

X = df.drop(['ID','Type_int'], axis=1)
y = df['Type_int']

logistic_reg = LogisticRegression(max_iter=1000)
random_forest = RandomForestClassifier()
decision_tree = DecisionTreeClassifier()
gradient_boosting = GradientBoostingClassifier()
gauss = GaussianNB()
# print("{:^} {:^} {:^} {:^}".format("tablica wynikow","Sredni wynik","sposob przetworzenia","Klasyfikator"))
#
# evaluate_model(X, y, logistic_reg,normalization)
# evaluate_model(X, y, random_forest,normalization)
# evaluate_model(X, y, decision_tree,normalization)
# evaluate_model(X, y, gradient_boosting,normalization)
# evaluate_model(X, y, gauss,normalization)






