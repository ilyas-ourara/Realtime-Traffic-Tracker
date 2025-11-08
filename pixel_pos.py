import cv2
import matplotlib.pyplot as plt

# Lire vidéo et frame comme avant
cap = cv2.VideoCapture("input/2.mp4")
ret, frame = cap.read()
cap.release()
resized_frame = cv2.resize(frame, (640, 640))

# Afficher avec matplotlib
plt.imshow(cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB))
plt.title("Cliquez sur la frame pour obtenir la position du pixel")

def onclick(event):
    x, y = int(event.xdata), int(event.ydata)
    print(f"Position du pixel : x={x}, y={y}")
    print("Valeur du pixel (BGR):", resized_frame[y, x])

plt.connect('button_press_event', onclick)
plt.show()
