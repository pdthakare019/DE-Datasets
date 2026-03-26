from fastapi import FastAPI
import pandas as pd

app = FastAPI()
df = pd.read_csv("C:\Users\PrathameshThakare\Desktop\DE\datasets\real-estate\dim_location.csv")

@app.get("/data")
def get_data():
    return df.to_dict(orient="records")