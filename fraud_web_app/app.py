from flask import Flask, render_template, request
import joblib
import numpy as np
import os

app = Flask(__name__)
model = joblib.load("fraud_model.pkl")

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    prob = None
    time_val = None
    amount_val = None

    if request.method == "POST":
        time_val = float(request.form["time"])
        amount_val = float(request.form["amount"])

        # Dummy PCA input
        input_data = np.zeros((1, 30))
        input_data[0, 0] = time_val
        input_data[0, -1] = amount_val

        pred = model.predict(input_data)[0]

        # ---- SMART PROBABILITY LOGIC ----
        risk_score = 0

        if amount_val > 5000:
            risk_score += 40
        elif amount_val > 1000:
            risk_score += 20
        else:
            risk_score += 5

        if time_val > 50000:
            risk_score += 30
        else:
            risk_score += 10

        if pred == 1:
            risk_score += 30

        prob = min(risk_score, 99)  # max 99%

        if prob >= 50:
            result = "Fraud Transaction"
        else:
            result = "Genuine Transaction"

    return render_template(
        "index.html",
        result=result,
        prob=prob,
        time=time_val,
        amount=amount_val
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
