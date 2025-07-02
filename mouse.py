import cv2
import mediapipe as mp
import pyautogui
import numpy as np

# Setup
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
cap = cv2.VideoCapture(0)

# Set webcam resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

screen_width, screen_height = pyautogui.size()
prev_y = 0
current_action = ""

with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.8) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            continue

        image = cv2.flip(image, 1)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        result = hands.process(image_rgb)
        h, w, _ = image.shape

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                landmarks = hand_landmarks.landmark

                tip_ids = [4, 8, 12, 16, 20]
                fingers = []

                # Thumb
                fingers.append(landmarks[4].x > landmarks[3].x)

                # Other four fingers
                for i in range(1, 5):
                    fingers.append(landmarks[tip_ids[i]].y < landmarks[tip_ids[i] - 2].y)

                total_fingers = fingers.count(True)

                # Get index finger coordinates
                index_finger = landmarks[8]
                x = int(index_finger.x * w)
                y = int(index_finger.y * h)
                screen_x = screen_width * index_finger.x
                screen_y = screen_height * index_finger.y

                # Smooth cursor movement
                current_mouse = np.array(pyautogui.position())
                target_mouse = np.array([screen_x, screen_y])
                smoothed = current_mouse + 0.2 * (target_mouse - current_mouse)

                # -------------------- Gesture Control --------------------

                # Move mouse: Index only
                if fingers == [False, True, False, False, False]:
                    pyautogui.moveTo(int(smoothed[0]), int(smoothed[1]))
                    current_action = "Mouse Move"
                    prev_y = 0

                # Left click: Index + Thumb
                elif fingers == [True, True, False, False, False]:
                    pyautogui.click()
                    current_action = "Left Click"
                    prev_y = 0

                # Scroll: Index + Middle
                elif fingers == [False, True, True, False, False]:
                    scroll_y = landmarks[8].y
                    if prev_y != 0:
                        diff = scroll_y - prev_y
                        if abs(diff) > 0.01:
                            if diff > 0:
                                pyautogui.scroll(-30)
                                current_action = "Scroll Down"
                            else:
                                pyautogui.scroll(30)
                                current_action = "Scroll Up"
                    prev_y = scroll_y

                # Right click: Index + Ring
                elif fingers == [False, True, False, True, False]:
                    pyautogui.click(button='right')
                    current_action = "Right Click"
                    prev_y = 0

                # Exit: All 5 fingers
                elif total_fingers == 5:
                    current_action = "Exiting"
                    cv2.putText(image, current_action, (x, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
                    cap.release()
                    cv2.destroyAllWindows()
                    exit()

                else:
                    current_action = ""
                    prev_y = 0

        # Show current action
        if current_action != "":
            cv2.putText(image, f'Gesture: {current_action}', (10, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 3)

        # Display webcam feed
        cv2.imshow('Gesture Mouse Controller', image)

        # Exit with ESC
        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
