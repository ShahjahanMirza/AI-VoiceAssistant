import cv2



def capture_image():
    # Open the camera
    camera = cv2.VideoCapture(0)
    # Check if the camera is opened correctly
    if not camera.isOpened():
        print("Unable to open the camera")
    # Wait for the user to press 'q'
    while True:
        # Read a frame from the camera
        ret, frame = camera.read()
        # Display the frame
        cv2.imshow("Camera", frame)
        # Check if the user pressed 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # Release the camera and close all windows
    camera.release()
    cv2.destroyAllWindows()

    # Save the snapshot
    cv2.imwrite("./images/snapshot.png", frame)
