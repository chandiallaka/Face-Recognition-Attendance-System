# Face Recognition Attendance System

A Python-based attendance system that uses facial recognition via webcam to automatically mark attendance.

## Features
- Capture face images for new students/employees
- Recognize registered faces via webcam
- Automatically mark attendance in a CSV file
- Text-to-speech confirmation when attendance is marked
- Unknown face detection (shown with red bounding box)

## Requirements

- Python 3.7+
- A webcam

### Install Dependencies

```bash
pip install -r requirements.txt
```

> **Note:** `face_recognition` requires `dlib` which in turn may require CMake and a C++ compiler.  
> On Windows, install CMake from https://cmake.org and Visual Studio Build Tools before running the above command.

## Project Structure

```
Face-Recognition-Attendance-System/
├── Mian.py                              # Main UI (Tkinter)
├── recognize.py                         # Face recognition logic
├── Attendence/                          # Folder of registered face images
│   └── <id>_<name>_<n>.jpg
├── Attendence.csv                       # Auto-generated attendance log
├── requirements.txt
└── *.dat                                # dlib model files (pre-included)
```

## How to Use

### Step 1 — Register a Face

1. Run the main UI:
   ```bash
   python Mian.py
   ```
2. Enter an **ID** and **Name** in the fields.
3. Click **Capture**.
4. A webcam window opens — press **SPACE** to take a photo, **ESC** to close.
5. Photos are saved in the `Attendence/` folder.

> Tip: Take multiple photos (different angles/lighting) for better accuracy.

### Step 2 — Mark Attendance

1. In the main UI, click **Recognize**.
2. A webcam window opens and begins scanning for faces.
3. Recognized faces get a **green** box and name label; their attendance is recorded in `Attendence.csv`.
4. Unrecognized faces get a **red** box labeled "Unknown".
5. Press **ESC** to end the session.

## Attendance Log

`Attendence.csv` is updated automatically. Format:
```
Name, Time
013_CHANDI, 10:45:00
031_SIVA, 10:46:12
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Camera not opening | Make sure webcam is connected; try changing `cv2.VideoCapture(0)` to `cv2.VideoCapture(1)` |
| `No face found in image` warning | Re-capture the face image in better lighting |
| `dlib` install fails | Install CMake + Visual Studio Build Tools on Windows |
| Face not recognized | Capture more training photos with varied angles |
