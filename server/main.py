from dataclasses import dataclass
from fastapi import status
from flask import Flask


app = Flask(__name__)


@dataclass
class ExamResults:
    grade: str
    total: int

@app.get("/")
def generalResults():
    results: ExamResults = {
       "grade": "A",
       "total": 40_000
    }

    response_data = {
        "results": results,
        "status_code": status.HTTP_200_OK,
    }
    return response_data

@app.get("/schools")
def schoolResults():
    results: ExamResults = {
       "grade": "A",
       "total": 50_000
    }

    response_data = {
        "results": results,
        "status_code": status.HTTP_200_OK,
    }
    return response_data



if __name__ == "__main__":
    app.run(host="127.0.0.1" ,port=5000, debug=True)
