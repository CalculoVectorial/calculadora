import cv2

def record_face():
    # Load the pre-trained face detection model
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Initialize camera
    cap = cv2.VideoCapture(0)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        if not ret:
            break

        # Convert to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            # Calculate face's position relative to the center
            center_x = x + w // 2 - frame.shape[1] // 2
            center_y = y + h // 2 - frame.shape[0] // 2

            print("X:", center_x, "Y:", center_y)

            with open("../src/datos.txt", "a") as file:
                file.write("," + str(center_x) + "," + str(center_y))
            # Draw rectangle around the face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Display the resulting frame
        cv2.imshow('Face Tracking', frame)

        # Check for user input to quit
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    # Release the camera and close all windows
    cap.release()
    cv2.destroyAllWindows()

with open("../src/datos.txt", "w") as file:
    file.write("0,0")
record_face()