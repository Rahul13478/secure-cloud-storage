import pandas as pd 
import joblib #save the model in a file 
from sklearn.tree import DecisionTreeClassifier

dataframe = pd.read_csv(r"F:\cloud-storage\backend\app\ML\practice_training_data.csv")

x = dataframe[["downloads_1min", "uploads_1min", "deletes_1min"]]
y = dataframe["label"]

model = DecisionTreeClassifier(random_state= 0 , max_depth=3).fit(x,y)

joblib.dump(model , "final_ml_model.joblib")

