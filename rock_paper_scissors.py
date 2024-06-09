import time

import cv2
import mediapipe as mp
import random
from collections import deque
import statistics as st

def calculate_winner(ai_choice, player_choice):
    if player_choice == "Invalid":
        return "Invalid!"
    if player_choice == ai_choice:
        return "Tie!"
    elif player_choice == "Rock" and ai_choice == "Scissors":
        return "You win!"
    elif player_choice == "Rock" and ai_choice == "Paper":
        return "AI wins!"
    elif player_choice == "Scissors" and ai_choice == "Rock":
        return "AI wins!"
    elif player_choice == "Scissors" and ai_choice == "Paper":
        return "You win!"
    elif player_choice == "Paper" and ai_choice == "Rock":
        return "You win!"
    elif player_choice == "Paper" and ai_choice == "Scissors":
        return "AI wins!"

def compute_fingers(hand_landmarks):
    count = 0
    if hand_landmarks[8][2] < hand_landmarks[6][2]:  # Index Finger
        count += 1
    if hand_landmarks[12][2] < hand_landmarks[10][2]:  # Middle Finger
        count += 1
    if hand_landmarks[16][2] < hand_landmarks[14][2]:  # Ring Finger
        count += 1
    if hand_landmarks[20][2] < hand_landmarks[18][2]:  # Pinky Finger
        count += 1
    if hand_landmarks[4][3] == "Left" and hand_landmarks[4][1] > hand_landmarks[3][1]:  # Thumb for Left Hand
        count += 1
    elif hand_landmarks[4][3] == "Right" and hand_landmarks[4][1] < hand_landmarks[3][1]:  # Thumb for Right Hand
        count += 1
    return count

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

webcam = cv2.VideoCapture(0)

cpu_choices = ["Rock", "Paper", "Scissors"]
ai_choice = "Nothing"
ai_score, player_score = 0, 0
winner_colour = (0, 255, 0)
player_choice, prev_player_choice = "Nothing", "Nothing"
hand_valid = False
display_values = ["Rock", "Invalid", "Scissors", "Invalid", "Invalid", "Paper"]
winner = "None"
de = deque(['Nothing'] * 5, maxlen=5)
previous_detection_time = 0

with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:

    while webcam.isOpened():
        success, image = webcam.read()
        if not success:
            print("Camera isn't working")
            continue

        image = cv2.flip(image, 1)

        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        handNumber = 0
        hand_landmarks = []
        isCounting = False
        count = 0

        if results.multi_hand_landmarks:
            isCounting = True

            for hand in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    hand,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())

                label = results.multi_handedness[handNumber].classification[0].label

                for id, landmark in enumerate(hand.landmark):
                    imgH, imgW, imgC = image.shape
                    xPos, yPos = int(landmark.x * imgW), int(landmark.y * imgH)
                    hand_landmarks.append([id, xPos, yPos, label])

                count = compute_fingers(hand_landmarks)

                handNumber += 1

        if isCounting and count <= 5:
            player_choice = display_values[count]
        elif isCounting:
            player_choice = "Invalid"
        else:
            player_choice = "Nothing"

        de.appendleft(player_choice)

        try:
            player_choice = st.mode(de)
        except st.StatisticsError:
            continue

        if player_choice != prev_player_choice:
            current_time = time.time()
            if current_time - previous_detection_time > 1:  # cooldown period of 1 second
                prev_player_choice = player_choice
                previous_detection_time = current_time
                ai_choice = random.choice(cpu_choices)
                winner = calculate_winner(ai_choice, player_choice)

                if winner == "You win!":
                    player_score += 1
                    winner_colour = (255, 0, 0)
                elif winner == "AI wins!":
                    ai_score += 1
                    winner_colour = (0, 0, 255)
                elif winner == "Invalid!" or winner == "Tie!":
                    winner_colour = (0, 255, 0)

        cv2.putText(image, "You", (90, 75),
                    cv2.FONT_HERSHEY_DUPLEX, 2, (255, 0, 0), 5)

        cv2.putText(image, "AI", (400, 75),
                    cv2.FONT_HERSHEY_DUPLEX, 2, (0, 0, 255), 5)

        cv2.putText(image, player_choice, (45, 375),
                    cv2.FONT_HERSHEY_DUPLEX, 2, (255, 0, 0), 5)

        cv2.putText(image, ai_choice, (350, 375),
                    cv2.FONT_HERSHEY_DUPLEX, 2, (0, 0, 255), 5)

        cv2.putText(image, winner, (250, 250),
                    cv2.FONT_HERSHEY_DUPLEX, 2, winner_colour, 5)

        cv2.putText(image, str(player_score), (145, 200),
                    cv2.FONT_HERSHEY_DUPLEX, 2, (255, 0, 0), 5)

        cv2.putText(image, str(ai_score), (500, 200),
                    cv2.FONT_HERSHEY_DUPLEX, 2, (0, 0, 255), 5)

        if player_score >= 5:
            cv2.putText(image, "Congratulations You win \n starting a new game", (150, 150),
                        cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 2)
            cv2.imshow('Rock, Paper, Scissors', image)
            cv2.waitKey(4000)  # Wait for 4 seconds
            player_score = 0
            ai_score = 0

        if ai_score >= 5:
            cv2.putText(image, "Oops, AI wins \n starting a new game", (150, 150),
                        cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)
            cv2.imshow('Rock, Paper, Scissors', image)
            cv2.waitKey(4000)  # Wait for 4 seconds
            player_score = 0
            ai_score = 0

        cv2.imshow('Rock, Paper, Scissors', image)

        if cv2.waitKey(1) & 0xFF == 27 or cv2.getWindowProperty('Rock, Paper, Scissors', cv2.WND_PROP_VISIBLE) < 1:
            break

webcam.release()
cv2.destroyAllWindows()
