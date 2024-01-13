from dataclasses import dataclass
import requests

from fastapi import status
from flask import Flask
import requests 
import asyncio

app = Flask(__name__)

@dataclass
class ExamResults:
    grade: str
    total: int

async def query_result(indexNumber, name):
    data = {"indexNumber": indexNumber, "name": name}
    try:
        response = await requests.post("https://results.knec.ac.ke/Home/CheckResult", data=data)
        print(response)
        return response
    except Exception as e:
        print(e)
        return e.message

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

@app.post("/check_results/{indexNumber}/{name}")
def check_result(indexNumber, name):
    
    results = asyncio.run(query_result(indexNumber, name))
    print(results)

    response_data = {
        "results": results,
        "status_code": status.HTTP_200_OK,
        
    }
    return response_data



if __name__ == "__main__":
    app.run(host="127.0.0.1" ,port=5000, debug=True)
