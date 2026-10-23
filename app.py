from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Load trained artifacts
model = joblib.load("model.joblib")
scaler = joblib.load("scaler.joblib")
encoder = joblib.load("encoder.joblib")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get JSON data from frontend
        data = request.get_json()

        # Extract features
        sepal_length = float(data["sepal_length"])
        sepal_width = float(data["sepal_width"])
        petal_length = float(data["petal_length"])
        petal_width = float(data["petal_width"])

        # Create feature array in the SAME ORDER
        # used while training the model
        features = np.array([[
            sepal_length,
            sepal_width,
            petal_length,
            petal_width
        ]])

        # Apply the same scaler used during training
        features_scaled = scaler.transform(features)

        # Predict encoded class
        prediction_encoded = model.predict(features_scaled)

        # Decode using LabelEncoder
        prediction = encoder.inverse_transform(prediction_encoded)

        return jsonify({
            "success": True,
            "species": prediction[0]
        })

    except KeyError as e:
        return jsonify({
            "success": False,
            "error": f"Missing field: {str(e)}"
        }), 400

    except ValueError:
        return jsonify({
            "success": False,
            "error": "Please enter valid numeric values."
        }), 400

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == "__main__":
       app.run(host="0.0.0.0", port=5000, debug=False)