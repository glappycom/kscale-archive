"""
Setup script for LeRobot Hardware Integration packages.

This script allows installing all packages in development mode.
"""

from setuptools import setup, find_packages

setup(
    name="lerobot-hardware-integration",
    version="0.1.0",
    description="LeRobot hardware integration packages",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "lerobot>=0.3.0",
        "numpy>=1.21.0",
        "opencv-python>=4.5.0",
        "pyserial>=3.5",
        "pygame>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov",
            "black",
            "isort",
            "flake8",
            "mypy",
        ],
    },
)
