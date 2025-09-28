# Hand Gesture Presentation Controller

Control slide images using your hand gestures via your webcam. Built with `cvzone` (MediaPipe Hands + OpenCV) and a simple presentation overlay.

## Features
- **Hand detection** with `cvzone.HandTrackingModule`
- **Next/Previous slide** gestures
- **Pointer** (cursor dot), **draw** on slide, and **undo** last stroke
- Live webcam overlay in the slide window

## Requirements
- Python 3.10
- Webcam
- OS: Windows (tested). Should also work on Linux/macOS with minor tweaks

## Setup
```powershell
# 1) Clone and enter the project
# git clone https://github.com/<your-username>/<your-repo>.git
cd "C:\Users\MAHESHKUMAR\OneDrive\Desktop\hand guesture"

# 2) (Recommended) Create & activate a virtual environment
py -3.10 -m venv .venv
.venv\Scripts\Activate.ps1

# 3) Install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Prepare slides
Place your slide images in the `Presentation/` folder (create it if it doesn’t exist). Supported formats: `.png`, `.jpg`, etc.

Example:
```
hand guesture/
├─ gesture_presentation.py
├─ requirements.txt
└─ Presentation/
   ├─ slide1.png
   ├─ slide2.png
   └─ slide3.png
```

## Run
```powershell
python gesture_presentation.py
```
Two windows open:
- `Slides`: your current slide with annotations and webcam overlay
- `Image`: raw webcam feed with detected landmarks

## Controls (default script)
- **Previous slide**: Thumb up only → `fingers == [1, 0, 0, 0, 0]`
- **Next slide**: Pinky up only → `fingers == [0, 0, 0, 0, 1]`
- **Pointer**: Index + middle up → `fingers == [0, 1, 1, 0, 0]` (red dot)
- **Draw**: Index up only → `fingers == [0, 1, 0, 0, 0]`
- **Undo last stroke**: Index + middle + ring up → `fingers == [0, 1, 1, 1, 0]`
- **Quit**: Press `q` in the window

A green horizontal line indicates the gesture zone near the top. Navigation (next/prev) works when the hand center is above this line to avoid accidental triggers while drawing.

## Troubleshooting
- **No images found**: Ensure you have files in `Presentation/`. Example: `slide1.png`, `slide2.png`, `slide3.png`.
- **Webcam not opening**: Your camera may be on a different index or need a Windows backend.
  - Try editing the camera line in `gesture_presentation.py`:
    ```python
    # Original
    cap = cv2.VideoCapture(0)
    # Try DirectShow backend on Windows
    # cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    # Or try different indices (1, 2, ...)
    ```
- **TensorFlow logs or oneDNN notice**: You can suppress or standardize numerics via environment variables before running:
  ```powershell
  setx TF_CPP_MIN_LOG_LEVEL 2
  setx TF_ENABLE_ONEDNN_OPTS 0
  # Then reopen your terminal
  ```
- **Dependency issues**: Use the provided `requirements.txt`. If problems persist, create a fresh venv and reinstall.

## Roadmap / Ideas
- CLI arg for camera index (e.g., `--cam 1`)
- Save/load annotations per slide
- Present mode with only the slide window visible

## Acknowledgements
- [cvzone](https://github.com/cvzone/cvzone)
- [MediaPipe](https://developers.google.com/mediapipe)
- [OpenCV](https://opencv.org/)
- [TensorFlow](https://www.tensorflow.org/)

## License
MIT — feel free to use and adapt. Replace with your preferred license if needed.
