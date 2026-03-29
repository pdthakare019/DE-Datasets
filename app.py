from fastapi import FastAPI, HTTPException, Header, Query
from fastapi.responses import Response
import os

app = FastAPI()

CSV_FILE = "financing_options.csv"
API_KEY = os.getenv("API_KEY")


@app.get("/")
def get_csv_root(
    x_api_key: str | None = Header(default=None),
    api_key: str | None = Query(default=None)
):
    # Allow API key either from header (good for ADF/Postman)
    # or query parameter (easy for browser testing)
    provided_key = x_api_key or api_key

    if not API_KEY:
        raise HTTPException(
            status_code=500,
            detail="Server API key is not configured"
        )

    if provided_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )

    if not os.path.exists(CSV_FILE):
        raise HTTPException(
            status_code=404,
            detail=f"CSV file not found: {CSV_FILE}"
        )

    try:
        with open(CSV_FILE, "r", encoding="utf-8-sig") as file:
            csv_content = file.read()

        return Response(
            content=csv_content,
            media_type="text/plain"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )






# from fastapi import FastAPI, HTTPException
# from fastapi.responses import Response
# import os

# app = FastAPI()

# CSV_FILE = "financing_options.csv"


# @app.get("/")
# def get_csv_root():
#     if not os.path.exists(CSV_FILE):
#         raise HTTPException(status_code=404, detail="CSV file not found")

#     try:
#         with open(CSV_FILE, "r", encoding="utf-8-sig") as file:
#             csv_content = file.read()

#         return Response(
#             content=csv_content,
#             media_type="text/plain"
#         )
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))



# @app.get("/dim_location", response_class=PlainTextResponse)
# def get_dim_location_csv():
#     if not os.path.exists(CSV_FILE):
#         raise HTTPException(status_code=404, detail="CSV file not found")

#     try:
#         with open(CSV_FILE, "r", encoding="utf-8-sig") as file:
#             return file.read()
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# from fastapi import FastAPI, HTTPException
# from fastapi.responses import PlainTextResponse
# import pandas as pd
# import os

# app = FastAPI()

# CSV_FILE = "dim_location.csv"


# @app.get("/")
# def home():
#     return {"message": "CSV API is running"}


# @app.get("/dim_location")
# def get_csv_as_json():
#     if not os.path.exists(CSV_FILE):
#         raise HTTPException(status_code=404, detail="CSV file not found")

#     try:
#         df = pd.read_csv(CSV_FILE, encoding="utf-8-sig")

#         # 🔥 This is the key fix
#         df = df.fillna("")

#         return df.to_dict(orient="records")

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @app.get("/raw-csv", response_class=PlainTextResponse)
# def get_raw_csv():
#     if not os.path.exists(CSV_FILE):
#         raise HTTPException(status_code=404, detail="CSV file not found")

#     try:
#         with open(CSV_FILE, "r", encoding="utf-8-sig") as file:
#             return file.read()
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
