import cv2
import numpy as np
import tkinter as tk
from tkinter import Label, Frame, Text, Scrollbar
from PIL import Image, ImageTk
from datetime import datetime

# Funkcija za zaznavanje barv in vračanje težišča
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

# Funkcija za posodabljanje Tkinter vmesnika
def update_frame():
    ret, frame = cap.read()
    if not ret:
        status_label.config(text="Status: Napaka pri zajemu kamere", fg="red", anchor="w")
        append_status("Napaka pri zajemu kamere")
        return

    # Določi HSV meje za modro, rdečo in belo barvo
    blue_lower = np.array([100, 150, 0])
    blue_upper = np.array([140, 255, 255])
    red_lower = np.array([0, 120, 70])
    red_upper = np.array([10, 255, 255])
    white_lower = np.array([0, 0, 200])
    white_upper = np.array([180, 55, 255])

    # Preveri barve
    blue_detected, blue_center, blue_mask = find_color(frame, blue_lower, blue_upper)
    red_detected, red_center, red_mask = find_color(frame, red_lower, red_upper)
    white_detected, white_center, white_mask = find_color(frame, white_lower, white_upper)

    # Določi orientacijo
    if blue_detected:
        orientation = "Kos je pravilno obrnjen (modra nalepka)"
        orientation_color = "green"
    elif red_detected:
        orientation = "Kos ni pravilno obrnjen (rdeča nalepka)"
        orientation_color = "red"
    elif white_detected or not (blue_detected or red_detected):
        orientation = "Kos ni zaznan"
        orientation_color = "orange"

    # Dodaj čas in status
    current_time = datetime.now().strftime("%H:%M:%S")
    append_status(f"[{current_time}] {orientation}")

    # Prikaz video toka
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame_rgb).resize((400, 300))  # Prilagodi velikost
    imgtk = ImageTk.PhotoImage(image=img)
    video_label.imgtk = imgtk
    video_label.configure(image=imgtk)

    # Prikaz maske
    if blue_detected:
        mask = blue_mask
    elif red_detected:
        mask = red_mask
    else:
        mask = white_mask
    mask_img = Image.fromarray(mask).convert("RGB").resize((400, 300))  # Prilagodi velikost
    mask_imgtk = ImageTk.PhotoImage(image=mask_img)
    mask_label.imgtk = mask_imgtk
    mask_label.configure(image=mask_imgtk)

    # Posodobi status
    status_label.config(text=f"Status: Program deluje", fg="green", anchor="w")
    orientation_label.config(text=f"Orientacija: {orientation}", fg=orientation_color, anchor="w")

    # Nadaljuj posodabljanje
    video_label.after(10, update_frame)

# Funkcija za dodajanje statusnih sporočil
def append_status(message):
    status_text.config(state="normal")  # Omogoči urejanje
    status_text.insert("end", f"{message}\n")
    status_text.config(state="disabled")  # Zakleni urejanje
    status_text.see("end")  # Samodejno pomakni na konec

# Tkinter uporabniški vmesnik
root = tk.Tk()
root.title("Zaznavanje nalepk - Kos Orientacija")
root.geometry("1000x600")

# Levi okvir za status
left_frame = Frame(root, width=300, height=600, bg="lightgrey")
left_frame.pack(side="left", fill="both", expand=False)

status_label = Label(left_frame, text="Status: Priprava...", font=("Helvetica", 16), bg="lightgrey", fg="black", anchor="w")
status_label.pack(pady=20, padx=10, fill="x")

orientation_label = Label(left_frame, text="Orientacija: ", font=("Helvetica", 16), bg="lightgrey", fg="black", anchor="w")
orientation_label.pack(pady=20, padx=10, fill="x")

# Statusno okno
status_text = Text(left_frame, wrap="word", state="disabled", bg="white", fg="black", height=15, font=("Helvetica", 12))
status_text.pack(pady=10, padx=10, fill="both", expand=True)

scrollbar = Scrollbar(status_text)
scrollbar.pack(side="right", fill="y")
status_text.config(yscrollcommand=scrollbar.set)

# Desni okvir za video in masko
right_frame = Frame(root, width=500, height=600, bg="white")
right_frame.pack(side="right", fill="both", expand=True)

# Video in maska v desnem okvirju
video_label = Label(right_frame, bg="black", width=400, height=300)
video_label.pack(side="top", pady=10)

mask_label = Label(right_frame, bg="black", width=400, height=300)
mask_label.pack(side="bottom", pady=10)


# Zagon kamere
cap = cv2.VideoCapture(0) #Uporabi zunanjo kamero
if not cap.isOpened():
    status_label.config(text="Status: Kamera ni odprta", fg="red")
    append_status("Kamera ni odprta")
    root.destroy()

# Začni posodabljanje
update_frame()

# Zagon GUI
root.mainloop()

# Sprostitev kamere
cap.release()
cv2.destroyAllWindows()
