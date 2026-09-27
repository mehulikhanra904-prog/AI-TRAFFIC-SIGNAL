# 🚦 FlowGuard — AI Traffic Signal Optimizer

<p align="center"><strong>Adaptive traffic-signal timing powered by machine learning</strong><br/><sub>Optimize green time from traffic conditions and provide an emergency-vehicle priority override.</sub></p>

<p align="center"><a href="https://ai-traffic-signal-jet.vercel.app">🌐 Live Demo</a> • <a href="https://github.com/mehulikhanra904-prog/AI-TRAFFIC-SIGNAL">📦 Repository</a></p>

<p align="center"><img src="https://img.shields.io/badge/AI-Random%20Forest-7c3aed?style=for-the-badge" alt="AI"/> <img src="https://img.shields.io/badge/API-FastAPI-009688?style=for-the-badge" alt="FastAPI"/> <img src="https://img.shields.io/badge/Frontend-HTML%20%2F%20CSS%20%2F%20JS-f59e0b?style=for-the-badge" alt="Frontend"/> <img src="https://img.shields.io/badge/Deployment-Vercel%20%2B%20Render-black?style=for-the-badge" alt="Deployment"/></p>

---

## 🧠 What is FlowGuard?

**FlowGuard** is an AI-powered traffic signal optimization prototype that demonstrates how traffic conditions can be converted into adaptive signal timings instead of relying only on fixed-duration traffic lights.

The system accepts lane-level traffic information such as:
- 🚗 Number of vehicles
- 🚧 Queue length
- 🏎️ Average vehicle speed
- ⏱️ Average waiting time

A trained **Random Forest regression model** uses these features to estimate an appropriate green-light duration for each lane.

The project also includes an **emergency vehicle priority override**, allowing a simulated ambulance to request a green corridor for a selected lane.

> ⚠️ **Important:** This is a demonstration/prototype. The current version uses simulated traffic inputs and synthetic training data. It is **not connected to live CCTV cameras, real traffic signals, or an actual emergency-dispatch system**.

## ✨ Key Features

| Feature | Description |
|---|---|
| 🤖 **ML-based signal timing** | Predicts green duration from traffic conditions |
| 🚦 **Adaptive signal control** | Uses different predicted timings for lanes A–D |
| 📊 **Traffic visualization** | Displays vehicle counts and lane status in a live dashboard |
| 🚑 **Emergency priority** | Simulates ambulance priority for a selected lane |
| 🔄 **Automatic refresh** | Requests fresh model predictions every 5 seconds |
| ⚡ **FastAPI backend** | Lightweight REST API for the decision layer |
| 🧪 **Synthetic training pipeline** | Reproducible demo dataset generation and model training |
| 🌐 **Web deployment** | Frontend deployed on Vercel with API routing toward Render |
| 🛡️ **Bounded predictions** | Green times are constrained to a practical 10–60 second range |
| 📱 **Responsive dashboard** | Browser-based traffic-control interface |

## 🏗️ System Architecture

```text
Traffic Inputs
  │
  ├── Vehicles
  ├── Queue Length
  ├── Average Speed
  └── Average Waiting Time
  │
  ▼
FastAPI Decision Layer
  │
  ▼
Random Forest Regression Model
  │
  ▼
Predicted Green Time
  │
  ├── Lane A
  ├── Lane B
  ├── Lane C
  └── Lane D
  │
  ▼
FlowGuard Dashboard
```

### 🚑 Emergency Override

```text
Ambulance Event → /api/emergency/activate → Priority Lane → Emergency Mode → /api/emergency/clear → AI Mode
```

## 🔄 How It Works

### 1️⃣ Traffic conditions

Each lane contains four input features: **vehicles**, **queue_length**, **avg_speed**, and **avg_wait**.

Example:

```text
Lane A → 47 vehicles | Queue: 29 | Speed: 8 | Wait: 20s
Lane B →  8 vehicles | Queue:  6 | Speed: 8 | Wait: 20s
Lane C → 31 vehicles | Queue: 20 | Speed: 8 | Wait: 20s
Lane D →  4 vehicles | Queue:  3 | Speed: 8 | Wait: 20s
```

### 2️⃣ ML prediction

The Random Forest regression model receives the four features for each lane and predicts a green-light duration. The API constrains the final prediction to **10–60 seconds**.

### 3️⃣ Dashboard

The frontend displays controller mode, vehicle counts, predicted green duration, active signal phase, countdown, emergency status, and API connection status.

### 4️⃣ Automatic refresh

The browser requests new optimization results every **5 seconds**.

### 5️⃣ Emergency priority

```text
NORMAL AI → EMERGENCY PRIORITY → Selected Lane → Emergency Cleared → NORMAL AI
```

## 🤖 Machine Learning Pipeline

The project includes **train_model.py**, which generates **1,200 synthetic traffic observations** and trains a Random Forest regression model.

| Feature | Meaning |
|---|---|
| **vehicles** | Number of vehicles in the lane |
| **queue_length** | Approximate queue size |
| **avg_speed** | Average traffic speed |
| **avg_wait** | Average waiting time |
| **green_seconds** | Target green-light duration |

Data split: **80% training / 20% testing**.

```python
RandomForestRegressor(
    n_estimators=120,
    random_state=7,
    min_samples_leaf=3
)
```

The training script reports **Mean Absolute Error (MAE)** on the test set.

### Why synthetic data?

The project can run without a private CCTV dataset. For production-oriented development, synthetic observations should be replaced with validated traffic observations from CCTV/video analytics, YOLO vehicle detection, traffic sensors, SUMO/TraCI, roadside IoT sensors, or historical datasets.

## 🧩 Technology Stack

### Frontend
- HTML5
- CSS3
- Vanilla JavaScript
- Fetch API
- Responsive dashboard UI

### Backend
- Python
- FastAPI
- Pydantic
- Uvicorn
- REST API
- CORS middleware

### Machine Learning
- scikit-learn
- Random Forest Regression
- NumPy
- Joblib
- Synthetic data generation

### Deployment
- Vercel — frontend
- Render — backend API

## 📁 Project Structure

```text
AI-TRAFFIC-SIGNAL/
│
├── 📄 index.html
├── 🎨 styles.css
├── ⚙️ app.js
├── 🐍 api.py
├── 🧠 train_model.py
├── 🤖 traffic_model.joblib
├── 📂 data/
│   └── traffic_samples.csv
├── 📄 requirements.txt
├── 📄 vercel.json
├── 📄 build-frontend.cjs
├── 📄 start.ps1
├── 📄 .gitignore
└── 📖 README.md
```

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- pip
- Git
- Modern web browser

### 1. Clone

```powershell
git clone https://github.com/mehulikhanra904-prog/AI-TRAFFIC-SIGNAL.git
cd AI-TRAFFIC-SIGNAL
```

### 2. Create virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Train the model

```powershell
python train_model.py
```

This generates **data/traffic_samples.csv** and **traffic_model.joblib**. The repository already contains a trained model, so retraining is optional.

### 5. Start the FastAPI backend

```powershell
uvicorn api:app --reload --port 8000
```

Open **http://127.0.0.1:8000**.

### 6. Alternative Windows startup

```powershell
.\start.ps1
```

## 🌐 Live Demo

👉 **https://ai-traffic-signal-jet.vercel.app**

The Vercel configuration routes API requests toward the configured Render backend.

> The live version is a demonstration environment and does not control real-world traffic infrastructure.

## 🔌 API Documentation

### GET /api/state

Returns the current controller state.

```json
{
  "mode": "optimized",
  "emergency": {
    "active": false,
    "lane": null,
    "distance": null,
    "vehicle": null,
    "started_at": null
  }
}
```

### POST /api/optimize

Calculates green-light durations for all four lanes.

```json
{
  "lanes": [
    {"id":"A","vehicles":47,"queue_length":29,"avg_speed":8,"avg_wait":20},
    {"id":"B","vehicles":8,"queue_length":6,"avg_speed":8,"avg_wait":20},
    {"id":"C","vehicles":31,"queue_length":20,"avg_speed":8,"avg_wait":20},
    {"id":"D","vehicles":4,"queue_length":3,"avg_speed":8,"avg_wait":20}
  ]
}
```

Example response:

```json
{
  "mode": "optimized",
  "green_seconds": [32, 18, 27, 15],
  "model": "Random Forest · synthetic training data",
  "emergency": {"active": false}
}
```

*Example values are illustrative; actual predictions depend on the loaded model.*

### POST /api/emergency/activate

Activates emergency priority.

```json
{"lane":"A","distance":120,"vehicle":"Ambulance"}
```

### POST /api/emergency/clear

Clears emergency mode and restores normal optimization.

```powershell
curl -X POST http://127.0.0.1:8000/api/emergency/clear
```

## 🚑 Emergency Simulation

1. Select a lane.
2. Click **Simulate ambulance**.
3. The API activates emergency priority mode.
4. The dashboard switches to **EMERGENCY** mode.
5. The selected lane receives priority in the simulation.
6. Click **Clear emergency** after the simulated vehicle passes.
7. Normal AI optimization resumes.

## 🔐 Safety & Scope

This project is a **simulation/prototype**, not a safety-certified traffic-control system.

The current implementation:
- Does not control physical traffic lights.
- Does not ingest live CCTV footage.
- Does not perform real-time YOLO vehicle detection.
- Does not connect to emergency services.
- Uses synthetic training data for the demonstration model.
- Should not be used for real-world traffic-control decisions.

Real deployment would require extensive validation, safety engineering, hardware integration, cybersecurity controls, fail-safe mechanisms, regulatory approval, and domain-expert oversight.

## 🔮 Future Roadmap

### 🚗 Phase 1 — Traffic perception
- [ ] Integrate YOLO-based vehicle detection
- [ ] Count vehicles from CCTV frames
- [ ] Estimate queue length
- [ ] Track average traffic speed
- [ ] Detect lane occupancy

### 🧠 Phase 2 — Advanced prediction
- [ ] Replace synthetic data with real traffic datasets
- [ ] Add time-of-day features
- [ ] Add weather/event features
- [ ] Compare Random Forest with gradient-boosting models
- [ ] Evaluate on held-out real-world data

### 🚦 Phase 3 — Traffic simulation
- [ ] Integrate SUMO
- [ ] Add TraCI communication
- [ ] Simulate multiple intersections
- [ ] Measure average waiting time
- [ ] Measure queue length
- [ ] Compare fixed-time vs adaptive strategies

### 🚑 Phase 4 — Emergency response
- [ ] Detect emergency vehicles from video
- [ ] Support authenticated priority requests
- [ ] Add route-aware emergency corridors
- [ ] Introduce conflict-safe signal transitions
- [ ] Add audit logs

### 🌐 Phase 5 — Smart-city platform
- [ ] Multi-intersection coordination
- [ ] Real-time monitoring
- [ ] Historical analytics
- [ ] Traffic forecasting
- [ ] Operator authentication
- [ ] Database-backed traffic events
- [ ] Cloud monitoring and observability

## 📈 Evaluation Metrics

| Metric | Purpose |
|---|---|
| ⏱️ Average waiting time | Measure vehicle delay |
| 🚗 Queue length | Measure congestion |
| 🟢 Green utilization | Evaluate signal efficiency |
| 🔄 Throughput | Measure vehicles served |
| 🚦 Number of stops | Estimate unnecessary stopping |
| 🚑 Emergency clearance time | Evaluate emergency simulation |
| 📊 Prediction MAE | Evaluate green-time prediction error |

## 🛠️ Development Workflow

```text
Traffic Data → Feature Engineering → Dataset → Model Training → Evaluation
→ traffic_model.joblib → FastAPI → REST API → FlowGuard Dashboard
```

## 💡 Why This Project Matters

Traditional fixed-time signals can struggle when traffic demand changes throughout the day. An adaptive approach can use observed traffic conditions to adjust signal timing dynamically.

FlowGuard demonstrates:

> **Traffic Data → Machine Learning → Signal Decision → Visualization**

and extends the concept with:

> **Emergency Event → Priority Override → Signal State Change**

This makes the project a useful foundation for experimenting with **AI, computer vision, intelligent transportation systems, and smart-city infrastructure**.

## 🤝 Contributing

Contributions and ideas are welcome.

```powershell
git clone https://github.com/mehulikhanra904-prog/AI-TRAFFIC-SIGNAL.git
cd AI-TRAFFIC-SIGNAL
git checkout -b feature/your-feature
git add .
git commit -m "feat: improve traffic optimization"
git push origin feature/your-feature
```

Then open a Pull Request and explain what changed, why it changed, how it was tested, and any limitations.

## 📜 License

This project is currently presented as a prototype. Add a repository license before distributing or reusing the project under specific open-source terms.

## 👩‍💻 Author

**Mehuli Khanra**

Aspiring AI Engineer • Full-Stack Developer • Web3 Explorer

GitHub: https://github.com/mehulikhanra904-prog

## ⭐ Support the Project

If you find **FlowGuard** interesting:
- ⭐ Star the repository
- 🍴 Fork it
- 🐛 Open an issue
- 💡 Suggest an improvement
- 🔧 Submit a pull request

<p align="center"><strong>🚦 FlowGuard</strong><br/><sub>Making traffic signals more adaptive, data-driven, and simulation-ready.</sub></p>