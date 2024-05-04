import cv2
import torch
import torchvision.transforms as transforms
from torchvision.models.detection import fasterrcnn_resnet50_fpn

# Load a pre-trained Faster R-CNN model
model = fasterrcnn_resnet50_fpn(pretrained=True)
model.eval()

# Define the transformation to apply to the input images
transform = transforms.Compose([
    transforms.ToTensor(),
])

# Open the video capture
save='static/'
cap = cv2.VideoCapture(0)  # Use 0 for webcam, or provide the path to a video file

# Loop to read frames from the video feed
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame from BGR to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Convert the frame to a PyTorch tensor
    image_tensor = transform(rgb_frame).unsqueeze(0)  # Add a batch dimension

    # Make predictions
    with torch.no_grad():
        predictions = model(image_tensor)

    # Visualize the predictions
    for box, label, score in zip(predictions[0]['boxes'], predictions[0]['labels'], predictions[0]['scores']):
        box = box.cpu().numpy().astype(int)
        if label == 77 and score > 0.7:  # Class 77 represents mobile phone in COCO dataset
            cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)
            # Capture and save the image
            person_image = frame.copy()
            cv2.imwrite("phone.jpg", person_image)
            cv2.imwrite(save+"phone.jpg", person_image)

    # Display the resulting frame
    cv2.imshow('Mobile Phone Detection', frame)

    # Check for the 'q' key to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()