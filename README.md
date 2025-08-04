# Hand-Gesture-VolumeControl-Project


This project allows you to control your computer’s volume using just your hand gestures via your webcam. It uses **OpenCV**, **MediaPipe**, and **pycaw** for real-time hand tracking and audio control.

---

## 📌 Features

- Real-time hand tracking using **MediaPipe**
- Gesture detection (thumb and index finger distance)
- System volume control using **pycaw**
- Live volume percentage display and bar UI
- Works with any standard webcam

---

## 🛠️ Tech Stack

- Python
- OpenCV
- MediaPipe
- NumPy
- pycaw (Python Core Audio Windows Library)

---

## 🚀 How It Works

1. Webcam captures real-time video.
2. MediaPipe detects hand landmarks.
3. Measures distance between **thumb tip (id=4)** and **index finger tip (id=8)**.
4. Maps this distance to the system volume range using **pycaw**.
5. Displays a volume bar and percentage on screen.

---

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/shreyalahane/hand-gesture-volume-control.git
   cd hand-gesture-volume-control
