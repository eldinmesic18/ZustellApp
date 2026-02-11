#!/bin/bash

echo "========================================"
echo "ZustellApp - Setup Script"
echo "========================================"
echo ""

echo "[1/4] Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "Error creating virtual environment!"
    exit 1
fi

echo "[2/4] Activating virtual environment..."
source venv/bin/activate

echo "[3/4] Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error installing dependencies!"
    exit 1
fi

echo "[4/4] Installing MapView..."
garden install mapview
if [ $? -ne 0 ]; then
    echo "Warning: MapView installation failed. You may need to install it manually."
fi

echo ""
echo "========================================"
echo "Setup complete!"
echo "========================================"
echo ""
echo "To create demo data, run:"
echo "  source venv/bin/activate"
echo "  cd ZustellApp"
echo "  python create_demo_data.py"
echo ""
echo "To start the app, run:"
echo "  source venv/bin/activate"
echo "  cd ZustellApp"
echo "  python main.py"
echo ""
