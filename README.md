# Rock-Paper-Scissors-Game
This repository contains a Python-based Rock, Paper, Scissors game that utilizes OpenCV for video capture and MediaPipe for hand landmark detection. The game allows users to play Rock, Paper, Scissors against an AI that makes random choices. The AI and player's scores are displayed, and the game announces the winner after either party reaches a score of 5.


# Features:
Hand Detection and Tracking: Utilizes MediaPipe's hand tracking module to detect and track hand landmarks.
Gesture Recognition: Recognizes player's gesture (Rock, Paper, Scissors) based on the number of extended fingers.
AI Opponent: The AI opponent randomly selects between Rock, Paper, and Scissors.
Scoring System: Keeps track of the scores for both the player and AI. The game declares the winner once a score of 5 is reached.
Real-time Feedback: Displays the player's and AI's choices, the winner of each round, and the current scores on the screen in real-time.


# How It Works:
Video Capture: The script captures video from the default webcam.
Hand Landmark Detection: MediaPipe processes each frame to detect hand landmarks.
Gesture Recognition: The number of extended fingers is counted to determine the player's gesture:
Rock: 0 or 1 fingers
Scissors: 2 fingers
Paper: 5 fingers
Invalid: Other numbers of fingers
Game Logic: The player's gesture is compared against the AI's random choice to determine the winner of the round. The scores are updated accordingly.
Display: The current round's winner, choices, and scores are displayed on the video feed.
Game End: The game announces the winner and restarts when either the player or AI reaches a score of 5.


# Prerequisites:
Python 3.x
OpenCV
MediaPipe
statistics module
