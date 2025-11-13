from flask import Flask, request, jsonify, render_template
import joblib
import cv2
import os
import numpy as np
import mysql.connector
from mysql.connector import Error
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message

app = Flask(__name__)

# Flask-Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Use your SMTP server
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'hrithikpoojary24@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'pqyn obhw upnl xmdz'  # Replace with your email password
app.config['MAIL_DEFAULT_SENDER'] = 'hrithikpoojary24@gmail.com'

# Initialize Flask-Mail
mail = Mail(app)

# Load models and scaler
models = {
    "Logistic Regression": joblib.load("models/logistic_regression_model.pkl"),
    "Random Forest": joblib.load("models/random_forest_model.pkl"),
    "Decision Tree": joblib.load("models/decision_tree_model.pkl"),
    "SVM": joblib.load("models/svm_model.pkl"),
    "XGBoost": joblib.load("models/xgboost_model.pkl"),
    "KNN": joblib.load("models/knn_model.pkl")
}
scaler = joblib.load("models/scaler.pkl")
model_accuracies = joblib.load("models/model_accuracies.pkl")

# MySQL connection setup
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        database='stroke_prediction_email',
        user='root',
        password=''
    )


# Sending Mail
def send_email(name, email, prediction_result, risk, years_until_stroke, model_name, stroke):
    """
    Sends an email with the stroke prediction results and health recommendations.

    Args:
        name (str): The name of the user.
        email (str): The email address of the user.
        prediction_result (str): The final prediction result (e.g., "Stroke Detected" or "Normal").
        risk (str): The calculated risk factor (e.g., "High" or "15.8%").
        years_until_stroke (str): The estimated years until stroke (e.g., "20 years" or "Immediate risk detected").
        model_name (str): The name of the model used for prediction.
        stroke (int): 1 if stroke is detected, 0 otherwise.
    """
    subject = "Stroke Risk Prediction Result"

    # Set health recommendations based on stroke prediction
    if stroke == 0:
        general_health_recommendations = """
        - Maintain a balanced diet rich in fruits and vegetables.
        - Exercise for at least 30 minutes daily.
        - Avoid smoking and limit alcohol consumption.
        - Monitor and manage blood pressure and cholesterol.
        - Reduce stress through relaxation techniques.
        """
        health_message = f"""
        Estimated Years Until Stroke: {years_until_stroke}
        
        Here are some general health recommendations to maintain a healthy lifestyle:
        {general_health_recommendations}
        """
    else:
        specific_health_recommendations = """
        - Consult a doctor for stroke prevention strategies.
        - Consider a stroke rehabilitation plan.
        - Take prescribed medications as advised.
        - Focus on mental well-being and stress management.
        """
        health_message = f"""
        Here are some specific recommendations after stroke detection:
        {specific_health_recommendations}
        """

    # Email body
    body = f"""
    Hello {name},

    Your stroke risk prediction result is as follows:

    Prediction: {prediction_result}
    Stroke Risk: {risk}
    Estimated Years Until Stroke: {years_until_stroke}
    
    Algorithm Used: {model_name}

    Stay healthy and take care!

    {health_message}

    Regards,
    Stroke Prediction System
    """
    
    # Create and send the email
    try:
        msg = Message(subject, recipients=[email], body=body)
        mail.send(msg)
        print(f"Email sent successfully to {email}.")
    except Exception as e:
        print(f"Error sending email to {email}: {e}")




# Create table if not exists
def create_table():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                age INT,
                email VARCHAR(255),
                gender VARCHAR(50),
                smoking VARCHAR(50),
                alcohol VARCHAR(50),
                activity VARCHAR(50),
                hypertension VARCHAR(50),
                diabetes VARCHAR(50),
                residence_type VARCHAR(50),
                ever_married VARCHAR(50),
                previous_strokes VARCHAR(50),
                work_type VARCHAR(100),
                model VARCHAR(100),
                prediction VARCHAR(50),
                confidence FLOAT,
                accuracy FLOAT,
                risk_factor FLOAT,
                image_path VARCHAR(255),
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()
    except Error as e:
        print(f"Error: {e}")

create_table()

# Preprocess image for prediction
def preprocess_image(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (128, 128))
    img = img / 255.0
    img_flattened = img.flatten().reshape(1, -1)
    return img_flattened


# Predict function
def preprocess_and_predict(img_path, model, scaler):
    img_flattened = preprocess_image(img_path)
    img_scaled = scaler.transform(img_flattened)  # Use the same scaler as training
    prediction = model.predict(img_scaled)[0]
    confidence = None
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(img_scaled)[0]
        confidence = max(probabilities) * 100
    return prediction, confidence



# Save results to database
def save_results_to_db(user_data, model_name, prediction, confidence, accuracy, img_path,risk_factor,estimated_years):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO predictions 
            (name, age, email, gender, smoking, alcohol, activity, hypertension, diabetes, 
            residence_type, ever_married, previous_strokes, work_type, model, prediction, confidence, accuracy, image_path,risk_factor,estimated_years) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)
        """
        cursor.execute(query, (
            user_data['name'],
            user_data['age'],
            user_data['email'],
            user_data['gender'],
            user_data['smoking'],
            user_data['alcohol'],
            user_data['activity'],
            # user_data['heart_disease'],
            user_data['hypertension'],
            user_data['diabetes'],
            user_data['residence_type'],
            user_data['ever_married'],
            user_data['previous_strokes'],
            user_data['work_type'],
            model_name,
            prediction,
            confidence,
            accuracy,
            img_path,
            risk_factor,
            estimated_years
        ))
        conn.commit()
        cursor.close()
        conn.close()
    except Error as e:
        print(f"Error: {e}")




# Risk factor calculation
# def calculate_risk_factor(user_data):
#     base_risk = max(1, 80 - user_data['age'])
#     if user_data['hypertension'] == "Yes":
#         base_risk *= 1.5
#     if user_data['diabetes'] == "Yes":
#         base_risk *= 1.3
#     if user_data['residence_type'] == "Urban":
#         base_risk *= 1.2
#     if user_data['ever_married'] == "Yes":
#         base_risk *= 1.1
#     return min(base_risk, 100)




def calculate_risk_factor(user_data):
    # Base risk should not be directly (80 - age), as it gives high values for young people
    if user_data['age'] < 40:
        base_risk = 5  # Lower base risk for younger people
    elif user_data['age'] < 60:
        base_risk = 20  # Moderate risk for middle-aged individuals
    else:
        base_risk = 40  # Higher base risk for older people

    # Weighted risk factors
    risk_factors = {
        "hypertension": 1.5 if user_data['hypertension'] == "Yes" else 1.0,
        "diabetes": 1.3 if user_data['diabetes'] == "Yes" else 1.0,
        "residence_type": 1.2 if user_data['residence_type'] == "Urban" else 1.0,
        "ever_married": 1.1 if user_data['ever_married'] == "Yes" else 1.0,
        "smoking": 1.4 if user_data['smoking'] == "Yes" else 1.0,
        "alcohol": 1.2 if user_data['alcohol'] == "Yes" else 1.0,
        "activity": 0.9 if user_data['activity'] == "Active" else 1.0,
        "previous_strokes": 1.6 if user_data['previous_strokes'] == "Yes" else 1.0,
        "work_type": 1.1 if user_data['work_type'] in ["Private", "Self-employed"] else 1.0,
        "gender": 1.1 if user_data['gender'] == "Male" else 1.0
    }

    # Apply multipliers
    total_risk = base_risk
    for factor, weight in risk_factors.items():
        total_risk *= weight

    # Cap at 100%
    return min(total_risk, 100)

# Flask routes
@app.route("/")
def index():
    return render_template("index.html", model_names=list(models.keys()))



# @app.route("/predict_bulk", methods=["POST"])
# def predict_bulk():
#     if "images" not in request.files:
#         return jsonify({"error": "No file uploaded"}), 400
    
#     files = request.files.getlist("images")
    
#     if not files:
#         return jsonify({"error": "No images selected"}), 400

#     if len(files) > 10:
#         return jsonify({"error": "You can upload a maximum of 10 images."}), 400
    
#     user_data = {
#     "name": request.form.get("name"),
#     "age": int(request.form.get("age")),
#     "email": request.form.get("email"),
#     "gender": request.form.get("gender"),
#     "smoking": request.form.get("smoking"),
#     "alcohol": request.form.get("alcohol"),
#     "activity": request.form.get("activity"),
#     "hypertension": request.form.get("hypertension"),
#     "diabetes": request.form.get("diabetes"),
#     "residence_type": request.form.get("residence_type"),
#     "ever_married": request.form.get("ever_married"),
#     "previous_strokes": request.form.get("previous_strokes"),
#     "work_type": request.form.get("work_type")  # Ensure this field is retrieved
# }

    
#     # Get selected model
#     model_name = request.form.get("model")
#     model = models.get(model_name)
    
#     if not model:
#         return jsonify({"error": "Invalid model selected"}), 400
    
#     results = []
#     stroke_count = 0
#     normal_count = 0

#     for file in files:
#         filename = secure_filename(file.filename)  # Sanitize filename
#         img_path = os.path.join("static", "uploads", filename)  # Save in static/uploads
#         file.save(img_path)

#         try:
#         # Make prediction
#             prediction, confidence = preprocess_and_predict(img_path, model, scaler)
#             accuracy = model_accuracies.get(model_name, "Not available")

#             if prediction == 1:  # Stroke detected
#                 stroke_count += 1
#             else:  # Normal detected
#                 normal_count += 1

#         # Calculate risk factor and estimated years
#             risk_factor = calculate_risk_factor(user_data)  # Calculate the risk factor before passing to DB
#             estimated_years = max(1, int(80 - user_data['age']))  # Calculate estimated years before passing to DB

#             result = {
#             "Model": model_name,
#             "Prediction": "Stroke" if prediction == 1 else "Normal",
#             "Confidence": f"{confidence:.2f}%" if confidence else "Not available",
#             "Model Accuracy": f"{accuracy * 100:.2f}%" if isinstance(accuracy, float) else accuracy,
#             "Image Path": "uploads/" + filename
#         }

#         # Save each result in the database, now with calculated risk_factor and estimated_years
#             save_results_to_db(user_data, model_name, result["Prediction"], confidence, accuracy, result["Image Path"], risk_factor, estimated_years)
#             results.append(result)

#         except Exception as e:
#             return jsonify({"error": f"Error processing image {file.filename}: {str(e)}"}), 500

#     # Determine final prediction based on counts
#     if stroke_count > normal_count:
#         final_result = {
#             "Final Prediction": "Stroke Detected",
#             "Suggestion": "Please consult a doctor immediately.",
#             "Algorithm": model_name,
#             "Accuracy": f"{model_accuracies[model_name] * 100:.2f}%",
#             "Risk Factor": "High",
#             "Estimated Years Until Stroke": "Immediate risk detected. Consult a doctor."
#         }
#     else:
#         # Calculate risk factor and estimated years until stroke
#         risk_factor = calculate_risk_factor(user_data)
#         estimated_years = max(1, int(80 - user_data['age']))
        
#         final_result = {
#             "Final Prediction": "Normal",
#             "General Health Recommendations": [
#                 "Maintain a balanced diet rich in fruits and vegetables.",
#                 "Exercise for at least 30 minutes daily.",
#                 "Avoid smoking and limit alcohol consumption.",
#                 "Monitor and manage blood pressure and cholesterol."
#             ],
#             "Algorithm": model_name,
#             "Accuracy": f"{model_accuracies[model_name] * 100:.2f}%",
#             "Risk Factor": f"{risk_factor:.2f}%",
#             "Estimated Years Until Stroke": f"{estimated_years} years"
#         }

#     return render_template("result_bulk.html", results=results, final_result=final_result, stroke_count=stroke_count, normal_count=normal_count,risk_factor=risk_factor,estimated_years=estimated_years)


@app.route("/predict_bulk", methods=["POST"])
def predict_bulk():
    if "images" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    files = request.files.getlist("images")
    
    if not files:
        return jsonify({"error": "No images selected"}), 400

    if len(files) > 10:
        return jsonify({"error": "You can upload a maximum of 10 images."}), 400
    
    user_data = {
        "name": request.form.get("name"),
        "age": int(request.form.get("age")),
        "email": request.form.get("email"),
        "gender": request.form.get("gender"),
        "smoking": request.form.get("smoking"),
        "alcohol": request.form.get("alcohol"),
        "activity": request.form.get("activity"),
        "hypertension": request.form.get("hypertension"),
        "diabetes": request.form.get("diabetes"),
        "residence_type": request.form.get("residence_type"),
        "ever_married": request.form.get("ever_married"),
        "previous_strokes": request.form.get("previous_strokes"),
        "work_type": request.form.get("work_type")
    }
    
    # Get selected model
    model_name = request.form.get("model")
    model = models.get(model_name)
    
    if not model:
        return jsonify({"error": "Invalid model selected"}), 400
    
    results = []
    stroke_count = 0
    normal_count = 0

    for file in files:
        filename = secure_filename(file.filename)
        img_path = os.path.join("static", "uploads", filename)
        file.save(img_path)

        try:
            # Make prediction
            prediction, confidence = preprocess_and_predict(img_path, model, scaler)
            accuracy = model_accuracies.get(model_name, "Not available")

            if prediction == 1:  # Stroke detected
                stroke_count += 1
            else:  # Normal detected
                normal_count += 1

            # Calculate risk factor and estimated years
            risk_factor = calculate_risk_factor(user_data)
            estimated_years = max(1, int(80 - user_data['age']))

            result = {
                "Model": model_name,
                "Prediction": "Stroke" if prediction == 1 else "Normal",
                "Confidence": f"{confidence:.2f}%" if confidence else "Not available",
                "Model Accuracy": f"{accuracy * 100:.2f}%" if isinstance(accuracy, float) else accuracy,
                "Image Path": "uploads/" + filename
            }

            # Save each result in the database
            save_results_to_db(user_data, model_name, result["Prediction"], confidence, accuracy, result["Image Path"], risk_factor, estimated_years)
            results.append(result)

        except Exception as e:
            return jsonify({"error": f"Error processing image {file.filename}: {str(e)}"}), 500

    # Determine final prediction based on counts
    if stroke_count > normal_count:
        final_result = {
            "Final Prediction": "Stroke Detected",
            "Suggestion": "Please consult a doctor immediately.",
            "Algorithm": model_name,
            "Accuracy": f"{model_accuracies[model_name] * 100:.2f}%",
            "Risk Factor": "High",
            "Estimated Years Until Stroke": "Immediate risk detected. Consult a doctor."
        }
    else:
        # Calculate risk factor and estimated years until stroke
        risk_factor = calculate_risk_factor(user_data)
        estimated_years = max(1, int(80 - user_data['age']))
        
        final_result = {
            "Final Prediction": "Normal",
            "General Health Recommendations": [
                "Maintain a balanced diet rich in fruits and vegetables.",
                "Exercise for at least 30 minutes daily.",
                "Avoid smoking and limit alcohol consumption.",
                "Monitor and manage blood pressure and cholesterol."
            ],
            "Algorithm": model_name,
            "Accuracy": f"{model_accuracies[model_name] * 100:.2f}%",
            "Risk Factor": f"{risk_factor:.2f}%",
            "Estimated Years Until Stroke": f"{estimated_years} years"
        }

    # Send email with prediction results
    try:
        send_email(
            name=user_data['name'],
            email=user_data['email'],
            prediction_result=final_result["Final Prediction"],
            risk=final_result["Risk Factor"],
            years_until_stroke=final_result["Estimated Years Until Stroke"],
            model_name=model_name,
            stroke=1 if stroke_count > normal_count else 0
        )
        email_sent = True
    except Exception as e:
        print(f"Error sending email: {e}")
        email_sent = False

    return render_template(
        "result_bulk.html",
        results=results,
        final_result=final_result,
        stroke_count=stroke_count,
        normal_count=normal_count,
        risk_factor=risk_factor,
        estimated_years=estimated_years,
        email_sent=email_sent,
        email=user_data['email']
    )

if __name__ == "__main__":
    os.makedirs("static/uploads", exist_ok=True)
    # app.run(debug=True)
    app.run(port=5001)
