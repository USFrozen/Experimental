import os
import sys
import subprocess

def main():
    # Upgrade pip
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])

    # Install requirements from requirements.txt
    base_dir = os.path.dirname(__file__)
    req_file = os.path.join(base_dir, "requirements.txt")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", req_file])

    print("\n✅ Installation complete! Run the game with:\n")
    print(f"    {sys.executable} run_game.py\n")

if __name__ == "__main__":
    main()
