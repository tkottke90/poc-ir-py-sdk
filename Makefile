# Makefile for iRacing Python project

# Detect OS
ifeq ($(OS),Windows_NT)
    PYTHON := venv/Scripts/python.exe
    PIP := venv/Scripts/pip.exe
    RM := del /Q
    RMDIR := rmdir /S /Q
    EXECUTABLE := dist/changeCamera.exe
else
    PYTHON := venv/bin/python
    PIP := venv/bin/pip
    RM := rm -f
    RMDIR := rm -rf
    EXECUTABLE := dist/changeCamera
endif

.PHONY: help venv install build clean run test activate test-obs

# Default target
help:
	@echo "Available targets:"
	@echo "  make venv       - Create virtual environment"
	@echo "  make install    - Install dependencies from requirements.txt"
	@echo "  make build      - Build standalone executable with PyInstaller"
	@echo "  make clean      - Remove build artifacts and venv"
	@echo "  make run GROUP=N - Run the script with camera group N (requires venv)"
	@echo "  make all        - Setup venv, install deps, and build executable"
	@echo "  make activate   - Show command to activate venv manually"
	@echo "  make test-obs   - Run OBS WebSocket connection troubleshooting"

# Create virtual environment (only if it doesn't exist)
venv:
ifeq ($(OS),Windows_NT)
	@if not exist venv (python -m venv venv && echo Virtual environment created.) else (echo Virtual environment already exists.)
else
	@if [ ! -d "venv" ]; then \
		python3 -m venv venv && echo "Virtual environment created."; \
	else \
		echo "Virtual environment already exists."; \
	fi
endif
	@echo "Run 'make install' to install dependencies."

# Install dependencies
install: venv
	$(PIP) install -r requirements.txt
	@echo "Dependencies installed."

# Build executable with PyInstaller
build: install
	$(PIP) install pyinstaller
	$(PYTHON) -m PyInstaller --onefile changeCamera.py
	@echo "Executable built: $(EXECUTABLE)"

# Run the script (example: make run GROUP=1)
run:
ifndef GROUP
	@echo "Error: Please specify GROUP number (e.g., make run GROUP=1)"
	@exit 1
endif
	$(PYTHON) changeCamera.py $(GROUP)

# Clean build artifacts
clean:
	$(RMDIR) build dist __pycache__ *.spec 2>/dev/null || true
	@echo "Build artifacts cleaned."

# Clean everything including venv
clean-all: clean
	$(RMDIR) venv 2>/dev/null || true
	@echo "Virtual environment removed."

# Setup everything and build
all: venv install build
	@echo "Setup complete! Executable available at: $(EXECUTABLE)"

# Show how to activate venv manually
activate: venv
ifeq ($(OS),Windows_NT)
	@echo "To activate the virtual environment, run:"
	@echo "  venv\\Scripts\\activate.bat    (Command Prompt)"
	@echo "  venv\\Scripts\\Activate.ps1    (PowerShell)"
else
	@echo "To activate the virtual environment, run:"
	@echo "  source venv/bin/activate"
endif

# Test OBS WebSocket connection
test-obs: install
	@echo "Running OBS WebSocket troubleshooting..."
	$(PYTHON) obs_troubleshoot.py

