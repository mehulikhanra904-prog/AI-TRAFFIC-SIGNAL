# Adaptive Traffic Signal Optimizer

## Live Demo

[Open the website on Vercel](https://ai-traffic-signal-jet.vercel.app)

Hackathon-ready prototype combining adaptive signal timing with an emergency
priority override. The browser dashboard is a no-build static frontend, and
the FastAPI service exposes the same decision layer for SUMO/TraCI or YOLO
adapters.

## Run the dashboard

```powershell
cd traffic_optimizer_web
python -m http.server 5173
```

Open http://localhost:5173.

## Run the API

```powershell
pip install -r requirements.txt
uvicorn api:app --reload --port 8000
```

The API's `POST /api/optimize` uses the trained model when scikit-learn is
available and falls back to a transparent pressure heuristic otherwise.
Train the small demo model with:

```powershell
python train_model.py
```

The model is intentionally trained on generated lane features so the project
runs without a private CCTV dataset. Replace `data/traffic_samples.csv` with
real YOLO/SUMO observations for a production model.
