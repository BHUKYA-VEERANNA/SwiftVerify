import cv2
import numpy as np
import os
import argparse
import warnings
import time

from src.anti_spoof_predict import AntiSpoofPredict
from src.generate_patches import CropImage
from src.utility import parse_model_name

warnings.filterwarnings('ignore')

#SAMPLE_IMAGE_PATH = "D:/Face_Detection_Real_Fake/Silent-Face-Anti-Spoofing-master/images/sample/"

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
        result_text = "Real Score: {:.2f}".format(value)
        color = (0, 255, 0)
    else:
        result_text = "Fake Score: {:.2f}".format(value)
        color = color = (0, 0, 255)

    cv2.rectangle(frame, (image_bbox[0], image_bbox[1]),
                  (image_bbox[0] + image_bbox[2], image_bbox[1] + image_bbox[3]), color, 2)
    cv2.putText(frame, result_text, (image_bbox[0], image_bbox[1] - 5), cv2.FONT_HERSHEY_COMPLEX, 0.5 * frame.shape[0] / 1024, color)

    return frame

def main(model_dir, device_id, target_width, target_height):
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, target_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, target_height)

    window_name = "Frame"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, target_width, target_height)
    
    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Unable to capture frame.")
            break

        frame = test(frame, model_dir, device_id, target_width, target_height)

        cv2.imshow(window_name, frame)
        
        # Get the screen resolution
        screen_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        screen_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        
        # Calculate the position to center the window
        x = int((screen_width - target_width) / 2)
        y = int((screen_height - target_height) / 2)
        
        cv2.moveWindow(window_name, x, y)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    desc = "Real-time face anti-spoofing detection"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("--device_id", type=int, default=0, help="which GPU id, [0/1/2/3]")
    parser.add_argument("--model_dir", type=str, default="C:/Users/bveer/Dropbox/4-2 B.Tech/Major Project/Code/Python_GUI/resources/anti_spoof_models", help="model library used to test")
    parser.add_argument("--target_width", type=int, default=640, help="target width for resizing the frame")
    parser.add_argument("--target_height", type=int, default=480, help="target height for resizing the frame")
    args = parser.parse_args()

    main(args.model_dir, args.device_id, args.target_width, args.target_height)
