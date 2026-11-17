import pandas as pd
from sklearn.ensemble import IsolationForest #<-- an ml model 
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

dataframe  = pd.read_csv(r"F:\cloud-storage\backend\app\ML\practice_training_data.csv")
x = dataframe[["downloads_1min", "uploads_1min", "deletes_1min"]]
y = dataframe["label"]

X_train ,  X_test ,Y_train ,  Y_test = train_test_split(x , y  , test_size=0.2,random_state= 0 , )

x_normal = X_train[Y_train == "normal"]
print(x_normal)

model = IsolationForest(random_state=0 , contamination=0.2).fit(x_normal)
predict = model.predict(X_test)
predict_words  = []
for items in predict:
    if items == -1 :
        predict_words.append("suspicious")
    else:
        predict_words.append("normal")    

accuracy = accuracy_score(Y_test, predict_words)
print(predict_words)
print(f"accuracy : {accuracy:.4f}")
