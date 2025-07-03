
🖐️ Palm & Finger Controlled Virtual Mouse

Control your mouse using hand gestures detected by your webcam — no hardware needed!
This project uses MediaPipe, **OpenCV**, and **PyAutoGUI** to simulate real-time mouse actions based on finger gestures.

---

🔥 Features

| Gesture           | Action         |
| ----------------- | -------------- |
| 🟢 Index only     | Move cursor    |
| 🟡 Index + Thumb  | Left click     |
| 🔵 Index + Middle | Scroll up/down |
| 🟣 Index + Ring   | Right click    |
| 🔴 All 5 fingers  | Exit program   |


---
💡 Requirements

* Python 3.10 or 3.9 (MediaPipe doesn't support 3.11+ well)
* Webcam
* Good lighting for hand visibility

---

🧠 How It Works

* Uses MediaPipe’s hand landmark model to track finger positions in real-time.
* Maps index finger coordinates to your screen resolution.
* Detects specific gesture combinations to trigger:

  * Mouse movement
  * Left/right clicks
  * Scrolling
  * Exit on full-hand open

---


📄 License

MIT License © 2025 [Ashish Kumar](https://github.com/ashishkumar0407)
