# SFC-Defrag-Emulator
Python SFC Scannow Defrag95 like emulation for nostalgia
![retro-defrag](https://github.com/user-attachments/assets/99167ad3-17de-4a8d-a6db-9d5a224616d9)


# SFC Defrag Visualizer - Installation Guide

A retro Windows 95-style defragmenter visualization that displays the progress of Windows System File Checker (SFC) scan in real-time.

## Requirements

- Windows 11
- Python 3.8 or higher
- Administrator privileges (required to run SFC scan)

## Step-by-Step Installation

### Step 1: Install Python

1. Download Python from the official website: https://www.python.org/downloads/
2. Run the installer
3. **IMPORTANT**: Check the box "Add Python to PATH" during installation
4. Click "Install Now"
5. Wait for installation to complete

### Step 2: Verify Python Installation

1. Open Command Prompt (CMD)
2. Type the following command and press Enter:
   ```
   python --version
   ```
3. You should see something like `Python 3.x.x`

### Step 3: Install Pygame

1. In Command Prompt, type the following command and press Enter:
   ```
   pip install pygame
   ```
2. Wait for installation to complete
3. You should see "Successfully installed pygame"

### Step 4: Download the Script

1. Download the `sfc_defrag_visualizer.py` file
2. Save it to a location you can easily access (e.g., `C:\Users\YourName\Desktop\`)

## Running the Application

### Step 1: Open Command Prompt as Administrator

1. Press `Windows Key + X`
2. Select "Terminal (Admin)" or "Command Prompt (Admin)"
3. Click "Yes" when asked for administrator permission

### Step 2: Navigate to Script Location

1. Use the `cd` command to navigate to where you saved the script:
   ```
   cd C:\Users\YourName\Desktop\
   ```
   (Replace with your actual path)

### Step 3: Run the Script

1. Type the following command and press Enter:
   ```
   python sfc_defrag_visualizer.py
   ```
2. The application window will open and the SFC scan will begin automatically

## What to Expect

- A retro-style window will appear with a grid of colored blocks
- Light cyan blocks represent files to be checked
- Red blocks (the "snake") show the current scanning position
- The last red block will blink to indicate active progress
- Dark blue blocks show completed verification
- White blocks represent free space
- A progress bar at the bottom shows the overall completion percentage
- The scan may take 15-30 minutes to complete

## Troubleshooting

### "python is not recognized as an internal or external command"
- Python is not in your PATH
- Reinstall Python and make sure to check "Add Python to PATH"

### "pip is not recognized as an internal or external command"
- Run: `python -m pip install pygame` instead

### "Access Denied" or "Administrator privileges required"
- Make sure you opened Command Prompt as Administrator (see Step 1 above)

### Application window doesn't open
- Check if pygame installed correctly: `pip show pygame`
- Reinstall pygame if needed: `pip uninstall pygame` then `pip install pygame`

### SFC scan doesn't start
- Make sure you're running CMD as Administrator
- Try running `sfc /scannow` manually first to verify it works

## Notes

- The SFC scan is a real Windows system scan that checks for corrupted system files
- It requires administrator privileges to run
- The scan can take 15-30 minutes depending on your system
- Do not close the application window during the scan
- The application will automatically close when the scan completes

## Exiting the Application

- To exit during the scan, simply close the window by clicking the X button
- The SFC scan will continue running in the background and can be viewed in CMD
