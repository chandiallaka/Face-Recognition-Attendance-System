from tkinter import *
from tkinter import messagebox
import os
import sys
import cv2

py = sys.executable

# creating window
class mainpg(Tk):
    def __init__(self):
        super().__init__()
        self.a = StringVar()
        self.b = StringVar()
        self.maxsize(1600, 700)
        self.minsize(1600, 700)
        self.configure(bg="gray")
        self.title("Face_Recogniser")

        # verifying input
        def takeimage():
            # FIX #1: Use 'or' so warning shows if EITHER field is empty
            if len(self.id_text.get()) <= 0 or len(self.name_text.get()) <= 0:
                messagebox.showinfo("Error", "Please enter both ID and Name fields properly.")
            else:
                id = self.id_text.get()
                name = self.name_text.get()
                # FIX #2: Use camera index 0 (default camera on most systems)
                cam = cv2.VideoCapture(0)
                if not cam.isOpened():
                    messagebox.showerror("Camera Error", "Could not open camera. Please check your webcam connection.")
                    return
                path = 'Attendence'
                os.makedirs(path, exist_ok=True)  # Ensure the folder exists
                cv2.namedWindow("Capture Face - Press SPACE to capture, ESC to quit")
                img_counter = 0
                while True:
                    ret, frame = cam.read()
                    if not ret:
                        messagebox.showerror("Camera Error", "Failed to read from camera.")
                        break
                    cv2.imshow("Capture Face - Press SPACE to capture, ESC to quit", frame)
                    k = cv2.waitKey(1)
                    if k % 256 == 27:
                        # ESC pressed
                        print("Escape hit, closing...")
                        break
                    elif k % 256 == 32:
                        # SPACE pressed — FIX #3: include img_counter in filename so captures don't overwrite
                        img_name = "{}_{}_{}.jpg".format(id, name, img_counter)
                        cv2.imwrite(os.path.join(path, img_name), frame)
                        print("{} written!".format(img_name))
                        img_counter += 1
                        messagebox.showinfo("Captured", f"Image {img_counter} captured successfully!")
                cam.release()
                cv2.destroyAllWindows()

        def recognise():
            os.system("python recognize.py")

        def check():
            self.mainlabel = Label(self, text="Face-Recognition-System",
                                   bg="black", fg="white", width=50,
                                   height=3, font=('cilia', '10', 'bold'))
            self.mainlabel.place(x=200, y=20)

            self.label1 = Label(self, text="Id :",
                                width=20, height=2, fg="cornflower blue",
                                bg="black", font=('times', 15, ' bold '))
            self.label1.place(x=400, y=200)
            self.id_text = Entry(self, width=20, bg="black", fg="cornflower blue", font=('times', 15, ' bold '))
            self.id_text.place(x=700, y=215)

            self.label2 = Label(self, text="Name :",
                                width=20, fg="cornflower blue", bg="black",
                                height=2, font=('times', 15, ' bold '))
            self.label2.place(x=400, y=300)
            self.name_text = Entry(self, width=20, bg="black", fg="cornflower blue", font=('times', 15, ' bold '))
            self.name_text.place(x=700, y=315)

            self.btn1 = Button(self, text="Capture", command=takeimage, fg="black", bg="cornflower blue",
                               width=20, height=3, activebackground="Red", font=('times', 15, ' bold '))
            self.btn1.place(x=200, y=500)

            self.btn2 = Button(self, text="Recognize", command=recognise, fg="black", bg="cornflower blue",
                               width=20, height=3, activebackground="Red", font=('times', 15, ' bold '))
            self.btn2.place(x=700, y=500)

            self.btn3 = Button(self, text="Quit", command=self.destroy, fg="black", bg="cornflower blue",
                               width=20, height=3, activebackground="Red", font=('times', 15, ' bold '))
            self.btn3.place(x=1100, y=500)

        check()

mainpg().mainloop()
