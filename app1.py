from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
import os

app = FastAPI()

CSV_FILE = "dim_location.csv"

from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
import os

app = FastAPI()

CSV_FILE = "property_interactions.csv"


@app.get("/")
def get_csv_root():
    if not os.path.exists(CSV_FILE):
        raise HTTPException(status_code=404, detail="CSV file not found")

    try:
        with open(CSV_FILE, "r", encoding="utf-8-sig") as file:
            csv_content = file.read()

        return Response(
            content=csv_content,
            media_type="text/plain"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
