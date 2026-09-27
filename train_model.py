"""Train a small reproducible green-time regressor from synthetic observations."""
from pathlib import Path
import csv
import random

import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib

ROOT = Path(__file__).parent
MODEL = ROOT / "traffic_model.joblib"
DATA = ROOT / "data" / "traffic_samples.csv"


def main() -> None:
    random.seed(7)
    rows = []
    for _ in range(1200):
        vehicles = random.randint(0, 70)
        queue = random.randint(0, 55)
        speed = random.uniform(4, 14)
        wait = random.uniform(0, 90)
        # Training target is a bounded, explainable proxy for desired green time.
        green = np.clip(8 + vehicles * 0.38 + queue * 0.20 + wait * 0.06 - speed * 0.18, 10, 60)
        rows.append([vehicles, queue, speed, wait, round(float(green), 2)])

    DATA.parent.mkdir(exist_ok=True)
    with DATA.open("w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["vehicles", "queue_length", "avg_speed", "avg_wait", "green_seconds"])
        writer.writerows(rows)

    values = np.array(rows, dtype=float)
    x_train, x_test, y_train, y_test = train_test_split(values[:, :4], values[:, 4], test_size=.2, random_state=7)
    model = RandomForestRegressor(n_estimators=120, random_state=7, min_samples_leaf=3)
    model.fit(x_train, y_train)
    print(f"MAE: {mean_absolute_error(y_test, model.predict(x_test)):.2f} seconds")
    joblib.dump(model, MODEL)
    print(f"Saved {MODEL}")


if __name__ == "__main__":
    main()
