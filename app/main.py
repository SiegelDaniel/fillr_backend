from fastapi import FastAPI
from routers.pdf_router import pdf_router

app = FastAPI(title="PDF Management API")
app.include_router(pdf_router)

@app.get("/")
async def root():
    return {"message": "PDF Management API is running"}

import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
