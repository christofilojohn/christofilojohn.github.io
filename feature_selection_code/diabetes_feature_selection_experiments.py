import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix, roc_auc_score
from sklearn.ensemble import RandomForestClassifier


def gnb_experiment(X_train, X_test, y_train, y_test):
    # Train the model
    model = GaussianNB()
    model.fit(X_train, y_train)
    # Predict
    y_pred = model.predict(X_test)

    """
    Evaluate the model performance over the testing set (f1, recall, ...)
    """
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')
    conf_matrix = confusion_matrix(y_test, y_pred)

    # Print the results
    print("Accuracy:", accuracy)
    print("Recall:", recall)
    print("F1 Score:", f1)
    print("Confusion Matrix:\n", conf_matrix)


def select_features_test_model():
    #  Load the data
    df = pd.read_csv('diabetes_012_health_indicators_BRFSS2015.csv')

    """ 1. Whole dataset """
    # prepare, split the data
    X = df.drop('Diabetes_012', axis=1)
    y = df['Diabetes_012']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    gnb_experiment(X_train, X_test, y_train, y_test)

    """ 2. First Feature Selection """
    # Select only the most relevant features as determined by the Random Forest
    selected_features = [
        'BMI',
        'Age',
        'Income',
        'PhysHlth',
        # 'Education',
        'GenHlth',
        # 'MentHlth',
        'HighBP',
        'Fruits',
        'Smoker',
        'Sex',
        'PhysActivity'
    ]

    X = df[selected_features]
    y = df['Diabetes_012']

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    gnb_experiment(X_train, X_test, y_train, y_test)

    """ 3. More complete feature selection """
    # Select only the most relevant features as determined by the Random Forest
    selected_features = [
        'BMI',
        'Age',
        'Income',
        'PhysHlth',
        'Education',
        'GenHlth',
        'MentHlth',
        'HighBP',
        'Fruits',
        'Smoker',
        'Sex',
        'Veggies',
        'HighChol',
        'PhysActivity',
    ]
    X = df[selected_features]
    y = df['Diabetes_012']

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    gnb_experiment(X_train, X_test, y_train, y_test)

    """ 3. Final feature selection vased on some intuition for best performance using GNB"""
    # Select only the most relevant features as determined by the Random Forest
    selected_features = [
        'BMI',
        'Age',
        # 'Income',
        'PhysHlth',
        # 'Education',
        # 'GenHlth',
        # 'MentHlth',
        'HighBP',
        'Fruits',
        'Smoker',
        'Sex',
        'Veggies',
        'HighChol',
        'PhysActivity',
    ]
    X = df[selected_features]
    y = df['Diabetes_012']

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    gnb_experiment(X_train, X_test, y_train, y_test)


# Perform Experiment:
select_features_test_model()
