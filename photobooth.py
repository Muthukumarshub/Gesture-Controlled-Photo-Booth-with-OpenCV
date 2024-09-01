#Import all Required Packages
import cv2
import time
import mediapipe as mp

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

# Initialize the camera
cap = cv2.VideoCapture(0)

def count_fingers(hand_landmarks):
    """Count the number of fingers shown based on hand landmarks."""
    if hand_landmarks:
        # Get the landmarks for the thumb and fingers
        landmarks = hand_landmarks.landmark
        # Count fingers
        finger_count = 0
        # Check thumb
        if landmarks[mp_hands.HandLandmark.THUMB_TIP].y < landmarks[mp_hands.HandLandmark.THUMB_IP].y:
            finger_count += 1
        # Check other fingers
        for i in range(1, 5):
            if landmarks[mp_hands.HandLandmark(i * 4 + 2)].y < landmarks[mp_hands.HandLandmark(i * 4)].y:
                finger_count += 1
        return finger_count
    return 0

def capture_image_when_two_fingers_detected():
    print("Show two fingers to capture the image...")
    
    while True:
        # Read frame from the camera
        ret, frame = cap.read()
        
        if not ret:
            break

        # Convert the frame to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        # Draw hand landmarks and count fingers
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw landmarks
                mp.solutions.drawing_utils.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                # Count fingers
                finger_count = count_fingers(hand_landmarks)
                if finger_count == 2:
                    print("Two fingers detected! Capturing image in 3 seconds...")
                    time.sleep(3)
                    cv2.imwrite('captured_image.jpg', frame)
                    print("Image captured and saved as 'captured_image.jpg'")
                    return

        # Display the frame
        cv2.imshow('Camera Feed', frame)

        # Exit if 'Esc' key is pressed
        if cv2.waitKey(1) == 27:
            break

# Run the finger detection and image capture function
capture_image_when_two_fingers_detected()

# Release the camera and close windows
cap.release()
cv2.destroyAllWindows()
