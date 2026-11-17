import joblib
import pandas as pd 
model = joblib.load(r"F:\cloud-storage\backend\final_ml_model.joblib")

def cheack_activity(download , upload , delet):
    # make a table using pandas -->
    row = [[download,upload,delet]]
    columns  = ["downloads_1min" , "uploads_1min" , "deletes_1min"]
    tabel = pd.DataFrame(row , columns=columns)
    result = model.predict(tabel)
    



    return result[0]

ans = cheack_activity(1,1,1)
print(ans)