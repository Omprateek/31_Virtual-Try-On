# app.py
from flask import Flask, render_template, Response
import cv2
import mediapipe as mp
import math

app = Flask(__name__)

# Initialize MediaPipe Hands model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Load the watch image with a transparent background (PNG format)
watch_image = cv2.imread('./static/Watch3.png', cv2.IMREAD_UNCHANGED)

# Initialize VideoCapture
cap = cv2.VideoCapture(0)

def generate_frames():
    while True:
        # Read a frame from the video feed
        ret, frame = cap.read()

        # Convert the frame to RGB (MediaPipe hands model requires RGB input)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame with MediaPipe Hands model
        results = hands.process(rgb_frame)

        # If hands are detected, overlay the watch image on the detected hand
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Get the coordinates of the wrist and index finger tip
                wrist = (int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x * frame.shape[1]),
                         int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y * frame.shape[0]))

                tip_of_index_finger = (int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * frame.shape[1]),
                                        int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * frame.shape[0]))

                # Calculate the angle between the wrist and index finger tip
                angle_rad = math.atan2(tip_of_index_finger[1] - wrist[1], tip_of_index_finger[0] - wrist[0])
                angle_deg = math.degrees(angle_rad)

                # Rotate the watch image by the calculated angle
                rotated_watch = cv2.warpAffine(watch_image, cv2.getRotationMatrix2D((watch_image.shape[1] // 2, watch_image.shape[0] // 2), angle_deg, 1.0), (watch_image.shape[1], watch_image.shape[0]))

                # Resize the rotated watch image
                resized_rotated_watch = cv2.resize(rotated_watch, (int(0.110 * rotated_watch.shape[1]), int(0.1 * rotated_watch.shape[0])))

                # Calculate the position to overlay the resized rotated watch image on the hand
                x_offset = wrist[0] - int(0.5 * resized_rotated_watch.shape[1])  # Center the watch on the hand
                y_offset = wrist[1] - int(0.45 * resized_rotated_watch.shape[0])  # Adjust the vertical offset based on your watch images

                # Ensure the offsets are within bounds
                x_offset = max(0, x_offset)
                y_offset = max(0, y_offset)

                # Calculate the region of interest for overlaying the watch image
                roi_width = min(resized_rotated_watch.shape[1], frame.shape[1] - x_offset)
                roi_height = min(resized_rotated_watch.shape[0], frame.shape[0] - y_offset)

                # Overlay the resized rotated watch image on the frame within the region of interest
                for c in range(0, 3):
                    frame[y_offset:y_offset + roi_height, x_offset:x_offset + roi_width, c] = \
                        frame[y_offset:y_offset + roi_height, x_offset:x_offset + roi_width, c] * \
                        (1 - resized_rotated_watch[:roi_height, :roi_width, 3] / 255.0) + \
                        resized_rotated_watch[:roi_height, :roi_width, c] * (resized_rotated_watch[:roi_height, :roi_width, 3] / 255.0)

        # Encode the frame as JPEG
        _, jpeg = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')  # Create an HTML file for the UI

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
