from fastapi import FastAPI
from generative_model import perform_analysis
from typing import Union
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

#ajettaan uvicorn main:app --reload

app = FastAPI()

origins = "http://127.0.0.1:8000"

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Report(BaseModel):
    report: str
    summarization_type: str


@app.get("/")
def read_root():
    return {"Working": "Backend is running"}



@app.post("/analyze/report")
async def analyze_report(items: Report):
    result = perform_analysis(items.report, items.summarization_type)
    return result