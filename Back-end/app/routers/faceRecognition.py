from fastapi import APIRouter, HTTPException,WebSocket
import cv2
import os
import numpy as np
from pathlib import Path
from plyer import notification
import base64
from fastapi.responses import HTMLResponse



router = APIRouter()

# Directories for storing images and model
IMAGE_DIR = "data"
MODEL_DIR = "trained_model"
Path(IMAGE_DIR).mkdir(parents=True, exist_ok=True)
Path(MODEL_DIR).mkdir(parents=True, exist_ok=True)

# Load the pre-trained face detector model
face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
face_recognizer = cv2.face.LBPHFaceRecognizer_create()

# Function to crop face from the image
def face_cropped(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        return img[y:y + h, x:x + w]
    return None

# Route to capture 100 images for a person
@router.post("/capture_images/{person_id}")
async def capture_images(person_id: str):
    try:
        # cap = cv2.VideoCapture('http://http://192.168.8.169:8080')
        cap = cv2.VideoCapture(0)
        img_id = 0
        person_dir = os.path.join(IMAGE_DIR, person_id)
        os.makedirs(person_dir, exist_ok=True)

        while True:
            ret, my_frame = cap.read()
            if not ret:
                break

            cropped_face = face_cropped(my_frame)
            if cropped_face is not None:
                img_id += 1
                face = cv2.resize(cropped_face, (450, 450))
                face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

                # Save the captured image in the specified directory
                file_name_path = f"{person_dir}/user.{person_id}.{img_id}.jpg"
                cv2.imwrite(file_name_path, face)

                # Display the image with a count
                cv2.putText(face, str(img_id), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                cv2.imshow("Cropped Face", face)

            # Break the loop if 'Enter' key is pressed or 100 images are captured
            if cv2.waitKey(1) == 13 or img_id == 100:
                break

        cap.release()
        cv2.destroyAllWindows()
        return {"message": f"Captured 100 images for person {person_id}"}
    except Exception as e:
        return {"error": str(e)}

# Route to train the model with captured images
@router.post("/train_model")
async def train_model():
    faces = []
    labels = []
    person_dirs = [d for d in os.listdir(IMAGE_DIR) if os.path.isdir(os.path.join(IMAGE_DIR, d))]

    for person_id in person_dirs:
        person_dir = os.path.join(IMAGE_DIR, person_id)
        label = int(person_id)

        for image_file in os.listdir(person_dir):
            if image_file.endswith(".jpg"):
                image_path = os.path.join(person_dir, image_file)
                image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                faces.append(image)
                labels.append(label)

    face_recognizer.train(faces, np.array(labels))
    model_path = os.path.join(MODEL_DIR, "face_model.xml")
    face_recognizer.save(model_path)

    return {"message": "Model trained and saved to face_model.xml"}

# Route to recognize a person in real-time
@router.post("/recognize_person")
async def recognize_person():
    try:
        # Load the trained model
        model_path = os.path.join(MODEL_DIR, "face_model.xml")
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read(model_path)

        # Load the face detector
        cascadePath = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(cascadePath)

        # Names corresponding to IDs
        names = ['','Banuka','Subaskar','Sasika']  # Modify this list with correct names

        # Initialize camera
        # cam = cv2.VideoCapture('rtsp://192.168.8.169:8080/h264_ulaw.sdp')
        cam = cv2.VideoCapture(0)
        minW = 0.1 * cam.get(3)
        minH = 0.1 * cam.get(4)
        font = cv2.FONT_HERSHEY_SIMPLEX

        while True:
            ret, img = cam.read()
            if not ret:
                raise HTTPException(status_code=500, detail="Failed to capture video")

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Detect faces in the frame
            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(int(minW), int(minH)),
            )

            for (x, y, w, h) in faces:
                # Draw a rectangle around the detected face
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)

                # Predict the ID and confidence for the detected face
                id, confidence = recognizer.predict(gray[y:y + h, x:x + w])

                 # Display the name and confidence on the video feed
                

                if confidence < 60:
                    person_name = names[id]
                    confidence_text = f"  {round(100 - confidence)}%"

                    # Log the identified person
                    print(f"{person_name} verified")
                    
                    # Turn off the camera and return a response
                    cam.release()
                    cv2.destroyAllWindows()
                    return {"message": f"{person_name} verified"}

                else:
                    person_name = "unknown"
                    confidence_text = f"  {round(100 - confidence)}%"

                    # Optional: You can send a notification or log here if an unknown person is detected
                    print(f"Unknown person detected with confidence: {confidence_text}")

                cv2.putText(img, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
                cv2.putText(img, str(confidence_text), (x + 5, y + h - 5), font, 1, (2, 255, 0), 1)

            cv2.imshow('camera', img)

            # Press 'ESC' to exit the loop
            k = cv2.waitKey(10) & 0xff
            if k == 27:
                break

        cam.release()
        cv2.destroyAllWindows()
        return {"message": "Recognition process completed"}

    except Exception as e:
        print("Exception happend")
        raise HTTPException(status_code=500, detail=str(e))
        cam.release()
        cv2.destroyAllWindows()


# @router.websocket("/")
# async def websocket_endpoint(websocket: WebSocket):
#     # Disable origin checks by accepting all origins
#     await websocket.accept()

#     try:
#         # Load the trained model
#         model_path = os.path.join(MODEL_DIR, "face_model.xml")
#         recognizer = cv2.face.LBPHFaceRecognizer_create()
#         recognizer.read(model_path)

#         # Load the face detector
#         cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
#         face_cascade = cv2.CascadeClassifier(cascade_path)

#         # Names corresponding to IDs
#         names = ['', 'Banuka', 'Subaskar']  # Modify this list with correct names

#         font = cv2.FONT_HERSHEY_SIMPLEX

#         while True:
#             data = await websocket.receive_text()
#             # Decode the base64 string to bytes
#             img_data = base64.b64decode(data)
#             # Convert the bytes to a numpy array and decode it as an image
#             nparr = np.frombuffer(img_data, np.uint8)
#             frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

#             if frame is not None:
#                 gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#                 # Detect faces in the frame
#                 faces = face_cascade.detectMultiScale(
#                     gray,
#                     scaleFactor=1.2,
#                     minNeighbors=5,
#                     minSize=(int(0.1 * frame.shape[1]), int(0.1 * frame.shape[0])),
#                 )

#                 for (x, y, w, h) in faces:
#                     # Predict the ID and confidence for the detected face
#                     id_, confidence = recognizer.predict(gray[y:y + h, x:x + w])

#                     if confidence < 60:
#                         person_name = names[id_]
#                         confidence_text = f"{round(100 - confidence)}%"

#                         # Log the identified person
#                         print(f"{person_name} verified with confidence {confidence_text}")

#                         # Send verification response back to the client
#                         await websocket.send(f"{person_name} verified with confidence {confidence_text}")

#                     else:
#                         confidence_text = f"{round(100 - confidence)}%"
#                         print(f"Unknown person detected with confidence {confidence_text}")
#                         await websocket.send(f"Unknown person detected with confidence {confidence_text}")

#     except WebSocketDisconnect:
#         print("Client disconnected")
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         await websocket.close()
