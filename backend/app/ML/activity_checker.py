import joblib
from pathlib import Path
import pandas as pd 
MODEL_PATH=Path(__file__).resolve().parents[2] / "final_ml_model.joblib"
model = joblib.load(MODEL_PATH)

def cheack_activity(download , upload , delet):
    # make a table using pandas -->
    row = [[download,upload,delet]]
    columns  = ["downloads_1min" , "uploads_1min" , "deletes_1min"]
    tabel = pd.DataFrame(row , columns=columns)
    result = model.predict(tabel)
    



    return result[0]

