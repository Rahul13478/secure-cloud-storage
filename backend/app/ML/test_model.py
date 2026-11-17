import joblib


model = joblib.load(r"F:\cloud-storage\backend\final_ml_model.joblib")

x_test = [[9,0,0],[1,0,1]]

predict = model.predict(x_test)
print(predict)