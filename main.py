import cv2
import serial
import time
import random
import numpy as np
import math
cam_url = "url_stream"
esp_port = 'port_esp' 
baud_rate = 115200

use_real_radar = False
try:
    ser = serial.Serial(esp_port, baud_rate, timeout=0.05)
    print(">> [RADAR] Đã kết nối DevKit V1!")
    use_real_radar = True
except:
    print(">> [RADAR] Chạy giả lập sóng!")

cap = cv2.VideoCapture(cam_url)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

print(">> HỆ THỐNG TARGET LOCK ĐÃ KÍCH HOẠT! Bấm 'q' để tắt.")


ar_targets = {}

def draw_lock_on_bracket(img, x, y, size, color, thickness=2):
    L = int(size * 0.3)
    cv2.line(img, (x - size, y - size), (x - size + L, y - size), color, thickness)
    cv2.line(img, (x - size, y - size), (x - size, y - size + L), color, thickness)
    cv2.line(img, (x + size, y - size), (x + size - L, y - size), color, thickness)
    cv2.line(img, (x + size, y - size), (x + size, y - size + L), color, thickness)
    cv2.line(img, (x - size, y + size), (x - size + L, y + size), color, thickness)
    cv2.line(img, (x - size, y + size), (x - size, y + size - L), color, thickness)
    cv2.line(img, (x + size, y + size), (x + size - L, y + size), color, thickness)
    cv2.line(img, (x + size, y + size), (x + size, y + size - L), color, thickness)

time_step = 0

while True:
    ret, frame = cap.read()
    if not ret:
        time.sleep(1)
        cap = cv2.VideoCapture(cam_url)
        continue
        
    frame = cv2.resize(frame, (1280, 720))
    h, w = frame.shape[:2]
    time_step += 1

    current_time = time.time()
    
    if use_real_radar:
        while ser.in_waiting > 0:
            try:
                line = ser.readline().decode('utf-8').strip()
                if "Muc tieu" in line and "RSSI):" in line:
                    parts = line.split("|")
                    name = parts[0].replace("Muc tieu", "").strip()
                    rssi = int(parts[1].split("RSSI):")[1].replace("dBm", "").strip())
                    
                    if name not in ar_targets:
                        ar_targets[name] = [random.randint(200, w-200), random.randint(150, h-150), rssi, current_time]
                    else:
                        ar_targets[name][2] = rssi
                        ar_targets[name][3] = current_time
            except: pass
    else:
        if time_step % 10 == 0:
            for n in ["Hidden_5G", "Cyber_Router", "Neighbor_Net"]:
                rssi = random.randint(-90, -40)
                if n not in ar_targets:
                    ar_targets[n] = [random.randint(200, w-200), random.randint(150, h-150), rssi, current_time]
                else:
                    ar_targets[n][2] = rssi
                    ar_targets[n][3] = current_time

    ar_targets = {k: v for k, v in ar_targets.items() if current_time - v[3] < 5.0}

    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (w, h), (15, 25, 10), -1)
    frame = cv2.addWeighted(overlay, 0.2, frame, 0.8, 0)

    center_x, center_y = w // 2, h

    for name, data in ar_targets.items():
        tx, ty, rssi, _ = data
        
        tx += int(math.sin(time_step * 0.05 + ty) * 2)
        ty += int(math.cos(time_step * 0.05 + tx) * 2)
        ar_targets[name][0], ar_targets[name][1] = tx, ty
        
        size = int(np.interp(rssi, [-95, -30], [20, 150]))
        
        if rssi > -50:
            color = (0, 0, 255) 
            thickness = 3
            cv2.line(frame, (center_x, center_y), (tx, ty + size), (0, 0, 150), 2, cv2.LINE_AA)
            cv2.putText(frame, "LOCKED", (tx - 40, ty + size + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        elif rssi > -70:
            color = (0, 200, 255) 
            thickness = 2
        else:
            color = (0, 255, 0) 
            thickness = 1
            
        draw_lock_on_bracket(frame, tx, ty, size, color, thickness)
        
        cv2.putText(frame, f"{name[:10]}", (tx - size, ty - size - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        cv2.putText(frame, f"[{rssi} dBm]", (tx + 10, ty - size - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

    cv2.imshow("Terminator Vision HUD", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
if use_real_radar: ser.close()
cv2.destroyAllWindows()
