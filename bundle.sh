#!/bin/bash

# Activate conda environment
conda activate gopro

# Run PyInstaller from within the conda environment
pyinstaller --onefile --windowed --additional-hooks-dir=./hooks GoProTransporter.py 

# Deactivate the conda environment
conda deactivate