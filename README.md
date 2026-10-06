# Face Recognition Attendance System

An automated, contactless attendance marking system built with Python, OpenCV, and Deep Learning (dlib face embeddings). It recognizes registered faces in real time through a live webcam stream, logs attendance timestamps directly into a CSV file, and provides instant audio confirmation with text-to-speech.

---

## 📌 Overview

Traditional manual attendance systems are prone to proxy attendance and time delays. This project provides a computer vision-driven desktop solution featuring:
- **Graphical User Interface (GUI)** for user-friendly face registration and system control.
- **Deep Metric Learning & Embeddings** (128-d feature vectors via ResNet architecture) for accurate facial recognition.
- **Real-Time Video Analytics** with face tracking, coordinate scaling, and visual feedback.
- **Automated Logging** to timestamp attendance without manual intervention.
- **Audio Feedback** through integrated Text-to-Speech (TTS).

---

## ✨ Features

- **Quick Registration**: Enter a user's ID and Name, then capture reference images using the webcam.
- **High-Accuracy Recognition**: Identifies registered faces and labels them with an active bounding box in green.
- **Unknown Face Detection**: Flags unregistered or low-confidence faces with a red bounding box and "Unknown" label.
- **Smart Duplicate Prevention**: Logs each attendee only once per session to avoid duplicate CSV entries.
- **Voice Confirmation**: Welcomes recognized individuals by name using synthesized audio speech (`pyttsx3`).
- **CSV Data Persistence**: Records date and time stamps in `Attendence.csv` for easy export to Excel or Google Sheets.

---

## 🛠️ Tech Stack & Dependencies

- **Language**: Python 3.7+ (tested up to Python 3.13)
- **Computer Vision**: OpenCV (`cv2`)
- **Face Recognition**: `face_recognition` (powered by `dlib`)
- **Mathematical Processing**: NumPy
- **Text-to-Speech**: `pyttsx3`
- **GUI**: Tkinter

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/chandiallaka/Face-Recognition-Attendance-System.git
cd Face-Recognition-Attendance-System
```

### 2. Install Required Packages
```bash
pip install -r requirements.txt
```

> **Note for Windows Users:**  
> The underlying `dlib` library requires C++ compilation tools. If you run into build errors, ensure you have:
> - [CMake](https://cmake.org/download/) installed and added to your system PATH.
> - [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) with the "Desktop development with C++" workload installed.

---

## 📂 Project Structure

```
Face-Recognition-Attendance-System/
├── Mian.py                              # Main Tkinter GUI application
├── recognize.py                         # Core face recognition and attendance engine
├── Attendence/                          # Directory containing registered face images
│   └── <id>_<name>_<counter>.jpg
├── Attendence.csv                       # Auto-generated attendance log file
├── requirements.txt                     # Python package dependencies
├── README.md                            # Project documentation
└── *.dat                                # Pre-trained dlib landmark and recognition models
```

---

## 🚀 How to Run

### Step 1: Launch the Application
Run the graphical interface:
```bash
python Mian.py
```

### Step 2: Register a New Face
1. Enter the student/employee **ID** (e.g., `013`) and **Name** (e.g., `Chandi`).
2. Click **Capture**.
3. A live camera feed will appear:
   - Press **SPACE** to take photos (capture multiple angles for improved recognition).
   - Press **ESC** to finish capturing and return to the main menu.

### Step 3: Start Attendance Tracking
1. In the main menu, click **Recognize** (or execute `python recognize.py` directly).
2. Look directly into the webcam:
   - **Registered Face**: Outlined in **green**, name displayed, voice prompt announces attendance, and a record is saved to `Attendence.csv`.
   - **Unrecognized Face**: Outlined in **red** with an "Unknown" tag.
3. Press **ESC** at any time to stop the session.

---

## 📊 Attendance Log Output

Attendance entries are recorded inside `Attendence.csv` with the following structure:

```csv
Name, Time
013_CHANDI, 10:45:00
031_SIVA, 10:46:12
```

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page or submit a Pull Request.

---

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).
