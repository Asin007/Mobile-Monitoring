import os
from pymongo import MongoClient
from PIL import Image

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/face_database')
db = client['face_database']
collection = db['faces']

# Function to insert a single set of qqdata
def insert_single_data():
    # Dummy data for one person
    name = 'SOURAV PAL'
    aadhar_number = '1234 5678 9012'
    phone_number = '+91 8777371146'
    email = 'souravpal@gmail.com'
    image_path = r'C:\Users\Abarna Dutta\OneDrive\Documents\basic_upload\phone.jpg'  # Adjust the path to your image

    # Check if image file exists
    if not os.path.exists(image_path):
        print(f"Error: Image file '{image_path}' not found.")
        return

    # Load image
    image = Image.open(image_path)

    # Convert image to binary data
    with open(image_path, 'rb') as f:
        image_data = f.read()

    # Create document for MongoDB
    document = {
        'name': name,
        'aadhar_number': aadhar_number,
        'phone_number': phone_number,
        'email': email,
        'face': image_data
    }

    # Insert document into MongoDB collection
    collection.insert_one(document)
    print("Data inserted successfully.")

if __name__ == "__main__":
    insert_single_data()
