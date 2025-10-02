# Siemens Camera Connect – Project

This project uses **OpenCV** to capture video streams and detect colors (HSV masks) in order to determine the orientation of labels on parts.  
Results are displayed in a **Tkinter GUI** and sent to a **Siemens PLC** via the **snap7** library, so that other parts of the system can grab and sort the pieces.

---

## 🔑 Main Features
- 🔎 Camera availability check (`camera_detect.py`)
- 🖼 GUI with video display, masks, and status window  
  (`kamera_senzor.py`, `camera_senzor_connect.py`, `camera_senzor_connect_v1.py`)
- 🔗 PLC connection and write operations  
  (`simens_conect.py`, `simens_connect1.py`)
- 🛠 Helper functions for PLC read/write  
  (examples in `simens_connect1.py`)

---

## 📂 File Structure
- `camera_detect.py` → test available camera indices  
- `kamera_senzor.py` → GUI only (camera + masks, no PLC)  
- `camera_senzor_connect.py` → GUI + color detection + PLC write (int values)  
- `camera_senzor_connect_v1.py` → similar to above, uses boolean write  
- `simens_conect.py` → simple PLC connection/read test  
- `simens_connect1.py` → helper functions (read/write Bool, memory)

---

## ⚙️ How It Works
1. Capture frame from camera (`cv2.VideoCapture`).  
2. Convert to HSV and create a mask for target colors (blue, red, white).  
3. Apply morphological operations and contours to detect objects and calculate centroid.  
4. Update status in GUI and send values to PLC (if configured).  

---

## 🔧 Configurable Parameters
- **PLC IP address** → hard-coded in scripts (e.g. `192.168.0.1`)  
- **DB and offsets** → `db_number`, `start_offset`, `bit_offset`  
- **Camera index** → `cv2.VideoCapture(0)` → change `0` if needed  
- **Min area** → `min_area` in `find_color` (minimum contour size)  

---

## 📋 Prerequisites
- Python **3.8+**  
- On Windows: recommended to use a virtual environment (venv or conda)  
- Dependencies listed in `requirements.txt`:  
  - `opencv-python`  
  - `numpy`  
  - `pillow`  
  - `python-snap7`  
  - `tqdm`  

---

## 🚀 Installation (PowerShell)
```powershell
# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r .\requirements.txt

## ▶️ Usage

### Quick camera test
```powershell
python .\camera_detect.py

python .\kamera_senzor.py

python .\camera_senzor_connect.py
# or
python .\camera_senzor_connect_v1.py
