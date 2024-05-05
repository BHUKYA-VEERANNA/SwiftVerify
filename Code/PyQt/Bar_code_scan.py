import numpy as np
import cv2
import winsound
from pyzbar.pyzbar import decode

def decode_image(im):
    decoded_objects = decode(im)

    return decoded_objects

def detect_glare(image):
    if image is None or image.size == 0:
        return 0.0  # Return 0 glare percentage for empty or invalid images

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Calculate mean pixel intensity as a measure of glare
    mean_intensity = np.mean(gray)

    # Normalize mean intensity to the range [0, 1]
    glare_percentage = (mean_intensity / 255.0)

    return glare_percentage

def display(im, decoded_objects):
    scanned_data = set()  # To store scanned data and ensure it's printed only once

    for decoded_object in decoded_objects:
        x, y, w, h = decoded_object.rect

        # Ensure that the bounding box falls within the image bounds
        if x < 0 or y < 0 or x + w > im.shape[1] or y + h > im.shape[0]:
            continue  # Skip processing if the bounding box is out of bounds

        # Extract the region of interest (ROI) from the image
        roi = im[y:y+h, x:x+w]

        # Calculate glare percentage for the ROI
        glare_percentage = detect_glare(roi)

        if glare_percentage > 0.5:  # Adjust the threshold as needed
            # Display warning in red for barcodes scanned from electronic devices
            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 0, 255), 3)
            cv2.putText(im, "Not accepted from Electronic Devices", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        else:
            # Display bounding box for accepted barcodes
            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 3)
            cv2.putText(im, str(decoded_object.data), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            winsound.Beep(1000, 200)  # Play beep sound once barcode is scanned

            # Add scanned data to the set
            scanned_data.add(decoded_object.data.decode('utf-8'))

    cv2.imshow("Barcode Scan", im)
    cv2.waitKey(1)  # Adjust the waitKey delay to control the frame rate

    return scanned_data

if __name__ == '__main__':
    # Open the default camera (index 0)
    cap = cv2.VideoCapture(0)

    scanned_data = set()  # To store scanned data and ensure it's printed only once

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        if not ret:
            print("Error: Unable to capture video.")
            break

        # Decode the frame to detect barcodes
        decoded_objects = decode_image(frame)

        # Display the frame with bounding boxes around detected barcodes
        scanned_data.update(display(frame, decoded_objects))

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture when finished
    cap.release()
    cv2.destroyAllWindows()