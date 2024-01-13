from dataclasses import dataclass
import requests

from fastapi import status
from flask import Flask, request
import requests 
import asyncio

app = Flask(__name__)

@dataclass
class ExamResults:
    grade: str
    total: int

def query_result(indexNumber, name):
    server_url = "https://results.knec.ac.ke/Home/CheckResult"
    data = {"indexNumber": indexNumber, "name": name}
    try:
        response = requests.post(server_url, data=data)
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

@app.post("/check_results")
def check_result():
    indexNumber, name = request.get_json() 
    results = query_result(indexNumber, name)
    print(results)

    response_data = {
        "results": "B+",
        "status_code": status.HTTP_200_OK,
        
    }
    return response_data



if __name__ == "__main__":
    app.run(host="127.0.0.1" ,port=5000, debug=True)
