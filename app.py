from flask import Flask, render_template, request
from joblib import load
import os
import numpy as np

model_path = 'svm_model_best.joblib'
scaler_path = 'scaler.joblib'

if not os.path.exists(model_path):
    print(f"Error: Model file '{model_path}' not found.")
    exit()

if not os.path.exists(scaler_path):
    print(f"Error: Scaler file '{scaler_path}' not found.")
    exit()

try:
    model = load(model_path)
    print("Model loaded successfully!")
    scaler = load(scaler_path)
    print("Scaler loaded successfully!")
except Exception as e:
    print(f"Error loading the model or scaler: {e}")
    exit()

def load_mappings(file_path):
    mappings = {}
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        exit()
    with open(file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split(':')
            mappings[key.strip()] = int(value.strip())
    return mappings

country_mapping = load_mappings('country_mapping.txt')

# Flask app
app = Flask(__name__)

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        form_data = {
            "A1_Score": request.form.get("A1_Score"),
            "A2_Score": request.form.get("A2_Score"),
            "A3_Score": request.form.get("A3_Score"),
            "A4_Score": request.form.get("A4_Score"),
            "A5_Score": request.form.get("A5_Score"),
            "A6_Score": request.form.get("A6_Score"),
            "A7_Score": request.form.get("A7_Score"),
            "A8_Score": request.form.get("A8_Score"),
            "A9_Score": request.form.get("A9_Score"),
            "A10_Score": request.form.get("A10_Score"),
            "age": request.form.get("age"),
            "gender": request.form.get("gender"),
            "jaundice": request.form.get("jaundice"),
            "autism": request.form.get("autism"),
            "country_of_residence": request.form.get("country_of_residence"),
            "used_app_before": request.form.get("used_app_before"),
            "result": request.form.get("result")
        }

        print("Form Data Received:", form_data)

        gender_encoding = {'f': 0, 'm': 1}
        jaundice_encoding = {'no': 0, 'yes': 1}
        autism_encoding = {'no': 0, 'yes': 1}
        used_app_before_encoding = {'no': 0, 'yes': 1}

        encoded_gender = gender_encoding.get(form_data["gender"], 0)
        encoded_jaundice = jaundice_encoding.get(form_data["jaundice"], 0)
        encoded_autism = autism_encoding.get(form_data["autism"], 0)
        encoded_used_app_before = used_app_before_encoding.get(form_data["used_app_before"], 0)

        try:
            features = np.array([[
                int(form_data["A1_Score"] or 0),
                int(form_data["A2_Score"] or 0),
                int(form_data["A3_Score"] or 0),
                int(form_data["A4_Score"] or 0),
                int(form_data["A5_Score"] or 0),
                int(form_data["A6_Score"] or 0),
                int(form_data["A7_Score"] or 0),
                int(form_data["A8_Score"] or 0),
                int(form_data["A9_Score"] or 0),
                int(form_data["A10_Score"] or 0),
                int(form_data["age"] or 0),
                encoded_gender,
                encoded_jaundice,
                encoded_autism,
                encoded_used_app_before,
                int(form_data["result"] or 0)
            ]])

            print("Raw Features for Prediction:", features)

            scaled_features = scaler.transform(features)
            print("Scaled Features for Prediction:", scaled_features)

            prediction = model.predict(scaled_features)
            print("Prediction:", prediction)

            return render_template(
                './front-end/startbootstrap-scrolling-nav-gh-pages/index.html',
                   prediction=prediction[0]                             )
        except Exception as e:
            print(f"Error during prediction: {e}")
            return render_template(
                './front-end/startbootstrap-scrolling-nav-gh-pages/index.html',
                error="An error occurred while processing your request. Please try again."
            )

    return render_template('./front-end/startbootstrap-scrolling-nav-gh-pages/index.html')

if __name__ == "__main__":
    app.run(debug=True)
