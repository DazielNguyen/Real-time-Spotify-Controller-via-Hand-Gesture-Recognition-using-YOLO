# Install required libraries
import subprocess
import sys

libs = [
    "ultralytics",
    "opencv-python-headless==4.10.0.84",
    "numpy==1.26.4",
    "pandas",
    "matplotlib",
    "tqdm",
    "pyyaml",
    "torch torchvision --index-url https://download.pytorch.org/whl/cu124"
]

for lib in libs:
    subprocess.check_call([sys.executable, "-m", "pip", "install", lib, "-q"])
    
print("All libraries installed successfully!")
