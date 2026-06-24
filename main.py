import os
import sys
import urllib3

# Suppress SSL warnings globally
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ==========================================
# DLL FIX (Windows / PyInstaller Compatibility)
# ==========================================
if getattr(sys, 'frozen', False):
    script_dir = sys._MEIPASS
else:
    script_dir = os.path.dirname(os.path.abspath(__file__))

if hasattr(os, "add_dll_directory"):
    os.add_dll_directory(script_dir)
os.environ["PATH"] = script_dir + os.pathsep + os.environ["PATH"]

from app import Application

if __name__ == "__main__":
    app = Application()
    sys.exit(app.run())