from flask import Flask, render_template, request
import pickle
import os
import numpy as np
import pandas as pd
from fetch_aqi import get_aqi  # Import the function to get real-time AQI

app = Flask(__name__)

# Load the trained model
model_path = "best_random_forest.pkl"
with open(model_path, "rb") as file:
    model = pickle.load(file)

# Available cities for Live AQI fetching
cities = [
    "Delhi", "Mumbai", "Bangalore", "Chennai", "Kolkata", "Hyderabad",
    "Ahmedabad", "Jaipur", "Gandhinagar", "Indore", "Patna", "Nagpur", "Udaipur", "Lucknow"
]

# Home Page
@app.route("/")
def home():
    return render_template("home.html")

# Predict AQI Page
@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        # Get input values from form
        try:
            T = float(request.form["T"])
            TM = float(request.form["TM"])
            Tm = float(request.form["Tm"])
            SLP = float(request.form["SLP"])
            H = float(request.form["H"])
            VV = float(request.form["VV"])
            V = float(request.form["V"])
            VM = float(request.form["VM"])


            # Compute engineered features
            temp_diff = (TM + Tm) / 2 - T
            h_slp_ratio = H / SLP
            wind_interaction = VV * V

            # Make prediction
            #input_features = np.array([[T, TM, Tm, SLP, H, VV, V, VM]])
            input_features = [[T, TM, Tm, SLP, H, VV, V, temp_diff, h_slp_ratio, wind_interaction]]
            predicted_aqi = model.predict(input_features)[0]

            return render_template("predict.html", result=predicted_aqi)

        except ValueError:
            return render_template("predict.html", error="Invalid input. Please enter numeric values.")

    return render_template("predict.html", result=None)

# Model Performance Page
@app.route("/performance")
def performance():
    return render_template("performance.html")

# EDA Insights Page
@app.route("/eda")
def eda():
    return render_template("eda.html")

# Live AQI Data Page
@app.route("/live-aqi", methods=["GET", "POST"])
def live_aqi():
    aqi_result = None

    if request.method == "POST":
        selected_city = request.form["city"]
        aqi_result = get_aqi(selected_city)  # Fetch AQI for selected city

    return render_template("live_aqi.html", cities=cities, result=aqi_result)

if __name__ == "__main__":
    app.run(debug=True)
