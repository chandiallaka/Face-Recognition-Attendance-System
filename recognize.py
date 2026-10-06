import cv2
import face_recognition
import numpy as np
import os
from datetime import datetime
import pyttsx3

# FIX #8: Initialize pyttsx3 ONCE at the top, not inside the loop
engine = pyttsx3.init()

path = 'Attendence'  # Path of stored face images
Images = []
ImageNames = []

# FIX #4 (partial): Only process valid image files, skip others like .DS_Store
VALID_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.bmp')
MyList = [f for f in os.listdir(path) if f.lower().endswith(VALID_EXTENSIONS)]

encodeList_saved = []

# Loading & Reading Images
for cls in MyList:
    curImg = face_recognition.load_image_file(f'{path}/{cls}')
    Images.append(curImg)
    ImageNames.append(os.path.splitext(cls)[0])

print("Loaded images:", ImageNames)


# Encoding of Images
def findEncodings(Images):
    for idx, img in enumerate(Images):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(img)
        # FIX #4: Skip image if no face was detected (prevents IndexError crash)
        if len(encodings) == 0:
            print(f"WARNING: No face found in image '{ImageNames[idx]}'. Skipping.")
            encodeList_saved.append(None)
        else:
            encodeList_saved.append(encodings[0])
    return encodeList_saved


# FIX #9 (typo fix): Renamed markAttendence → markAttendance
def markAttendance(name):
    with open('Attendence.csv', 'a+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0].strip())
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')
            print(f"Attendance marked for: {name} at {dtString}")


encodeListKnown = findEncodings(Images)
# Remove None entries (images where no face was detected)
valid_pairs = [(enc, name) for enc, name in zip(encodeListKnown, ImageNames) if enc is not None]

if len(valid_pairs) == 0:
    print("ERROR: No valid face encodings found in the Attendence folder. Please add face images first.")
    exit()

encodeListKnown, ImageNames = zip(*valid_pairs)
encodeListKnown = list(encodeListKnown)
ImageNames = list(ImageNames)

print(f"Encoding complete. {len(encodeListKnown)} faces loaded.")

cap = cv2.VideoCapture(0)  # FIX #5: Use camera index 0 (default camera)

if not cap.isOpened():
    print("ERROR: Could not open camera.")
    exit()

# Track which people have already had attendance marked this session
markedlist = set()

while True:
    success, img = cap.read()
    if not success:
        print("Failed to read from camera.")
        break

    # FIX #1 & #2: Correctly resize and convert the SAME variable (imgs)
    imgs = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgs = cv2.cvtColor(imgs, cv2.COLOR_BGR2RGB)  # FIX: was cv2.cvtColor(img, ...) — wrong variable

    faceCurFrame = face_recognition.face_locations(imgs)
    encodeCurFrame = face_recognition.face_encodings(imgs, faceCurFrame)

    for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

        matchIndex = np.argmin(faceDis)

        if matches[matchIndex] and faceDis[matchIndex] <= 0.5:
            name = ImageNames[matchIndex].upper()

            # FIX #2: Scale face location coordinates back up (×4) to match full-res frame
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4

            # Draw bounding box and name label
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

            # FIX #3: Simplified and fixed attendance marking logic (removed broken nested loop)
            if name not in markedlist:
                markedlist.add(name)
                markAttendance(name)
                # FIX #8: Use the pre-initialized engine; FIX typo "your" → " your"
                engine.say(name + " your attendance is marked")
                engine.runAndWait()
        else:
            # Unknown face — draw red box
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 0, 255), cv2.FILLED)
            cv2.putText(img, "Unknown", (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow('Face Recognition - Press ESC to quit', img)

    k = cv2.waitKey(1)
    if k % 256 == 27:
        print("Escape hit, closing...")
        break

cap.release()
cv2.destroyAllWindows()
print("Session ended. Marked attendance for:", list(markedlist))