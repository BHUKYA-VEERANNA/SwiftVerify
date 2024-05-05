import cv2
import numpy as np
import os, subprocess
import argparse
import warnings
import time
import threading
import pyttsx3  # for voice output

from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi

from src.anti_spoof_predict import AntiSpoofPredict
from src.generate_patches import CropImage
from src.utility import parse_model_name

warnings.filterwarnings('ignore')

def check_image(image):
    height, width, _ = image.shape
    aspect_ratio = width / height
    if abs(aspect_ratio - 4 / 3) > 0.01:  # Allowing a small deviation
        print(f"Image is not appropriate!!!\nHeight/Width ratio should be 4/3. Current ratio is {aspect_ratio:.2f}.")
        return False
    else:
        return True

def resize_frame(frame, target_width, target_height):
    return cv2.resize(frame, (target_width, target_height))

def test(frame, model_dir, device_id, target_width, target_height):
    model_test = AntiSpoofPredict(device_id)
    image_cropper = CropImage()

    result = check_image(frame)
    if result is False:
        return

    if frame.shape[1] != target_width or frame.shape[0] != target_height:
        frame = resize_frame(frame, target_width, target_height)

    image_bbox = model_test.get_bbox(frame)
    prediction = np.zeros((1, 3))
    test_speed = 0

    for model_name in os.listdir(model_dir):
        h_input, w_input, model_type, scale = parse_model_name(model_name)
        param = {
            "org_img": frame,
            "bbox": image_bbox,
            "scale": scale,
            "out_w": w_input,
            "out_h": h_input,
            "crop": True,
        }
        if scale is None:
            param["crop"] = False
        img = image_cropper.crop(**param)
        start = time.time()
        prediction += model_test.predict(img, os.path.join(model_dir, model_name))
        test_speed += time.time() - start

    label = np.argmax(prediction)
    value = prediction[0][label] / 2
    if label == 1:
        result_text = "Real Face, Attendance marked successfully!!"
        color = (0, 255, 0)  # Green for real
        speak_text = "Real face detected, attendance marked successfully!"
    else:
        result_text = "Fake Face Detected"
        color = (255, 0, 0)  # Red for fake
        speak_text = "Fake face, can't proceed further"

    return result_text, color, speak_text, image_bbox

class FaceRecognitionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("C:/Users/bveer/OneDrive/Desktop/Major Project/Code/PyQt/UI_Files/face_recognition.ui", self)

        self.model_dir = "C:/Users/bveer/OneDrive/Desktop/Major Project/Code/PyQt/resources/anti_spoof_models"
        self.device_id = 0
        self.target_width = 640
        self.target_height = 480

        self.pushButton.clicked.connect(self.open_voice_verification)  # Connect button clicked signal to open_voice_verification method

        self.start_camera()

    def start_camera(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.target_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.target_height)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(10)  # Update every 10 milliseconds

    def display_frame(self, frame):
        # Convert OpenCV frame to QImage
        image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(image)

        # Display frame in label_2
        self.label_2.setPixmap(pixmap)
        self.label_2.setScaledContents(True)

    def paintEvent(self, event):
        # Draw bounding box on the image
        if hasattr(self, 'bbox'):
            painter = QPainter(self.label_2.pixmap())
            color = QColor(*self.color)
            painter.setPen(QPen(color, 2, Qt.SolidLine))  # Use color determined by test function
            x, y, w, h = self.bbox
            painter.drawRect(x, y, w, h)
            painter.end()

    def update_frame(self):
        ret, frame = self.cap.read()

        if not ret:
            print("Error: Unable to capture frame.")
            return

        result_text, color, speak_text, bbox = test(frame, self.model_dir, self.device_id, self.target_width, self.target_height)

        self.color = color  # Store color for painting
        self.bbox = bbox
        self.display_frame(frame)
        self.update()

        # Display result in label_3
        self.label_3.setText(result_text)
        self.label_3.setStyleSheet("color: rgb({},{},{}); font-weight: bold;".format(*color))

        # Text to speech
        engine = pyttsx3.init()
        engine.say(speak_text)
        engine.runAndWait()

    def open_voice_verification(self):
        # Get the directory of the current script
        current_directory = os.path.dirname(os.path.realpath(__file__))

        # Construct the path to Voice_verification.py
        voice_verification_path = os.path.join(current_directory, 'app_voice.py')

        # Check if Voice_verification.py exists
        if os.path.exists(voice_verification_path):
            # Execute Voice_verification.py using subprocess
            subprocess.Popen(['python', voice_verification_path])
            # Close the current window
            self.close()
        else:
            print("Error: Voice_verification.py file not found at:", voice_verification_path)

    def open_face_recognition_page(self):
        # Close the current window
        self.close()
        # Get the directory of the current script
        current_directory = os.path.dirname(os.path.realpath(__file__))

        # Construct the path to app_face.py
        face_recognition_path = os.path.join(current_directory, 'app_face.py')

        # Check if app_face.py exists
        if os.path.exists(face_recognition_path):
            # Execute app_face.py using subprocess
            subprocess.Popen(['python', face_recognition_path])
        else:
            print("Error: app_face.py file not found at:", face_recognition_path)

    def setup_buttons(self):
        self.pushButton.clicked.connect(self.open_voice_verification)  # Connect "continue" button clicked signal to open_voice_verification method
        # You can connect other buttons here if needed

    def __init__(self):
        super().__init__()
        loadUi("C:/Users/bveer/OneDrive/Desktop/Major Project/Code/PyQt/UI_Files/face_recognition.ui", self)

        self.model_dir = "C:/Users/bveer/OneDrive/Desktop/Major Project/Code/PyQt/resources/anti_spoof_models"
        self.device_id = 0
        self.target_width = 640
        self.target_height = 480

        self.setup_buttons()  # Setup button connections

        self.start_camera()

if __name__ == "__main__":
    app = QApplication([])
    window = FaceRecognitionApp()
    window.show()
    app.exec_()
