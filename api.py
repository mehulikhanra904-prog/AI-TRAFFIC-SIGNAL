"""Decision-layer API: normal AI optimization plus emergency override."""
from pathlib import Path
from typing import List
import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi import HTTPException
from pydantic import BaseModel, Field

ROOT = Path(__file__).parent
MODEL_PATH = ROOT / "traffic_model.joblib"
app = FastAPI(title="Adaptive Signal Optimizer")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

emergency = {"active": False, "lane": None, "distance": None, "vehicle": None, "started_at": None}


class Lane(BaseModel):
    id: str = Field(pattern="^[A-D]$")
    vehicles: int = Field(ge=0, le=500)
    queue_length: int = Field(ge=0, le=500)
    avg_speed: float = Field(ge=0, le=100)
    avg_wait: float = Field(ge=0, le=600)


class TrafficSnapshot(BaseModel):
    lanes: List[Lane]


class EmergencyEvent(BaseModel):
    lane: str = Field(pattern="^[A-D]$")
    distance: float = Field(ge=0)
    vehicle: str = "Ambulance"


def predict(lanes: List[Lane]) -> List[int]:
    try:
        import joblib
        model = joblib.load(MODEL_PATH)
        result = model.predict([[x.vehicles, x.queue_length, x.avg_speed, x.avg_wait] for x in lanes])
        return [max(10, min(60, round(float(value)))) for value in result]
    except Exception as exc:
        raise HTTPException(503, "Model unavailable. Train traffic_model.joblib with train_model.py.") from exc


@app.get("/api/state")
def state():
    return {"mode": "emergency" if emergency["active"] else "optimized", "emergency": emergency}


@app.post("/api/optimize")
def optimize(snapshot: TrafficSnapshot):
    if sorted(x.id for x in snapshot.lanes) != list("ABCD"):
        raise HTTPException(422, "Provide exactly one lane each: A, B, C, D")
    greens = predict(snapshot.lanes)
    return {"mode": "emergency" if emergency["active"] else "optimized", "green_seconds": greens,
            "model": "Random Forest · synthetic training data", "emergency": emergency}


@app.post("/api/emergency/activate")
def activate(event: EmergencyEvent):
    emergency.update(active=True, lane=event.lane, distance=event.distance,
                     vehicle=event.vehicle, started_at=time.time())
    return {"status": "priority_active", "message": f"Green corridor reserved for Lane {event.lane}", "emergency": emergency}


@app.post("/api/emergency/clear")
def clear():
    emergency.update(active=False, lane=None, distance=None, vehicle=None, started_at=None)
    return {"status": "cleared", "message": "AI optimization restored", "emergency": emergency}


@app.get("/")
def dashboard():
    return FileResponse(ROOT / "index.html")


@app.get("/app.js")
def javascript():
    return FileResponse(ROOT / "app.js", media_type="application/javascript")


@app.get("/styles.css")
def stylesheet():
    return FileResponse(ROOT / "styles.css", media_type="text/css")
