import pandas as pd
from sklearn.model_selection import StratifiedKFold
import os

# Constants
DATA_PATH = "./data/"
ORIGINAL_DATA_FILE = "diabetes_012_health_indicators_BRFSS2015.csv"


def load_and_select_features(data_path):
    """Load the dataset and select specific features."""
    df = pd.read_csv(data_path)
    selected_features = [
        'BMI',
        'Age',
        'PhysHlth',
        'HighBP',
        'Fruits',
        'Smoker',
        'Sex',
        'Veggies',
        'HighChol',
        'PhysActivity',
    ]
    # df.dropna(inplace=True)
    X = df[selected_features]
    y = df['Diabetes_012']

    return X, y


def save_k_fold_splits(data_path, n_splits=5, random_state=None):
    """
    Perform stratified k-fold split on the dataset and save each fold to a separate CSV file.
    """
    X, y = load_and_select_features(data_path)
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=random_state)
    fold_number = 0

    for _, test_index in skf.split(X, y):
        fold_X = pd.DataFrame(X.iloc[test_index].values, columns=[f'feature_{j}' for j in range(X.shape[1])])
        fold_Y = pd.Series(y.iloc[test_index].values, name='target')

        # Merge X and Y
        fold_data = pd.concat([fold_X, fold_Y], axis=1)
        fold_data.to_csv(f'{DATA_PATH}data_portion_{fold_number}.csv', index=False)
        fold_number += 1

# Main execution
save_k_fold_splits(ORIGINAL_DATA_FILE, n_splits=16)
