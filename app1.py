from fastapi import FastAPI, HTTPException, Header, Query
from fastapi.responses import Response
import os
import pandas as pd

app = FastAPI()
CSV_FILE = "property_interactions.csv"
API_KEY  = os.getenv("API_KEY")

def verify_api_key(x_api_key, api_key):
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

@app.get("/")
def get_interactions(
    x_api_key: str | None = Header(default=None),
    api_key:   str | None = Query(default=None),
    page:      int        = Query(default=1,    ge=1),
    size:      int        = Query(default=1000, ge=1, le=5000)
):
    verify_api_key(x_api_key, api_key)

    if not os.path.exists(CSV_FILE):
        raise HTTPException(
            status_code=404,
            detail=f"CSV file not found: {CSV_FILE}"
        )

    try:
        df = pd.read_csv(CSV_FILE, encoding="utf-8-sig")

        total_records = len(df)
        total_pages   = max(1, (total_records + size - 1) // size)

        if page > total_pages:
            return {
                "page":          page,
                "size":          size,
                "total_records": total_records,
                "total_pages":   total_pages,
                "has_next":      False,
                "data":          []
            }

        start   = (page - 1) * size
        end     = start + size
        page_df = df.iloc[start:end]
        page_df = page_df.where(pd.notnull(page_df), None)

        return {
            "page":          page,
            "size":          size,
            "total_records": total_records,
            "total_pages":   total_pages,
            "has_next":      page < total_pages,
            "data":          page_df.to_dict(orient="records")
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/raw")
def get_csv_raw(
    x_api_key: str | None = Header(default=None),
    api_key:   str | None = Query(default=None)
):
    verify_api_key(x_api_key, api_key)

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
        raise HTTPException(status_code=500, detail=str(e))




#Backup Code
# from fastapi import FastAPI, HTTPException, Header, Query
# from fastapi.responses import Response
# import os

# app = FastAPI()

# CSV_FILE = "property_interactions.csv"
# API_KEY = os.getenv("API_KEY")


# @app.get("/")
# def get_csv_root(
#     x_api_key: str | None = Header(default=None),
#     api_key: str | None = Query(default=None)
# ):
#     # Allow API key either from header (good for ADF/Postman)
#     # or query parameter (easy for browser testing)
#     provided_key = x_api_key or api_key

#     if not API_KEY:
#         raise HTTPException(
#             status_code=500,
#             detail="Server API key is not configured"
#         )

#     if provided_key != API_KEY:
#         raise HTTPException(
#             status_code=401,
#             detail="Unauthorized"
#         )

#     if not os.path.exists(CSV_FILE):
#         raise HTTPException(
#             status_code=404,
#             detail=f"CSV file not found: {CSV_FILE}"
#         )

#     try:
#         with open(CSV_FILE, "r", encoding="utf-8-sig") as file:
#             csv_content = file.read()

#         return Response(
#             content=csv_content,
#             media_type="text/plain"
#         )

#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail=str(e)
#         )

