from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="real-time-spotify-controller",
    version="1.0.0",
    author="Nguyen Van Anh Duy",
    author_email="duynvse181823@fpt.edu.vn",
    description="Real-time Spotify controller via hand gesture recognition using YOLOv8",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/real-time-spotify-controller",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Scientific/Engineering :: Image Recognition",
    ],
    python_requires=">=3.8",
    install_requires=[
        "ultralytics>=8.0.0",
        "opencv-python>=4.8.0",
        "torch>=2.0.0",
        "torchvision>=0.15.0",
        "pandas>=1.5.0",
        "matplotlib>=3.7.0",
        "seaborn>=0.12.0",
        "numpy>=1.23.0",
        "Pillow>=9.5.0",
        "tqdm>=4.65.0",
        "PyYAML>=6.0",
    ],
    entry_points={
        "console_scripts": [
            "gesture-control=src.hand_tracking:main",
        ],
    },
)
