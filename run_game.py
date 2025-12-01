import os
import sys
import subprocess

def main():
    base_dir = os.path.dirname(__file__)
    game_file = os.path.join(base_dir, "main.py")
    subprocess.check_call([sys.executable, game_file])

if __name__ == "__main__":
    main()