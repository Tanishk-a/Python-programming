
############################################# IMPORTING ################################################
import tkinter as tk
from tkinter import messagebox as mess
import os, csv, datetime

import importlib
try:
    cv2 = importlib.import_module("cv2")
except Exception:
    print("Error: OpenCV (cv2) is not installed. Install it using: pip install opencv-python")
    cv2 = None

############################################# PATHS ################################################
def assure_path_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

assure_path_exists("StudentDetails/")
assure_path_exists("TrainingImage/")

# Determine cascade path; fall back to packaged cascade if available
if cv2:
    try:
        haarcasecade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    except Exception:
        haarcasecade_path = "haarcascade_frontalface_default.xml"
else:
    haarcasecade_path = "haarcascade_frontalface_default.xml"
studentdetail_path = "StudentDetails/StudentDetails.csv"

############################################# FUNCTIONS ################################################
def update_total_count(label):
    if os.path.isfile(studentdetail_path):
        with open(studentdetail_path, "r") as f:
            total = sum(1 for line in f) - 1
    else:
        total = 0
    label.config(text=f"Total Registered People: {total}")

def update_time():
    now = datetime.datetime.now()
    lbl_date.config(text=now.strftime("%Y-%m-%d"))
    lbl_time.config(text=now.strftime("%H:%M:%S"))
    window.after(1000, update_time)

def RegisterStudent():
    if cv2 is None:
        mess.showerror("Missing Dependency", "OpenCV (cv2) is not installed. Install it using: pip install opencv-python")
        return
    Id = txt_id.get().strip()
    name = txt_name.get().strip()

    if Id == "" or name == "":
        mess.showinfo("Input Error", "Please enter both ID and Name.")
        return

    # Create CSV if not exists
    if not os.path.isfile(studentdetail_path):
        with open(studentdetail_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Id","Name","Date","Time"])

    # Current date/time
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    timeStamp = now.strftime("%H:%M:%S")

    # Open camera
    cam = cv2.VideoCapture(0)
    detector = cv2.CascadeClassifier(haarcasecade_path)
    captured = False

    while not captured:
        ret, img = cam.read()
        if not ret:
            break
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            # Draw blue rectangle
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(img, f"{name} ID:{Id}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0),2)
            # Save single image
            cv2.imwrite(f"TrainingImage/{name}.{Id}.jpg", gray[y:y+h, x:x+w])
            captured = True
        cv2.imshow("Attendance Capture", img)
        cv2.waitKey(1)

    cam.release()
    cv2.destroyAllWindows()

    # Save details in CSV immediately after capture
    with open(studentdetail_path, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([Id, name, date, timeStamp])

    mess.showinfo("Success", f"Registered {name} (ID: {Id})\nDate: {date} | Time: {timeStamp}")
    update_total_count(totalLbl)
    txt_id.delete(0, tk.END)
    txt_name.delete(0, tk.END)

############################################# GUI ################################################
window = tk.Tk()
window.title("Face Registration Attendance System")
window.geometry("700x550")
window.configure(bg="#1f1f2e")

# Title
title = tk.Label(window, text="FACE REGISTRATION ATTENDANCE SYSTEM", bg="#222", fg="white", width=50, height=2, font=('Times', 18, 'bold'))
title.place(x=10, y=10)

# Live Date & Time Labels
lbl_date_title = tk.Label(window, text="Date:", bg="#1f1f2e", fg="white", font=('Times', 14, 'bold'))
lbl_date_title.place(x=70, y=70)
lbl_date = tk.Label(window, text="", bg="#1f1f2e", fg="#00b894", font=('Times', 14, 'bold'))
lbl_date.place(x=130, y=70)

lbl_time_title = tk.Label(window, text="Time:", bg="#1f1f2e", fg="white", font=('Times', 14, 'bold'))
lbl_time_title.place(x=400, y=70)
lbl_time = tk.Label(window, text="", bg="#1f1f2e", fg="#00b894", font=('Times', 14, 'bold'))
lbl_time.place(x=460, y=70)

update_time()  # Start live clock

# ID & Name input
lbl_id = tk.Label(window,text="Enter ID",width=10,height=2,bg="#333",fg="white",font=('Times',15,'bold'))
lbl_id.place(x=70,y=120)
txt_id = tk.Entry(window,width=20,fg="black",font=('Times',15,'bold'))
txt_id.place(x=230,y=130)

lbl_name = tk.Label(window,text="Enter Name",width=10,height=2,bg="#333",fg="white",font=('Times',15,'bold'))
lbl_name.place(x=70,y=200)
txt_name = tk.Entry(window,width=20,fg="black",font=('Times',15,'bold'))
txt_name.place(x=230,y=210)

# Total registered
totalLbl = tk.Label(window,text="",bg="#1f1f2e",fg="#f39c12",font=('Times',14,'bold'))
totalLbl.place(x=230,y=260)
update_total_count(totalLbl)

# Buttons
btn_register = tk.Button(window,text="Attendance",command=RegisterStudent,bg="#00b894",fg="white",width=20,height=2,font=('Times',15,'bold'))
btn_register.place(x=230,y=320)

btn_quit = tk.Button(window,text="Quit",command=window.destroy,bg="#d63031",fg="white",width=20,height=2,font=('Times',15,'bold'))
btn_quit.place(x=230,y=400)

window.mainloop()
