import os
import sys

# Add the root directory to sys.path so imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui.main_window import launch_gui

def main():
    launch_gui()

if __name__ == "__main__":
    main()
