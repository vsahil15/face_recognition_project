import cv2
import os
import numpy as np
from insightface.app import FaceAnalysis

# Load InsightFace model
app = FaceAnalysis()
app.prepare(ctx_id=-1)

# -------------------------
# Create Sahil Profile
# -------------------------
dataset_path = "dataset/sahil"

embeddings = []

for file in os.listdir(dataset_path):

    if file.endswith(".jpg"):

        img_path = os.path.join(dataset_path, file)

        img = cv2.imread(img_path)

        faces = app.get(img)

        if len(faces) > 0:
            embeddings.append(faces[0].embedding)

if len(embeddings) == 0:
    print("No faces found in dataset!")
    exit()

# Average embedding of all images
sahil_profile = np.mean(embeddings, axis=0)

print("Sahil profile created successfully!")

# -------------------------
# Start Webcam
# -------------------------
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:

    ret, frame = cap.read()

    if not ret:
        break

    faces = app.get(frame)

    for face in faces:

        embedding = face.embedding

        distance = np.linalg.norm(
            embedding - sahil_profile
        )

        x1, y1, x2, y2 = map(int, face.bbox)

        if distance < 25:
            
            print("Welcome Sahil")

            cap.release()
            cv2.destroyAllWindows()

            exit()
           

        else:

            label = f"Unknown ({distance:.2f})"

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            label,
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

    cv2.imshow("Face Recognition", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()