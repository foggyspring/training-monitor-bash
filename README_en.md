# Training Process Monitor (Bash Command Version)

This project is a visual tool for launching and monitoring training processes via Bash commands entered on a web page. The frontend is based on Vue, and the backend uses Flask + Flask-SocketIO for real-time log streaming.

## Features
- Enter any Bash training command on the web page (e.g., `python train.py --epochs 5`)
- View real-time training logs and progress
- Support for stopping and deleting training processes
- Multi-process management

## Directory Structure
```
├── app.py                # Backend Flask + SocketIO service
├── quick_start.py        # One-click script to launch frontend and backend
├── vue_frontend.html     # Frontend page (served statically via http.server)
├── train.py              # Test training script (can be called by Bash command)
```

## Installation
Python 3.7+ is recommended. Install the following dependencies:

```bash
pip install flask flask_cors flask_socketio
```

## How to Start
1. **One-click start (recommended):**
   ```bash
   python quick_start.py
   ```
   The frontend page will open automatically.

2. **Manual start:**
   - Start backend:
     ```bash
     python app.py
     ```
   - Start frontend static server:
     ```bash
     python -m http.server 8080
     ```
   - Open in browser:
     [http://localhost:8080/vue_frontend.html](http://localhost:8080/vue_frontend.html)

## Usage
- Enter a Bash training command in the web input box (e.g., `python train.py --epochs 5`)
- Click "Start Training" to monitor logs in real time
- You can stop or delete processes at any time

## Test Script
- `train.py` is a mock training script with common arguments for testing

---
If you encounter port conflicts or missing dependencies, please follow the terminal prompts to resolve them. 