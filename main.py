print("loading imports")

import pyautogui
import time
import os
import sys
import requests
import shutil
import re
from pathlib import Path

# Perform checks
if input("Is Minecraft FOV at 82? [Y/N]: ").strip().lower() == "n":
    print("Find out how \033]8;;https://github.com/Eletroman179/JC-menu/blob/main/tutorials/FOV.md\033\\Here\033]8;;\033\\")
    print("This is required")
    sys.exit(0)
if input("Is Minecraft at the next tab? [Y/N]: ").strip().lower() == "n":
    print("This is required")
    sys.exit(0)
if input("Is Minecraft resolution at 1024 x 1024? [Y/N]: ").strip().lower() == "n":
    print("Find out how \033]8;;https://github.com/Eletroman179/JC-menu/blob/main/tutorials/resolution.md\033\\Here\033]8;;\033\\")
    print("This is required")
    sys.exit(0)

cords = input("enter cords with F3 + C or X Y Z\n")

pattern = r'tp @s (-?\d+\.?\d*) (-?\d+\.?\d*) (-?\d+\.?\d*)'  # Updated to handle floating-point numbers
match = re.search(pattern, cords)

if match:
    # Extract coordinates from the matched pattern as float values
    x, y, z = map(float, match.groups())
    target_position = (x, y, z)
else:
    # Attempt to parse plain coordinates if not in "tp @s" format
    try:
        coords = list(map(float, target_input.strip().split()))
        if len(coords) != 3:
            raise ValueError("Invalid coordinate input.")
        target_position = tuple(coords)
    except ValueError:
        print(f"{Back.RED}{Fore.BLACK}Error: Invalid input format. Expected 'tp @s X Y Z' or 'X Y Z'.{Style.RESET_ALL}")
        sys.exit(1)

# Define paths
screenshot_path = Path(input("screenshot path: "))
downloads_path = Path("C:\\Users\\James\\Downloads")
main_path = downloads_path / "main"
save_path = main_path / "assets/minecraft/textures/gui/title/background"
zip_name = input("Output name: ") + ".zip"
zip_path = downloads_path / zip_name

# Ensure the destination folder exists
save_path.mkdir(parents=True, exist_ok=True)

# Delete the old zip file if it exists
if zip_path.exists():
    zip_path.unlink()
    print(f"Deleted old file: {zip_path}")

# Switch to Minecraft window
pyautogui.hotkey('alt', 'tab')

def command(cmd):
    pyautogui.press("/")
    pyautogui.typewrite(cmd)
    pyautogui.press("enter")
    #time.sleep(0.2)
    pyautogui.press("F2")

# Wait before executing commands
time.sleep(2)

# Execute teleport commands
command(f"tp Electroman179 {x} {y} {z} -180 0")
command(f"tp Electroman179 {x} {y} {z} -90 0")
command(f"tp Electroman179 {x} {y} {z} 0 0")
command(f"tp Electroman179 {x} {y} {z} 90 0")
command(f"tp Electroman179 {x} {y} {z} -180 -90")
command(f"tp Electroman179 {x} {y} {z} -180 90")

# Wait for screenshots to save
time.sleep(3)

# Get the 5 latest .png files based on the creation time
png_files = sorted(screenshot_path.glob("*.png"), key=lambda f: f.stat().st_ctime)[:6]

# Rename and move them to the new location
for index, file in enumerate(png_files):
    new_name = save_path / f"panorama_{index}.png"
    file.rename(new_name)
    print(f"Moved {file} -> {new_name}")

# Function to download files
def download_file(url, dest):
    response = requests.get(url)
    if response.status_code == 200:
        with open(dest, "wb") as file:
            file.write(response.content)
        print(f"Downloaded {dest}")
    else:
        print(f"Failed to download {url}")

# Download pack.mcmeta and pack.png
download_file("https://raw.githubusercontent.com/Eletroman179/JC-menu/main/depndencies/pack.mcmeta", main_path / "pack.mcmeta")
download_file("https://raw.githubusercontent.com/Eletroman179/JC-menu/main/depndencies/pack.png", main_path / "pack.png")

# Zip the 'main' directory
shutil.make_archive(str(zip_path).replace(".zip", ""), 'zip', str(main_path))
print(f"Zipped to {zip_path}")

# Delete the 'main' folder after zipping
shutil.rmtree(main_path)
print(f"Deleted the 'main' folder at {main_path}")

print("All files moved, downloaded, zipped, and the 'main' folder deleted successfully!")
