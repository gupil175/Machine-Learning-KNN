### You will work with a dataset containing information about Asteroids, and develop a kNN model to classify whether an Asteroid is a Near Earth Object (NEO).


### Preparation: load dataset
Download the dataset 'neo_v2.csv.zip' and store it in the same folder as this Jupyter notebook. Use the following codes to load the dataset.
"""

import numpy as np
import pandas as pd

df = pd.read_csv('neo_v2.csv.zip')

"""### Q1. Understand the dataset (1 point)
1. Use the proper command to show the first 8 rows of the dataset (0.5 point)
2. Use the proper command(s) to examine whether there is missing data in the dataset. If there is missing data, choose the suitable approach to handle missing data. (0.5 point)
"""

# Write your code for Q1.1 here
df.head(8)
# Write your code for Q1.2 here
data=df.isnull().sum()
print(data)

if df.isnull().values.any():
   print("There are missing values in the dataset.")
else:
    print("No missing values found in the dataset.")

"""### Q2. Create separate arrays to store features and target label (1 point)
In this dataset, the target label is indicated in the column 'hazardous'.
Among the other columns, we will use the following as features (predictor variables): 'est_diameter_min', 'est_diameter_max', 'relative_velocity', 'miss_distance', 'sentry_object', 'absolute_magnitude'.
"""

# Complete the following commands
# We first create separate dataframes for features and target label
df_x = df[['est_diameter_min', 'est_diameter_max', 'relative_velocity', 'miss_distance', 'sentry_object', 'absolute_magnitude']]
df_y = df[['hazardous']]

# We need to transform boolean values into integer values in 'sentry_object' and 'hazardous' columns:
# replace True with 1 and replace False with 0
df_x["sentry_object"] = df_x["sentry_object"].astype(int) 
df_y["hazardous"] = df_y["hazardous"].astype(int)

# We then store the dataframe for features as a numpy array X, and the dataframe for label as a numpy array y.
X = df_x.values
y = df_y.values
"""### Q3. Split dataset into train-test with a 80/20 split (1 point)
Use the proper commands to split (X,y) into training set (80% of all data), and testing set (20% of all data).
"""

# Write your code for Q3 here: use random_state=4
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=4)

"""### Q4. Fit a kNN model with default setting (2 points)
Use the proper commands to fit a kNN model on the training set with the default setting in `scikit-learn`.
"""

# Write your code for Q4 here
from sklearn.neighbors import KNeighborsClassifier

knn = KNeighborsClassifier()
knn.fit(X_train, y_train)

"""### Q5. Apply and test the trained kNN model (1 point)
1. Predict the label for a unlabeled asteroid with the following features:
est_diameter_min = 0.127, est_diameter_max = 0.285, relative_velocity = 48066, miss_distance = 37066550,  sentry_object = True, absolute_magnitude = 23.5
2. Use the proper command to find the classification accuracy on testing set.
"""

# Write your code for Q5.1 here
unlabeled = [0.127, 0.285, 48066, 37066550, 1, 23.5] 
knn.predict([unlabeled])
# Write your code for Q5.2 here
knn.score(X_test, y_test)
"""### Q6. Use cross validation to select k from the range [2,20] (2 points)
Use the proper command to select k from the indicated range with 5-fold cross validation. Note that you will use the unsplit dataset (X,y) for cross validation. Your goal is to find the k in this range that gives the best accuracy score.
"""

# Write your code for Q6 here. Hint: you should use the imported GridSearchCV function
from sklearn.model_selection import GridSearchCV

params = {'n_neighbors': range(2, 21)}
grid_knn = GridSearchCV(KNeighborsClassifier(), params, cv=5, scoring='accuracy')
grid_knn.fit(X, y)
print(grid_knn.best_params_)
print(grid_knn.best_score_)

"""### Q7. Apply scaling to variables (2 points)
The predictor variables vary greatly in scales. We now wish to scale two columns that are significantly larger than the rest: 'relative_velocity', 'miss_distance'. Your goals are two-fold:
1. Select a scaling approach to scale the columns so that they both have the range [0,1]. (0.5 point)
2. Repeat Q3 and Q4 on the scaled dataset, namely, use a 80/20 train-test split to train a kNN with default setting. Then report the kNN's testing accuracy. (0.5 point)
"""

# Write your code for Q7.1 here
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()
scaler.fit(df[['relative_velocity','miss_distance']])
df[['relative_velocity','miss_distance']] = scaler.transform(df[['relative_velocity','miss_distance']])

# Write your code for Q7.2 here
knn = KNeighborsClassifier()
knn.fit(X_train, y_train)

print(knn.score(X_test, y_test))
