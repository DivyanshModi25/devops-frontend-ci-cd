from fastapi import FastAPI, HTTPException,Query
from pydantic import BaseModel, Field
import requests, os
from dotenv import load_dotenv
from fastapi_mcp import FastApiMCP
import uvicorn


load_dotenv()

JENKINS_URL = os.getenv("JENKINS_URL")
JENKINS_USER = os.getenv("JENKINS_USER")
JENKINS_TOKEN = os.getenv("JENKINS_TOKEN")

if not (JENKINS_URL and JENKINS_USER and JENKINS_TOKEN):
    raise RuntimeError("Jenkins environment variables not configured properly!")


app = FastAPI(title="Jenkins MCP Server")


class JenkinsJob(BaseModel):
    job_name: str = Field(..., description="The name of the Jenkins job to trigger or check")




# list all jenkins project
@app.get("/jobs", operation_id="list_jenkins_jobs", summary="List all Jenkins jobs")
def list_jenkins_jobs():
    """Lists all available Jenkins jobs (projects)."""
    url = f"{JENKINS_URL}/api/json"
    r = requests.get(url, auth=(JENKINS_USER, JENKINS_TOKEN))

    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=f"Failed to fetch projects: {r.text}")
    
    data = r.json()
    jobs = [
        {"name": job["name"], "url": job["url"], "status_color": job.get("color")}
        for job in data.get("jobs", [])
    ]
    return {"count": len(jobs), "projects": jobs}





# trigger jenkins build based on job
@app.post("/trigger", operation_id="trigger_jenkins_build", summary="Trigger Jenkins pipeline by job name")
def trigger_jenkins_build(job: JenkinsJob):
    """Triggers a Jenkins pipeline by job name."""
    url = f"{JENKINS_URL}/job/{job.job_name}/build"
    r = requests.post(url, auth=(JENKINS_USER, JENKINS_TOKEN))
    if r.status_code == 201:
        return {"success": True, "message": f"Build for '{job.job_name}' triggered successfully!"}
    else:
        raise HTTPException(status_code=r.status_code, detail=f"Failed to trigger build: {r.text}")



# get last build status 
@app.get("/status", operation_id="get_jenkins_status", summary="Get Jenkins last build status")
def get_jenkins_status(job_name: str):
    """Fetches latest build result for a Jenkins job."""
    url = f"{JENKINS_URL}/job/{job_name}/lastBuild/api/json"
    r = requests.get(url, auth=(JENKINS_USER, JENKINS_TOKEN))
    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=f"Error: {r.text}")
    
    data = r.json()
    # print(data) 
    return {
        "job_name": job_name,
        "build_id": data.get("id", "unknown"),
        "status": data.get("result", "IN PROGRESS"),
        "url": data.get("url", "")
    }




# get jenkins build logs
@app.get("/logs", operation_id="get_jenkins_logs", summary="Fetch Jenkins build logs")
def get_jenkins_logs(job_name: str):
    """Gets console logs from last Jenkins build."""
    url = f"{JENKINS_URL}/job/{job_name}/lastBuild/consoleText"
    r = requests.get(url, auth=(JENKINS_USER, JENKINS_TOKEN))
    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=f"Could not fetch logs: {r.text}")
    
    logs = r.text[-1500:]  # return last few lines for readability
    return {"job_name": job_name, "logs_tail": logs}



# get past n builds for a specific job
@app.get("/projects/{job_name}/builds", operation_id="get_pastn_job_builds",summary="Fetch past N builds for a Jenkins job")
def get_past_n_builds(
    job_name: str,
    n: int
):
    """Fetches past N builds for a given Jenkins job."""
    url = f"{JENKINS_URL}/job/{job_name}/api/json?tree=builds[number,result,url]{{0,{n}}}"
    r = requests.get(url, auth=(JENKINS_USER, JENKINS_TOKEN))

    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=f"Failed to fetch builds: {r.text}")

    builds = [
        {
            "build_number": b["number"],
            "status": b.get("result", "IN_PROGRESS"),
            "url": b["url"]
        }
        for b in r.json().get("builds", [])
    ]

    return {
        "job_name": job_name,
        "requested_count": n,
        "fetched_count": len(builds),
        "builds": builds
    }




if __name__ == "__main__":
    
    mcp = FastApiMCP(
        app,
        include_operations=[
            "trigger_jenkins_build",
            "get_jenkins_status",
            "get_jenkins_logs",
            "check_health",
            "list_jenkins_jobs",
            "get_pastn_job_builds"
        ]
    )
    mcp.mount_http()

    uvicorn.run(app, host="0.0.0.0", port=8765)
