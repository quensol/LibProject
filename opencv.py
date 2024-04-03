import cv2
import numpy as np
from pyzbar.pyzbar import decode

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, 640)
cap.set(4, 480)

while True:
    success, frame = cap.read()
    if success:
        for code in decode(frame):
            data = code.data.decode('utf-8')

            pts = np.array([code.polygon], np.int32)
            print(pts)
            pts = pts.reshape((-1, 1, 2))

            cv2.polylines(frame, [pts], True, (0, 255, 0), 5)

            code_box = code.rect
            cv2.putText(frame, data, (code_box[0], code_box[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
        cv2.imshow('result', frame)
        key = cv2.waitKey(1)
        if key == 27 or cv2.getWindowProperty('result', cv2.WND_PROP_VISIBLE) < 1.0:
            break
cap.release()
cv2.destroyAllWindows()
