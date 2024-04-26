
from sklearn.datasets import make_blobs
from sklearn.model_selection import StratifiedKFold
import argparse
import pandas as pd 
import os


DATA_PATH = "./data/"

"""Create the dataset and split this data into n portions, where n is the number of clients
(n-splits) = n
"""
def create_data(samples, centroids, variance, features, n_splits):
    """Create the blobs dataset"""
    X, y = make_blobs(n_samples=samples, centers=centroids, cluster_std=variance, n_features=features)

    """Make splits based on n_splits with class stratification"""
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True)

    for i, (_, test_index) in enumerate(skf.split(X, y)):
        # Create DataFrames for features and target
        fold_X = pd.DataFrame(X[test_index], columns=[f'feature_{j}' for j in range(features)])
        fold_Y = pd.Series(y[test_index], name='target')

        # Merge X and Y
        fold_data = pd.concat([fold_X, fold_Y], axis=1)

        # Save to CSV
        # Check if the folder exists
        if not os.path.exists(DATA_PATH):
            # If it doesn't exist, create it
            os.makedirs(DATA_PATH)
        fold_data.to_csv(f"{DATA_PATH}data_portion_{i}.csv", header=True, index=False)



"""Argparser"""
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create dataset and split into portions.")
    parser.add_argument('--s', type=int, help='Number of samples in the dataset')
    parser.add_argument('--v', type=int, help='Variance of clusters')
    parser.add_argument('--c', type=int, help='Number of centroids for make_blobs')
    parser.add_argument('--f', type=int, help='Number of features for make_blobs')
    parser.add_argument('--n', type=int, help='Number of splits for StratifiedKFold')
    
    args = parser.parse_args()
    
    if None in [args.s,  args.c,  args.v, args.f, args.n,]:
        create_data(500, 2, 15.0, 10, 3)
    else:
        create_data(args.s, args.v, args.c, args.f, args.n)