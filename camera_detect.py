import cv2

for i in range(10):  # Preveri prvih 10 indeksov kamer
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f"Kamera z indeksom {i} je dostopna.")
        ret, frame = cap.read()
        if ret:
            cv2.imshow(f"Kamera {i}", frame)
            cv2.waitKey(1000)  # Prikaži sliko za 1 sekundo
            cv2.destroyAllWindows()
        cap.release()
    else:
        print(f"Kamera z indeksom {i} ni dostopna.")
