# objective for now is teach python to read from csv file ..
# this file will leter train the model 
# for now it will read as a table and print the tabel 

# for that we will use pandas and its table object dataframe 

import pandas as pd 
from sklearn.tree import DecisionTreeClassifier  , export_text
from sklearn.model_selection import train_test_split #<--- a helper func that split dataset into train and test 
from sklearn.metrics import accuracy_score #<--- to cheack the accuracy 

dataframe  = pd.read_csv(r"F:\cloud-storage\backend\app\ML\practice_training_data.csv") #read the csv file as a table into pandas dataframe
# print(dataframe) 
x = dataframe[["downloads_1min", "uploads_1min", "deletes_1min"]]
y = dataframe["label"]
# print(x )
# print(y)
X_trian , X_test, Y_train , Y_test = train_test_split(x , y , test_size=0.2 , random_state=0)

# train a decision tree -->
# for learning u call fit then model looks through ur examples and predict ans for random value 
# for predictions use predict 

# decisionTreeClassifire
# x_test = [[9,0,4],[4,2,1],[0,0,0],[0,1,7],[0,1,10],[7,0,0],[0,4,9],[0,0,12],[8,8,8],[6,0,0] , [5,0,0]]

# scikit-learn train_test_split --> it splits the dataset into like 80 , 20. 80 for learning and 20 for testing 


model = DecisionTreeClassifier(random_state=0, max_depth=3).fit(X_trian , Y_train) # model learn from here
tree_rule = export_text(model , feature_names=list(model.feature_names_in_)) 
predict = model.predict(X_test) # model gives a predicted ans from what he learned 
accuracy = accuracy_score(Y_test , predict) # to cheack the accurecy 
result  = X_test.copy()
result["real"] = Y_test
result["predict"] = predict


print(f"accuracy{accuracy:.4f}")
print(predict)
print(tree_rule)
# print(result)
#look inside the tree 
# print the rule of this model -- this is how u debug a model 
# scikit-learn export_text decision tree

# need to write a script that will read line by line for txt file and find numbers 
# after 3 coloums and print text for lebel 