import tkinter as tk
import threading
import cv2
import numpy as np
import os
from insightface.app import FaceAnalysis

# -----------------------
# Create Sahil Profile
# -----------------------

app = FaceAnalysis()
app.prepare(ctx_id=-1)

dataset_path = "dataset/sahil"

embeddings = []

for file in os.listdir(dataset_path):

    if file.endswith(".jpg"):

        img = cv2.imread(
            os.path.join(dataset_path, file)
        )

        faces = app.get(img)

        if len(faces) > 0:
            embeddings.append(
                faces[0].embedding
            )

sahil_profile = np.mean(
    embeddings,
    axis=0
)

# -----------------------
# Tkinter Lock Screen
# -----------------------

root = tk.Tk()

root.attributes("-fullscreen", True)

label = tk.Label(
    root,
    text="🔒 SYSTEM LOCKED",
    font=("Arial", 40)
)

label.pack(pady=100)

status = tk.Label(
    root,
    text="Looking for Sahil...",
    font=("Arial", 20)
)

status.pack()

# Emergency exit
def exit_app(event=None):
    root.destroy()

root.bind("<Control-Shift-Q>", exit_app)

# -----------------------
# Face Recognition Thread
# -----------------------

def recognize():

    cap = cv2.VideoCapture(0)

    while True:

        ret, frame = cap.read()

        if not ret:
            continue

        faces = app.get(frame)

        for face in faces:

            embedding = face.embedding

            distance = np.linalg.norm(
                embedding - sahil_profile
            )

            if distance < 25:

                status.config(
                    text="Welcome Sahil!"
                )

                cap.release()

                root.after(
                    1000,
                    root.destroy
                )

                return

        cv2.waitKey(1)

threading.Thread(
    target=recognize,
    daemon=True
).start()

root.mainloop()