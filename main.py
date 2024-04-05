from fastapi import FastAPI, BackgroundTasks
from celery import Celery
import requests

app = FastAPI()

# Initialize Celery
celery = Celery(__name__, broker='redis://localhost:6379/')

# Define Celery task
@celery.task
def scrape_apollo(name: str, organization_name: str):
    # Implement scraping functionality here
    # Make requests to Apollo.io and scrape search results
    # Return scraped results or save them to a database
    url = "https://api.apollo.io/api/v1/mixed_companies/search"

    url = "https://api.apollo.io/v1/mixed_people/search"
    
    data = {
        "api_key": "",
        "q_organization_domains": "apollo.io\ngoogle.com",
        "page" : 1,
        "per_page": 10,
        "organization_locations": ["California, US"],
        "person_seniorities": ["senior", "manager"],
        "organization_num_employees_ranges": ["1,1000000"],
        "person_titles" : ["sales manager", "engineer manager"]
    }
    
    headers = {
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, json=data)
    
    print(response.text)
    return response
    

@app.post("/scrape")
async def start_scraping(name: str, organization_name: str, background_tasks: BackgroundTasks):
    # Start the scraping task asynchronously
    task = scrape_apollo.delay(name, organization_name)
    # Return the job id
    return {"job_id": task.id}

@app.get("/scrape_results")
async def get_scrape_results(job_id: str):
    # Check the status of the Celery task
    print("sq")
    task = scrape_apollo.AsyncResult(job_id)
    if task.ready():
        # If the task is finished, return the results
        return {"status": "finished", "results": task.result}
    else:
        # If the task is still running, return the status
        return {"status": "running"}
