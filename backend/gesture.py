import cv2
import mediapipe as mp
import numpy as np
import tensorflow as tf
import time
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource (for PyInstaller compatibility). """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)

# Construct model and label paths using resource_path
model_path = resource_path("model/keras_model.h5")
labels_path = resource_path("model/labels.txt")
# Load the model and labels
model = tf.keras.models.load_model(model_path)
with open(labels_path, "r") as f:
    labels = f.read().splitlines()

# Initialize mediapipe for hand detection
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.6
)

# Define the function to detect hand gesture
def detect_gesture():
    cap = cv2.VideoCapture(0)
    offset = 30
    model_input_size = 224
    CONFIDENCE_THRESHOLD = 0.8

    detected_gesture = None
    gesture_detected = False
    start_time = time.time()  # Start timer for 20 seconds

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)  # Flip the frame to create a mirror image
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Hand detection
        results = hands.process(frame_rgb)

        # inside detect_gesture()

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Get hand landmark coordinates
                h, w, _ = frame.shape
                x_list = [int(landmark.x * w) for landmark in hand_landmarks.landmark]
                y_list = [int(landmark.y * h) for landmark in hand_landmarks.landmark]
                x_min, x_max = min(x_list) - offset, max(x_list) + offset
                y_min, y_max = min(y_list) - offset, max(y_list) + offset

                # Clamp coordinates within frame boundaries
                x_min = max(0, x_min)
                y_min = max(0, y_min)
                x_max = min(w, x_max)
                y_max = min(h, y_max)

                # Check for valid crop area
                if x_max - x_min == 0 or y_max - y_min == 0:
                    continue  # skip this frame if invalid

                # Crop and resize the hand for input to the model
                cropped = frame[y_min:y_max, x_min:x_max]
                resized = cv2.resize(cropped, (model_input_size, model_input_size))
                input_data = np.expand_dims(resized, axis=0).astype(np.float32) / 255.0

                # Make prediction
                prediction = model.predict(input_data)
                confidence = np.max(prediction)
                predicted_index = np.argmax(prediction)

                if confidence > CONFIDENCE_THRESHOLD and (predicted_index == 2 or predicted_index == 3):
                    predicted_label = labels[predicted_index]
                    detected_gesture = predicted_label
                    gesture_detected = True
                    break  

        # Exit if a gesture is detected
        if gesture_detected:
            break
        
        elapsed_time = time.time() - start_time
        if elapsed_time > 20:  # If no gesture detected in 20 seconds, exit and return none
            detect_gesture = "none"
            break  

        # Check if 'q' is pressed to break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    return detected_gesture