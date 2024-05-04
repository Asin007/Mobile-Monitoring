from flask import Flask, render_template
import cv2
import numpy as np
from pymongo import MongoClient
from twilio.rest import Client
from datetime import datetime
from deepface import DeepFace

app = Flask(__name__)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['face_database']
collection = db['faces']

# Twilio credentials
account_sid = ''
auth_token = ''
twilio_client = Client(account_sid, auth_token)
twilio_number = '+12514511811'

# Load pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Function to detect faces in an image
def detect_faces(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    return faces

# Function to recognize faces in the database
def recognize_face(image):
    for record in collection.find():
        stored_face = np.frombuffer(record['face'], dtype=np.uint8)
        stored_face = cv2.imdecode(stored_face, cv2.IMREAD_COLOR)
        if stored_face is None:
            print("Error: Unable to load stored face image.")
            continue
        result = DeepFace.verify(image, stored_face, enforce_detection=False)
        if result['verified']:
            return record
    return None

# Function to send SMS using Twilio
def send_sms(recipient_number, message):
    twilio_client.messages.create(
        to=recipient_number,
        from_=twilio_number,
        body=message
    )
    print("SMS sent to:", recipient_number)

# Route to match the provided image path and upload details
@app.route('/')
def match_and_upload():
    image_path = r"C:\Users\Abarna Dutta\OneDrive\Documents\basic_upload\phone.jpg"  # Specify the path to the pre-existing image
    image = cv2.imread(image_path)
    if image is None:
        return "Error: Unable to read image"
    
    faces = detect_faces(image)
    if len(faces) > 0:
        for (x, y, w, h) in faces:
            face = image[y:y+h, x:x+w]
            matched_info = recognize_face(face)
            if matched_info:
                # Store matched details in the database
                collection.insert_one({
                    'name': matched_info['name'],
                    'aadhar_number': matched_info['aadhar_number'],
                    'phone_number': matched_info['phone_number'],
                    'email': matched_info['email'],
                    'timestamp': datetime.now()
                })
                # Send SMS
                message = f"Hello {matched_info['name']}! Your detected using mobile phone."
                send_sms(matched_info['phone_number'], message)
                # Print details from database
                print("Matched Face Details:")
                print("Name:", matched_info['name'])
                print("Aadhar Number:", matched_info['aadhar_number'])
                print("Phone Number:", matched_info['phone_number'])
                print("Email:", matched_info['email'])
                return render_template('match.html', name=matched_info['name'],
                                       aadhar_number=matched_info['aadhar_number'],
                                       phone_number=matched_info['phone_number'],
                                       email=matched_info['email']
                                       )
        return render_template('no_match.html')
    else:
        return "No faces detected in the provided image"

if __name__ == "__main__":
    app.run(debug=True)
    print("Server updated.")
