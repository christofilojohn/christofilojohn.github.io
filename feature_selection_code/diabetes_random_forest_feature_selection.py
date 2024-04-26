import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix, roc_auc_score
from sklearn.ensemble import RandomForestClassifier

# average = weighted datasets with imbalanced classes or when dealing with multi-class classification problems.

# Load and prepare data
df = pd.read_csv('diabetes_012_health_indicators_BRFSS2015.csv')
X = df.drop('Diabetes_012', axis=1)
y = df['Diabetes_012']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Initialize and train a Random Forest Classifier to measure feature importance
forest = RandomForestClassifier(n_estimators=150, random_state=42)
forest.fit(X_train, y_train)

importance_vector = forest.feature_importances_

# Print importance by feature
feature_names = X.columns
feature_imports = pd.Series(importance_vector, index=feature_names).sort_values(ascending=False)
print("Using Random Forest Classifier,"
      "\nwe can sort the features of the dataset by importance:" )
print(feature_imports)
