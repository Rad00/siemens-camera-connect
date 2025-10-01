import cv2
import numpy as np
import tkinter as tk
from tkinter import Label, Frame, Text, Scrollbar
from PIL import Image, ImageTk
from datetime import datetime
import snap7
from tqdm import tqdm
import time

# PLC configuration
plc = snap7.client.Client()

# Progress bar for initialization
for i in tqdm(range(100), desc="Initializing program"):
    time.sleep(0.01)  # Simulate loading delay

plc.connect('192.168.0.1', 0, 1)  # IP address, rack, slot

db_number = 1
start_offset = 0
bit_offset = 0

# PLC write function
def writeBool(db_number, start_offset, bit_offset, value):
    reading = plc.db_read(db_number, start_offset, 1)
    snap7.util.set_bool(reading, 0, bit_offset, value)
    plc.db_write(db_number, start_offset, reading)

# Camera color detection
cap = cv2.VideoCapture(0)  # First camera


def find_color(frame, lower_bound, upper_bound, min_area=500):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > min_area:
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                return True, (cx, cy), mask
    return False, None, mask

def update_frame():
    ret, frame = cap.read()


    # Define HSV bounds for colors
    blue_lower = np.array([100, 150, 0])
    blue_upper = np.array([140, 255, 255])
    red_lower = np.array([0, 120, 70])
    red_upper = np.array([10, 255, 255])

    # Detect colors
    blue_detected, _, blue_mask = find_color(frame, blue_lower, blue_upper)
    red_detected, _, red_mask = find_color(frame, red_lower, red_upper)

    # Combine masks for color view
    combined_mask = cv2.bitwise_or(blue_mask, red_mask)
    color_view = cv2.cvtColor(combined_mask, cv2.COLOR_GRAY2RGB)

    # Determine orientation and send data to PLC
    if blue_detected:
        orientation = "Correct orientation (blue label)"
        orientation_color = "green"
        writeBool(db_number, 0, 0, True)  # Send 1 to PLC
        writeBool(db_number, 0, 1, False)
    elif red_detected:
        orientation = "Incorrect orientation (red label)"
        orientation_color = "red"
        writeBool(db_number, 0, 1, True)  # Send 0 to PLC
        writeBool(db_number, 0, 0, False)
    else:
        orientation = "Object not detected"
        orientation_color = "orange"
        writeBool(db_number, 0, 0, False)  # Send 0 to PLC
        writeBool(db_number, 0, 1, False)  # Send 0 to PLC

    # Update GUI
    current_time = datetime.now().strftime("%H:%M:%S")
    append_status(f"[{current_time}] {orientation}")

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame_rgb).resize((400, 300))
    imgtk = ImageTk.PhotoImage(image=img)
    video_label.imgtk = imgtk
    video_label.configure(image=imgtk)

    color_view_resized = cv2.resize(color_view, (400, 300))
    img2 = Image.fromarray(color_view_resized)
    imgtk2 = ImageTk.PhotoImage(image=img2)
    video_label2.imgtk = imgtk2
    video_label2.configure(image=imgtk2)

    status_label.config(text="Status: Program running", fg="green")
    orientation_label.config(text=f"Orientation: {orientation}", fg=orientation_color)

    video_label.after(10, update_frame)

def append_status(message):
    status_text.config(state="normal")
    status_text.insert("end", f"{message}\n")
    status_text.config(state="disabled")
    status_text.see("end")

# Tkinter GUI setup
root = tk.Tk()
root.title("Label Detection - Orientation")
root.geometry("1200x800")

left_frame = Frame(root, width=300, height=600, bg="lightgrey")
left_frame.pack(side="left", fill="both")

status_label = Label(left_frame, text="Status: Initializing...", font=("Helvetica", 16), bg="lightgrey")
status_label.pack(pady=20, padx=10, fill="x")

orientation_label = Label(left_frame, text="Orientation: ", font=("Helvetica", 16), bg="lightgrey")
orientation_label.pack(pady=20, padx=10, fill="x")

status_text = Text(left_frame, wrap="word", state="disabled", bg="white", height=15, font=("Helvetica", 12))
status_text.pack(pady=10, padx=10, fill="both", expand=True)

scrollbar = Scrollbar(status_text)
scrollbar.pack(side="right", fill="y")
status_text.config(yscrollcommand=scrollbar.set)

right_frame = Frame(root, width=500, height=600, bg="white")
right_frame.pack(side="right", fill="both", expand=True)

video_label = Label(right_frame, bg="black", width=400, height=300)
video_label.pack(side="top", pady=10)

video_label2 = Label(right_frame, bg="black", width=400, height=300)
video_label2.pack(side="bottom", pady=10)

update_frame()
root.mainloop()

cap.release()
plc.disconnect()
cv2.destroyAllWindows()
