from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field,field_validator
from typing import Literal

app = FastAPI()

incidents = []


class IncidentCreate(BaseModel):
    service: str = Field(min_length=3, max_length=100)
    error_code: int = Field(ge=400, le=599)
    message: str = Field(min_length=10, max_length=1000)
    severity: Literal["low", "medium", "high", "critical"]

    @field_validator("service", mode="before")
    @classmethod
    def clean_service(cls, value):
        return value.strip()


class IncidentUpdate(BaseModel):
    severity: Literal["low", "medium", "high", "critical"] | None = None


@app.get("/")
def home():
    return {
        "message": "Incident Management API is running"
    }


@app.post("/incidents")
def create_incident(incident: IncidentCreate):
    incident_data = incident.model_dump()
    incident_id = len(incidents) + 1

    incident_data["id"] = incident_id

    incidents.append(incident_data)
    return incident_data


@app.get("/incidents")
def get_incidents():
    return incidents


@app.get("/incidents/{incident_id}")
def get_incident(incident_id: int):
    for incident in incidents:
        if incident["id"] == incident_id:
            return incident

    raise HTTPException(
        status_code=404,
        detail="Incident not found"
    )


@app.patch("/incidents/{incident_id}")
def update_incident(update: IncidentUpdate, incident_id: int):
    for incident in incidents:
        if incident["id"] == incident_id:
            if update.severity is not None:
                incident["severity"] = update.severity
            
            return incident
        
    raise HTTPException(
        status_code=404,
        detail="Incident not found"
    )


@app.delete("/incidents/{incident_id}")
def delete_incident(incident_id: int):
    for incident in incidents:
        if incident["id"] == incident_id:
            incidents.remove(incident)

            return {
                "message": "Incident deleted successfully"
            }

    raise HTTPException(
        status_code=404,
        detail="Incident not found"
    ) 

