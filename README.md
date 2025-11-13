🧠 Brain Stroke Detection using MRI and CT Scans
📘 Overview

This project is an AI-powered Brain Stroke Detection System that classifies MRI and CT scan images as either Stroke or Non-Stroke.
It aims to assist medical professionals in early and efficient stroke diagnosis by leveraging Machine Learning and Deep Learning models.

⚙️ Features

🧩 Classifies brain scans (MRI/CT) into stroke / non-stroke categories

📈 Utilizes trained ML models (KNN, SVM, etc.)

📬 Includes an automated email alert system for patient results

🌐 Fully integrated with a web-based dashboard

💾 Supports real-time predictions from uploaded scan images

🧰 Tech Stack
Category	Tools & Libraries
Programming Language	Python 3.12
Frameworks	Flask / FastAPI (depending on your setup)
Machine Learning	scikit-learn, pandas, numpy, joblib
Visualization	matplotlib, seaborn
Deployment	GitHub, Render / AWS / Heroku
Email Integration	smtplib, Flask-Mail
🧩 Model Files

Due to GitHub’s 100 MB upload limit, the trained model files are hosted externally.
Please download them and place them in the models/ directory before running the project.

🔗 Download Models:

KNN Model (knn_model.pkl)

SVM Model (svm_model.pkl)

After downloading, the directory should look like this:

Brain_Stroke_email_project/
│
├── models/
│   ├── knn_model.pkl
│   └── svm_model.pkl
│
├── static/
├── templates/
├── app.py
├── requirements.txt
└── README.md

🚀 Setup Instructions
1️⃣ Clone the repository
git clone https://github.com/Hrixxy/Brainstroke.git
cd Brainstroke

2️⃣ Create & activate a virtual environment
python -m venv .venv
.venv\Scripts\activate   # (on Windows)

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Download & place model files

Place the .pkl files inside the models/ folder as shown above.

5️⃣ Run the application
python app.py


Visit your app in the browser at:
👉 http://127.0.0.1:5000/

📬 Email Notification Feature

Once a scan is classified, the system automatically sends an email alert to the registered patient or doctor with the prediction result.

📊 Future Enhancements

Integration with Deep Learning (CNN) models for higher accuracy

Real-time DICOM file processing

Enhanced dashboard analytics and visual reports

Docker-based deployment support
